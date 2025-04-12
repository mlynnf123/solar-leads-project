"""
Bill estimation module for the Solar Lead Generation System.
Implements advanced algorithms for estimating electric bills based on property characteristics.
"""

import logging
import numpy as np
from datetime import datetime
import calendar

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BillEstimator:
    """Class to estimate electric bills based on property characteristics and location."""
    
    def __init__(self, config=None):
        """
        Initialize with optional configuration parameters.
        
        Args:
            config: Dictionary with configuration parameters
        """
        self.config = config or {}
        
        # Default base consumption values by home size (kWh/month)
        self.base_consumption = self.config.get('base_consumption', {
            'small': 700,      # <1200 sq ft
            'medium': 1000,    # 1200-2500 sq ft
            'large': 1300,     # 2500-3500 sq ft
            'very_large': 1600 # >3500 sq ft
        })
        
        # Monthly usage factors for Texas (relative to annual average)
        # Based on typical seasonal patterns in Texas
        self.monthly_factors = self.config.get('monthly_factors', {
            1: 0.85,   # January
            2: 0.80,   # February
            3: 0.75,   # March
            4: 0.80,   # April
            5: 1.00,   # May
            6: 1.30,   # June
            7: 1.50,   # July
            8: 1.50,   # August
            9: 1.20,   # September
            10: 0.90,  # October
            11: 0.75,  # November
            12: 0.85   # December
        })
        
        # Climate zone factors for Texas regions
        self.climate_zones = self.config.get('climate_zones', {
            'north': {
                'base_factor': 1.0,
                'zip_prefixes': ['750', '751', '752', '753', '754', '755', '756', '757', '758', '759', '760', '761', '762', '763', '764', '765', '766', '767']
            },
            'central': {
                'base_factor': 1.05,
                'zip_prefixes': ['768', '769', '770', '771', '772', '773', '774', '775', '776', '777', '778', '779', '780', '781', '782', '783', '784', '785']
            },
            'south': {
                'base_factor': 1.15,
                'zip_prefixes': ['786', '787', '788', '789', '790', '791', '792', '793', '794', '795', '796', '797', '798', '799']
            }
        })
    
    def estimate_monthly_bill(self, property_data, utility_data=None, month=None):
        """
        Estimate monthly electric bill based on property characteristics and utility rates.
        
        Args:
            property_data: Dictionary with property information
            utility_data: Optional dictionary with utility rate information
            month: Optional month (1-12) to estimate for specific month, or None for annual average
            
        Returns:
            Estimated monthly bill in dollars
        """
        logger.info(f"Estimating electric bill for property")
        
        try:
            # Extract property characteristics
            square_footage = property_data.get('square_footage', 0)
            year_built = property_data.get('year_built', 2000)
            bedrooms = property_data.get('bedrooms', 3)
            zip_code = property_data.get('zip_code', '')
            
            # Default electricity rate if utility_data not provided
            if utility_data and 'residential' in utility_data:
                rate = utility_data.get('residential')
            else:
                rate = 0.12  # National average rate in $/kWh
            
            # Determine base consumption by home size
            if square_footage < 1200:
                base_usage = self.base_consumption['small']
            elif square_footage < 2500:
                base_usage = self.base_consumption['medium']
            elif square_footage < 3500:
                base_usage = self.base_consumption['large']
            else:
                base_usage = self.base_consumption['very_large']
            
            # Fine-tune based on exact square footage
            if square_footage > 0:
                # Determine the category boundaries
                if square_footage < 1200:
                    min_sqft, max_sqft = 800, 1200
                    min_usage, max_usage = self.base_consumption['small'] * 0.8, self.base_consumption['small']
                elif square_footage < 2500:
                    min_sqft, max_sqft = 1200, 2500
                    min_usage, max_usage = self.base_consumption['medium'] * 0.8, self.base_consumption['medium'] * 1.2
                elif square_footage < 3500:
                    min_sqft, max_sqft = 2500, 3500
                    min_usage, max_usage = self.base_consumption['large'] * 0.8, self.base_consumption['large'] * 1.2
                else:
                    min_sqft, max_sqft = 3500, 5000
                    min_usage, max_usage = self.base_consumption['very_large'] * 0.8, self.base_consumption['very_large'] * 1.3
                
                # Linear interpolation within the category
                sqft_factor = (square_footage - min_sqft) / (max_sqft - min_sqft)
                base_usage = min_usage + sqft_factor * (max_usage - min_usage)
            
            # Adjust for home age (newer homes are typically more efficient)
            current_year = datetime.now().year
            if year_built > 0:
                age = current_year - year_built
                if age <= 5:
                    age_factor = 0.85  # 15% more efficient than average
                elif age <= 15:
                    age_factor = 0.9   # 10% more efficient than average
                elif age <= 30:
                    age_factor = 1.0   # Average efficiency
                elif age <= 50:
                    age_factor = 1.1   # 10% less efficient than average
                else:
                    age_factor = 1.2   # 20% less efficient than average
            else:
                age_factor = 1.0
            
            # Adjust for number of bedrooms (proxy for number of occupants)
            if bedrooms <= 1:
                bedroom_factor = 0.7
            elif bedrooms == 2:
                bedroom_factor = 0.85
            elif bedrooms == 3:
                bedroom_factor = 1.0
            elif bedrooms == 4:
                bedroom_factor = 1.15
            else:
                bedroom_factor = 1.25
            
            # Determine climate zone based on ZIP code
            climate_factor = 1.0  # Default
            for zone, data in self.climate_zones.items():
                for prefix in data['zip_prefixes']:
                    if zip_code.startswith(prefix):
                        climate_factor = data['base_factor']
                        break
            
            # Apply monthly seasonal factor if month is specified
            month_factor = 1.0
            if month is not None and 1 <= month <= 12:
                month_factor = self.monthly_factors.get(month, 1.0)
            
            # Calculate estimated monthly usage
            estimated_usage = base_usage * age_factor * bedroom_factor * climate_factor * month_factor
            
            # Calculate estimated bill
            estimated_bill = estimated_usage * rate
            
            logger.info(f"Estimated monthly bill: ${estimated_bill:.2f}")
            return estimated_bill
            
        except Exception as e:
            logger.error(f"Error estimating electric bill: {e}")
            return 0
    
    def estimate_annual_bill_profile(self, property_data, utility_data=None):
        """
        Estimate electric bill for each month of the year.
        
        Args:
            property_data: Dictionary with property information
            utility_data: Optional dictionary with utility rate information
            
        Returns:
            Dictionary with monthly bill estimates
        """
        logger.info(f"Estimating annual bill profile")
        
        monthly_bills = {}
        annual_total = 0
        
        for month in range(1, 13):
            monthly_bill = self.estimate_monthly_bill(property_data, utility_data, month)
            month_name = calendar.month_name[month]
            monthly_bills[month_name] = round(monthly_bill, 2)
            annual_total += monthly_bill
        
        return {
            'monthly': monthly_bills,
            'annual_total': round(annual_total, 2),
            'monthly_average': round(annual_total / 12, 2)
        }
    
    def estimate_bill_by_zip_code(self, zip_code, square_footage, year_built=2000, bedrooms=3):
        """
        Estimate electric bill based on ZIP code and basic property characteristics.
        
        Args:
            zip_code: Property ZIP code
            square_footage: Home size in square feet
            year_built: Year the home was built
            bedrooms: Number of bedrooms
            
        Returns:
            Estimated monthly bill in dollars
        """
        logger.info(f"Estimating bill by ZIP code: {zip_code}")
        
        # Create simplified property data dictionary
        property_data = {
            'zip_code': zip_code,
            'square_footage': square_footage,
            'year_built': year_built,
            'bedrooms': bedrooms
        }
        
        # Determine utility rate based on ZIP code
        # This would typically involve looking up the utility provider for the ZIP code
        # For now, use a simplified approach with Texas average rates
        
        # Different utility rates by region in Texas
        utility_rates = {
            'north': 0.115,    # North Texas (Dallas area)
            'central': 0.125,  # Central Texas (Austin/San Antonio area)
            'south': 0.135,    # South Texas (Houston area)
            'west': 0.110,     # West Texas
            'panhandle': 0.105 # Texas Panhandle
        }
        
        # Determine region based on ZIP code
        region = 'central'  # Default
        for zone, data in self.climate_zones.items():
            for prefix in data['zip_prefixes']:
                if zip_code.startswith(prefix):
                    region = zone
                    break
        
        # Map climate zones to utility regions
        region_map = {
            'north': 'north',
            'central': 'central',
            'south': 'south'
        }
        
        utility_region = region_map.get(region, 'central')
        rate = utility_rates.get(utility_region, 0.12)
        
        # Create simplified utility data
        utility_data = {
            'residential': rate,
            'utility_provider': f"{utility_region.capitalize()} Texas Utility"
        }
        
        # Estimate bill
        return self.estimate_monthly_bill(property_data, utility_data)
    
    def analyze_bill_factors(self, property_data, utility_data=None):
        """
        Analyze the factors affecting the electric bill.
        
        Args:
            property_data: Dictionary with property information
            utility_data: Optional dictionary with utility rate information
            
        Returns:
            Dictionary with analysis of bill factors
        """
        logger.info(f"Analyzing bill factors")
        
        try:
            # Base bill with all factors
            base_bill = self.estimate_monthly_bill(property_data, utility_data)
            
            # Create modified property data for each factor
            factors = {}
            
            # Size factor
            if 'square_footage' in property_data:
                smaller_property = property_data.copy()
                smaller_property['square_footage'] = property_data['square_footage'] * 0.8
                smaller_bill = self.estimate_monthly_bill(smaller_property, utility_data)
                
                larger_property = property_data.copy()
                larger_property['square_footage'] = property_data['square_footage'] * 1.2
                larger_bill = self.estimate_monthly_bill(larger_property, utility_data)
                
                factors['size'] = {
                    'description': 'Impact of home size',
                    'current': property_data['square_footage'],
                    'current_bill': base_bill,
                    'smaller': smaller_property['square_footage'],
                    'smaller_bill': smaller_bill,
                    'smaller_savings': base_bill - smaller_bill,
                    'larger': larger_property['square_footage'],
                    'larger_bill': larger_bill,
                    'larger_cost': larger_bill - base_bill
                }
            
            # Age factor
            if 'year_built' in property_data:
                newer_property = property_data.copy()
                newer_property['year_built'] = min(datetime.now().year - 5, property_data['year_built'] + 20)
                newer_bill = self.estimate_monthly_bill(newer_property, utility_data)
                
                older_property = property_data.copy()
                older_property['year_built'] = max(1900, property_data['year_built'] - 20)
                older_bill = self.estimate_monthly_bill(older_property, utility_data)
                
                factors['age'] = {
                    'description': 'Impact of home age',
                    'current': property_data['year_built'],
                    'current_bill': base_bill,
                    'newer': newer_property['year_built'],
                    'newer_bill': newer_bill,
                    'newer_savings': base_bill - newer_bill,
                    'older': older_property['year_built'],
                    'older_bill': older_bill,
                    'older_cost': older_bill - base_bill
                }
            
            # Rate factor
            if utility_data and 'residential' in utility_data:
                current_rate = utility_data['residential']
                
                lower_rate_utility = utility_data.copy()
                lower_rate_utility['residential'] = current_rate * 0.9
                lower_rate_bill = self.estimate_monthly_bill(property_data, lower_rate_utility)
                
                higher_rate_utility = utility_data.copy()
                higher_rate_utility['residential'] = current_rate * 1.1
                higher_rate_bill = self.estimate_monthly_bill(property_data, higher_rate_utility)
                
                factors['rate'] = {
                    'description': 'Impact of electricity rate',
                    'current': current_rate,
                    'current_bill': base_bill,
                    'lower': lower_rate_utility['residential'],
                    'lower_bill': lower_rate_bill,
                    'lower_savings': base_bill - lower_rate_bill,
                    'higher': higher_rate_utility['residential'],
                    'higher_bill': higher_rate_bill,
                    'higher_cost': higher_rate_bill - base_bill
                }
            
            # Seasonal factor
            current_month = datetime.now().month
            summer_bill = self.estimate_monthly_bill(property_data, utility_data, 7)  # July
            winter_bill = self.estimate_monthly_bill(property_data, utility_data, 1)  # January
            
            factors['seasonal'] = {
                'description': 'Seasonal impact on bill',
                'current_month': calendar.month_name[current_month],
                'current_bill': base_bill,
                'summer_month': 'July',
                'summer_bill': summer_bill,
                'summer_difference': summer_bill - base_bill,
                'winter_month': 'January',
                'winter_bill': winter_bill,
       
(Content truncated due to size limit. Use line ranges to read in chunks)