"""
Lead scoring module for the Solar Lead Generation System.
Implements algorithms for evaluating and scoring potential solar leads.
"""

import logging
import numpy as np
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LeadScoringEngine:
    """Class to calculate lead scores based on multiple factors."""
    
    def __init__(self, config=None):
        """
        Initialize with optional configuration parameters.
        
        Args:
            config: Dictionary with configuration parameters
        """
        self.config = config or {}
        
        # Default weights for different scoring components
        self.weights = self.config.get('weights', {
            'bill_size': 0.30,       # 30% weight for bill size
            'roof_suitability': 0.25, # 25% weight for roof suitability
            'property_value': 0.15,   # 15% weight for property value
            'net_metering': 0.20,     # 20% weight for net metering benefits
            'homeowner': 0.10         # 10% weight for homeowner characteristics
        })
        
        # Qualification thresholds
        self.thresholds = self.config.get('thresholds', {
            'excellent': 80,  # 80+ is excellent
            'good': 65,       # 65-79 is good
            'average': 50,    # 50-64 is average
            'poor': 35,       # 35-49 is poor
            'unsuitable': 0   # Below 35 is unsuitable
        })
        
        # Minimum requirements
        self.min_requirements = self.config.get('min_requirements', {
            'monthly_bill': 120,  # Minimum monthly bill ($)
            'roof_score': 30      # Minimum roof suitability score
        })
    
    def calculate_overall_score(self, property_data, utility_data=None, roof_data=None, owner_data=None):
        """
        Calculate overall lead score based on all available data.
        
        Args:
            property_data: Dictionary with property information
            utility_data: Optional dictionary with utility information
            roof_data: Optional dictionary with roof information
            owner_data: Optional dictionary with homeowner information
            
        Returns:
            Dictionary with overall score and component scores
        """
        logger.info(f"Calculating lead score for property")
        
        try:
            # Calculate component scores
            bill_score = self.calculate_bill_score(property_data, utility_data)
            roof_score = self.calculate_roof_score(property_data, roof_data)
            property_score = self.calculate_property_score(property_data)
            metering_score = self.calculate_net_metering_score(property_data, utility_data)
            homeowner_score = self.calculate_homeowner_score(property_data, owner_data)
            
            # Check if any component scores disqualify the lead
            if bill_score < self.min_requirements['monthly_bill']:
                disqualified = True
                disqualification_reason = "Monthly bill below minimum threshold"
            elif roof_score < self.min_requirements['roof_score']:
                disqualified = True
                disqualification_reason = "Roof unsuitable for solar installation"
            else:
                disqualified = False
                disqualification_reason = None
            
            # Calculate weighted overall score
            if disqualified:
                overall_score = 0
            else:
                overall_score = (
                    bill_score * self.weights['bill_size'] +
                    roof_score * self.weights['roof_suitability'] +
                    property_score * self.weights['property_value'] +
                    metering_score * self.weights['net_metering'] +
                    homeowner_score * self.weights['homeowner']
                )
            
            # Determine qualification category
            if overall_score >= self.thresholds['excellent']:
                qualification = "excellent"
            elif overall_score >= self.thresholds['good']:
                qualification = "good"
            elif overall_score >= self.thresholds['average']:
                qualification = "average"
            elif overall_score >= self.thresholds['poor']:
                qualification = "poor"
            else:
                qualification = "unsuitable"
            
            # Return comprehensive result
            return {
                'property_id': property_data.get('property_id', 'unknown'),
                'overall_score': round(overall_score),
                'qualification': qualification,
                'disqualified': disqualified,
                'disqualification_reason': disqualification_reason,
                'component_scores': {
                    'bill_score': round(bill_score),
                    'roof_score': round(roof_score),
                    'property_score': round(property_score),
                    'metering_score': round(metering_score),
                    'homeowner_score': round(homeowner_score)
                },
                'weights': self.weights,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error calculating lead score: {e}")
            return {
                'property_id': property_data.get('property_id', 'unknown'),
                'overall_score': 0,
                'qualification': 'error',
                'error': str(e)
            }
    
    def calculate_bill_score(self, property_data, utility_data=None):
        """
        Calculate score component based on estimated monthly bill.
        
        Args:
            property_data: Dictionary with property information
            utility_data: Optional dictionary with utility information
            
        Returns:
            Score from 0-100 for this component
        """
        # Get estimated monthly bill
        if utility_data and 'estimated_monthly_bill' in utility_data:
            monthly_bill = utility_data['estimated_monthly_bill']
        else:
            # Estimate based on property characteristics if no utility data
            # This is a simplified estimation; in practice, would use more sophisticated model
            if 'square_footage' in property_data:
                square_footage = property_data['square_footage']
                # Simple estimation: $0.10 per square foot per month
                monthly_bill = square_footage * 0.10
            else:
                monthly_bill = 0
        
        # Score based on bill size
        # $120 = 50 points (minimum qualifying)
        # $200 = 80 points
        # $300+ = 100 points
        
        if monthly_bill < 120:
            return 0  # Disqualify if below minimum
        elif monthly_bill >= 300:
            return 100
        elif monthly_bill >= 200:
            return 80 + (monthly_bill - 200) * 20 / 100
        else:
            return 50 + (monthly_bill - 120) * 30 / 80
    
    def calculate_roof_score(self, property_data, roof_data=None):
        """
        Calculate score component based on roof characteristics.
        
        Args:
            property_data: Dictionary with property information
            roof_data: Optional dictionary with roof information
            
        Returns:
            Score from 0-100 for this component
        """
        if not roof_data:
            return 50  # Neutral score if no roof data
        
        # Check if we have a pre-calculated roof score
        if 'overall_score' in roof_data:
            return roof_data['overall_score']
        
        # Calculate based on roof characteristics
        score = 0
        
        # Orientation factor (south-facing is best)
        if 'primary_orientation' in roof_data:
            orientation = roof_data['primary_orientation']
            orientation_scores = {
                'S': 100,   # South is optimal
                'SE': 90,   # Southeast is very good
                'SW': 90,   # Southwest is very good
                'E': 70,    # East is good
                'W': 70,    # West is good
                'NE': 40,   # Northeast is poor
                'NW': 40,   # Northwest is poor
                'N': 20     # North is very poor
            }
            orientation_score = orientation_scores.get(orientation, 50)
            score += orientation_score * 0.4  # 40% weight for orientation
        
        # Usable area factor
        if 'usable_roof_area' in roof_data:
            usable_area = roof_data['usable_roof_area']
            if usable_area < 400:
                area_score = 0  # Disqualify if too small
            elif usable_area >= 1200:
                area_score = 100
            else:
                area_score = 50 + (usable_area - 400) * 50 / 800
            score += area_score * 0.3  # 30% weight for area
        
        # Shading factor
        if 'shading_percentage' in roof_data:
            shading_pct = roof_data['shading_percentage']
            if shading_pct > 40:
                shading_score = 0  # Disqualify if too shaded
            else:
                shading_score = 100 - (shading_pct / 40) * 100
            score += shading_score * 0.2  # 20% weight for shading
        
        # Roof condition factor
        if 'roof_condition' in roof_data:
            condition = roof_data['roof_condition'].lower()
            condition_scores = {
                'excellent': 100,
                'good': 80,
                'fair': 60,
                'poor': 30,
                'very poor': 10
            }
            condition_score = condition_scores.get(condition, 50)
            score += condition_score * 0.1  # 10% weight for condition
        
        return score
    
    def calculate_property_score(self, property_data):
        """
        Calculate score component based on property characteristics.
        
        Args:
            property_data: Dictionary with property information
            
        Returns:
            Score from 0-100 for this component
        """
        score = 0
        
        # Owner-occupied factor
        if 'is_owner_occupied' in property_data:
            if property_data['is_owner_occupied']:
                score += 100 * 0.4  # 40% weight for owner-occupied
            else:
                return 0  # Disqualify if not owner-occupied
        
        # Property type factor
        if 'property_type' in property_data:
            property_type = property_data['property_type']
            if property_type == 'Single-Family':
                score += 100 * 0.3  # 30% weight for single-family
            elif property_type == 'Multi-Family':
                score += 50 * 0.3   # Multi-family gets half points
            else:
                score += 0 * 0.3     # Other types get no points
        
        # Property value factor
        if 'property_value' in property_data:
            value = property_data['property_value']
            if value >= 500000:
                value_score = 100
            elif value >= 300000:
                value_score = 80
            elif value >= 200000:
                value_score = 60
            elif value >= 100000:
                value_score = 40
            else:
                value_score = 20
            score += value_score * 0.2  # 20% weight for value
        
        # Solar permit factor
        if 'has_solar_permit' in property_data:
            if property_data['has_solar_permit']:
                return 0  # Disqualify if already has solar
            else:
                score += 100 * 0.1  # 10% weight for no solar
        
        return score
    
    def calculate_net_metering_score(self, property_data, utility_data=None):
        """
        Calculate score component based on net metering benefits.
        
        Args:
            property_data: Dictionary with property information
            utility_data: Optional dictionary with utility information
            
        Returns:
            Score from 0-100 for this component
        """
        if not utility_data:
            return 50  # Neutral score if no utility data
        
        score = 0
        
        # Net metering availability factor
        if 'net_metering_available' in utility_data:
            if utility_data['net_metering_available']:
                score += 100 * 0.6  # 60% weight for net metering availability
            else:
                score += 30 * 0.6   # Still possible but less attractive
        
        # Utility rate factor
        if 'residential' in utility_data:
            rate = utility_data['residential']
            if rate >= 0.14:
                rate_score = 100  # High rates make solar more attractive
            elif rate >= 0.12:
                rate_score = 80
            elif rate >= 0.10:
                rate_score = 60
            elif rate >= 0.08:
                rate_score = 40
            else:
                rate_score = 20
            score += rate_score * 0.4  # 40% weight for rate
        
        return score
    
    def calculate_homeowner_score(self, property_data, owner_data=None):
        """
        Calculate score component based on homeowner characteristics.
        
        Args:
            property_data: Dictionary with property information
            owner_data: Optional dictionary with homeowner information
            
        Returns:
            Score from 0-100 for this component
        """
        if not owner_data:
            return 50  # Neutral score if no owner data
        
        score = 0
        
        # Contact information factor
        has_phone = 'phone' in owner_data and owner_data['phone']
        has_email = 'email' in owner_data and owner_data['email']
        
        if has_phone and has_email:
            contact_score = 100
        elif has_phone:
            contact_score = 70
        elif has_email:
            contact_score = 60
        else:
            contact_score = 0
        
        score += contact_score * 0.4  # 40% weight for contact info
        
        # Do not call factor
        if 'do_not_call' in owner_data:
            if owner_data['do_not_call']:
                score += 0 * 0.3  # 30% weight for do not call
            else:
                score += 100 * 0.3
        
        # Ownership length factor
        if 'ownership_years' in owner_data:
            years = owner_data['ownership_years']
            if years >= 5:
                ownership_score = 100  # Long-term owners are better prospects
            elif years >= 3:
                ownership_score = 80
            elif years >= 1:
                ownership_score = 60
            else:
                ownership_score = 40
            score += ownership_score * 0.3  # 30% weight for ownership length
        
        return score
    
    def analyze_lead_distribution(self, scores):
        """
        Analyze the distribution of lead scores.
        
        Args:
            scores: List of lead scores
            
        Returns:
            Dictionary with distribution analysis
        """
        if not scores:
            return {
                'count': 0,
                'message': 'No scores to analyze'
            }
        
        # Convert to numpy array for analysis
        scores_array = np.array(scores)
        
        # Calculate statistics
        count = len(scores)
        mean = np.mean(scores_array)
        median = np.median(scores_array)
        std_dev = np.std(scores_array)
        min_score = np.min(scores_array)
        max_score = np.max(scores_array)
        
        # Calculate percentiles
        percentiles = {
            '10th': np.percentile(scores_array, 10),
            '25th': np.percentile
(Content truncated due to size limit. Use line ranges to read in chunks)