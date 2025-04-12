"""
Data enrichment module for the Solar Lead Generation System.
Integrates data from various sources and enriches property records.
"""

import os
import logging
import json
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataEnrichmentPipeline:
    """Class to integrate and enrich data from multiple sources."""
    
    def __init__(self, database, property_collector, utility_collector, roof_collector, skip_tracer):
        """
        Initialize with component instances.
        
        Args:
            database: Database instance for storing data
            property_collector: PropertyDataCollector instance
            utility_collector: UtilityDataCollector instance
            roof_collector: RoofDataCollector instance
            skip_tracer: SkipTracer instance
        """
        self.database = database
        self.property_collector = property_collector
        self.utility_collector = utility_collector
        self.roof_collector = roof_collector
        self.skip_tracer = skip_tracer
        
    def process_property(self, address, city, state, zip_code):
        """
        Process a single property through the entire pipeline.
        
        Args:
            address: Street address
            city: City name
            state: State code
            zip_code: ZIP code
            
        Returns:
            Dictionary with processed data including property_id
        """
        logger.info(f"Processing property: {address}, {city}, {state} {zip_code}")
        
        try:
            # Step 1: Fetch property data
            property_data = self.property_collector.fetch_property_by_address(address, city, state, zip_code)
            if not property_data:
                logger.warning(f"Could not find property data for {address}")
                return None
            
            # Step 2: Check if property meets basic criteria
            if not self._meets_basic_criteria(property_data):
                logger.info(f"Property does not meet basic criteria: {address}")
                return None
            
            # Step 3: Insert property into database
            property_id = self.database.insert_property(property_data)
            if not property_id:
                logger.error(f"Failed to insert property into database: {address}")
                return None
            
            # Step 4: Fetch utility data
            utility_data = self.utility_collector.fetch_utility_rates_by_zip(zip_code)
            if utility_data:
                # Calculate estimated monthly bill
                square_footage = property_data.get('square_footage', 0)
                utility_data['estimated_monthly_bill'] = self.utility_collector.estimate_monthly_bill(
                    square_footage, utility_data
                )
                
                # Add property_id and insert into database
                utility_data['property_id'] = property_id
                self.database.insert_utility(utility_data)
            
            # Step 5: Fetch roof data
            if 'latitude' in property_data and 'longitude' in property_data:
                roof_data = self.roof_collector.fetch_roof_data(
                    property_data['latitude'], 
                    property_data['longitude'],
                    address
                )
                
                if roof_data:
                    # Estimate solar potential
                    solar_potential = self.roof_collector.estimate_solar_potential(roof_data, utility_data)
                    roof_data.update(solar_potential)
                    
                    # Add property_id and insert into database
                    roof_data['property_id'] = property_id
                    self.database.insert_roof(roof_data)
            
            # Step 6: Perform skip tracing
            owner_data = self.skip_tracer.trace_property_owner(property_data)
            if owner_data:
                # Add property_id and insert into database
                owner_data['property_id'] = property_id
                homeowner_id = self.database.insert_homeowner(owner_data)
                
                # Step 7: Create lead record if all data is available
                if homeowner_id and 'roof_id' in locals() and 'utility_id' in locals():
                    # Calculate lead score
                    lead_score = self._calculate_lead_score(property_data, utility_data, roof_data, owner_data)
                    
                    # Create lead data
                    lead_data = {
                        'property_id': property_id,
                        'homeowner_id': homeowner_id,
                        'lead_score': lead_score,
                        'lead_status': 'new',
                        'estimated_savings': solar_potential.get('annual_savings', 0) if 'solar_potential' in locals() else 0,
                        'estimated_system_size': solar_potential.get('system_size', 0) if 'solar_potential' in locals() else 0,
                        'estimated_installation_cost': solar_potential.get('system_cost', 0) if 'solar_potential' in locals() else 0,
                        'estimated_payback_period': solar_potential.get('payback_period', 0) if 'solar_potential' in locals() else 0
                    }
                    
                    # Insert lead into database
                    lead_id = self.database.insert_lead(lead_data)
            
            # Return the processed data
            return {
                'property_id': property_id,
                'property_data': property_data,
                'utility_data': utility_data if 'utility_data' in locals() else None,
                'roof_data': roof_data if 'roof_data' in locals() else None,
                'owner_data': owner_data if 'owner_data' in locals() else None,
                'lead_id': lead_id if 'lead_id' in locals() else None
            }
            
        except Exception as e:
            logger.error(f"Error processing property: {e}")
            return None
    
    def batch_process_properties(self, property_list):
        """
        Process a batch of properties through the pipeline.
        
        Args:
            property_list: List of property dictionaries or addresses
            
        Returns:
            List of processed property results
        """
        logger.info(f"Batch processing {len(property_list)} properties")
        
        results = []
        for prop in property_list:
            if isinstance(prop, dict):
                # If property is a dictionary, extract address components
                address = prop.get('address_line_1', '')
                city = prop.get('city', '')
                state = prop.get('state', '')
                zip_code = prop.get('zip_code', '')
            else:
                # If property is an address string, parse it (simplified)
                parts = prop.split(',')
                if len(parts) >= 3:
                    address = parts[0].strip()
                    city = parts[1].strip()
                    state_zip = parts[2].strip().split()
                    state = state_zip[0] if state_zip else ''
                    zip_code = state_zip[1] if len(state_zip) > 1 else ''
                else:
                    logger.warning(f"Could not parse address: {prop}")
                    continue
            
            # Process the property
            result = self.process_property(address, city, state, zip_code)
            if result:
                results.append(result)
        
        logger.info(f"Completed batch processing with {len(results)} successful properties")
        return results
    
    def import_and_process_csv(self, csv_file):
        """
        Import properties from CSV and process them.
        
        Args:
            csv_file: Path to CSV file
            
        Returns:
            List of processed property results
        """
        logger.info(f"Importing and processing properties from {csv_file}")
        
        # Import properties from CSV
        properties = self.property_collector.import_properties_from_csv(csv_file)
        
        # Process the imported properties
        return self.batch_process_properties(properties)
    
    def _meets_basic_criteria(self, property_data):
        """
        Check if property meets basic criteria for solar leads.
        
        Args:
            property_data: Dictionary with property information
            
        Returns:
            Boolean indicating if property meets criteria
        """
        # Check if property is a single-family home
        if property_data.get('property_type', '').lower() != 'single-family':
            return False
        
        # Check if property is owner-occupied
        if not property_data.get('is_owner_occupied', False):
            return False
        
        # Check if property already has solar
        if property_data.get('has_solar_installation', False):
            return False
        
        # Check if property has a recent solar permit
        if property_data.get('has_solar_permit', False):
            return False
        
        # Property passes basic criteria
        return True
    
    def _calculate_lead_score(self, property_data, utility_data, roof_data, owner_data):
        """
        Calculate a lead score based on all available data.
        
        Args:
            property_data: Dictionary with property information
            utility_data: Dictionary with utility information
            roof_data: Dictionary with roof information
            owner_data: Dictionary with owner information
            
        Returns:
            Integer score from 0-100
        """
        # This is a simplified scoring algorithm
        # In a real implementation, this would be more sophisticated
        
        score = 50  # Start with a neutral score
        
        # Property factors (up to +/-15 points)
        if property_data:
            # Age of home
            year_built = property_data.get('year_built', 0)
            if year_built > 0:
                if year_built < 1970:
                    score -= 5  # Older homes may need electrical upgrades
                elif year_built > 2010:
                    score += 5  # Newer homes typically have better electrical systems
            
            # Home value
            assessed_value = property_data.get('assessed_value', 0)
            if assessed_value > 500000:
                score += 5  # Higher value homes often have more disposable income
            
            # Square footage
            square_footage = property_data.get('square_footage', 0)
            if square_footage > 2500:
                score += 5  # Larger homes typically have higher energy usage
        
        # Utility factors (up to +/-30 points)
        if utility_data:
            # Monthly bill
            monthly_bill = utility_data.get('estimated_monthly_bill', 0)
            if monthly_bill > 200:
                score += 15  # High bills mean more savings potential
            elif monthly_bill > 150:
                score += 10
            elif monthly_bill > 120:
                score += 5
            else:
                score -= 10  # Low bills mean less savings potential
            
            # Net metering
            if utility_data.get('has_net_metering', False):
                score += 15  # Net metering significantly improves ROI
        
        # Roof factors (up to +/-40 points)
        if roof_data:
            # Usable area
            usable_area = roof_data.get('usable_roof_area', 0)
            if usable_area > 1000:
                score += 10  # Larger usable area means more panels
            elif usable_area < 500:
                score -= 10  # Small usable area limits system size
            
            # Orientation
            orientation = roof_data.get('primary_orientation', '')
            if orientation in ['S', 'SE', 'SW']:
                score += 15  # Optimal orientations
            elif orientation in ['E', 'W']:
                score += 5  # Acceptable orientations
            else:
                score -= 15  # Poor orientations
            
            # Shading
            shading = roof_data.get('shading_percentage', 0)
            if shading < 10:
                score += 15  # Minimal shading is ideal
            elif shading < 20:
                score += 5  # Some shading is acceptable
            else:
                score -= 15  # Heavy shading reduces production
        
        # Owner factors (up to +/-15 points)
        if owner_data:
            # Length of ownership
            ownership_length = owner_data.get('length_of_ownership', 0)
            if ownership_length > 5:
                score += 5  # Longer ownership suggests stability
            
            # Do Not Call list
            if owner_data.get('do_not_call', False):
                score -= 10  # DNC status makes contact more difficult
        
        # Ensure score is within 0-100 range
        score = max(0, min(100, score))
        
        return score
