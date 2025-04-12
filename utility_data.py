"""
Utility data collection module for the Solar Lead Generation System.
Handles fetching utility rate data from various sources.
"""

import requests
import json
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class UtilityDataCollector:
    """Class to collect utility data from various sources."""
    
    def __init__(self, api_keys=None):
        """Initialize with API keys for different services."""
        self.api_keys = api_keys or {}
        
    def fetch_utility_rates_by_location(self, latitude, longitude):
        """
        Fetch utility rates by geographic location using NREL API.
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            Dictionary with utility rate data or None if not found
        """
        logger.info(f"Fetching utility rates for location: {latitude}, {longitude}")
        
        try:
            # Check if we have an NREL API key
            if 'nrel' in self.api_keys:
                api_key = self.api_keys['nrel']
                
                # Construct API URL and parameters for NREL Utility Rates API
                url = "https://developer.nrel.gov/api/utility_rates/v3.json"
                params = {
                    "api_key": api_key,
                    "lat": latitude,
                    "lon": longitude
                }
                
                # Make the API request
                # response = requests.get(url, params=params)
                # if response.status_code == 200:
                #     return response.json().get('outputs', {})
                
                # For now, return mock data
                return self._mock_utility_data(latitude, longitude)
            else:
                logger.warning("No NREL API key provided")
                return self._mock_utility_data(latitude, longitude)
                
        except Exception as e:
            logger.error(f"Error fetching utility rates: {e}")
            return None
    
    def fetch_utility_rates_by_zip(self, zip_code):
        """
        Fetch utility rates by ZIP code.
        
        Args:
            zip_code: ZIP code to search
            
        Returns:
            Dictionary with utility rate data or None if not found
        """
        logger.info(f"Fetching utility rates for ZIP code: {zip_code}")
        
        try:
            # In a real implementation, we would convert ZIP to lat/lon
            # For now, use mock coordinates for Texas
            import random
            # Approximate coordinates for Texas
            latitude = 31.0 + random.uniform(-3, 3)
            longitude = -100.0 + random.uniform(-5, 5)
            
            return self.fetch_utility_rates_by_location(latitude, longitude)
                
        except Exception as e:
            logger.error(f"Error fetching utility rates by ZIP: {e}")
            return None
    
    def estimate_monthly_bill(self, square_footage, utility_rates=None):
        """
        Estimate monthly electricity bill based on home size and utility rates.
        
        Args:
            square_footage: Home size in square feet
            utility_rates: Dictionary with utility rate information
            
        Returns:
            Estimated monthly bill in dollars
        """
        logger.info(f"Estimating monthly bill for {square_footage} sq ft home")
        
        try:
            # Default values if utility_rates not provided
            if utility_rates is None:
                utility_rates = {
                    'residential': 0.12  # National average rate in $/kWh
                }
            
            # Get the residential rate
            rate = utility_rates.get('residential', 0.12)
            
            # Estimate monthly usage based on square footage
            # Average usage is about 12 kWh per square foot per year
            annual_usage = square_footage * 12
            monthly_usage = annual_usage / 12
            
            # Calculate estimated bill
            estimated_bill = monthly_usage * rate
            
            logger.info(f"Estimated monthly bill: ${estimated_bill:.2f}")
            return estimated_bill
            
        except Exception as e:
            logger.error(f"Error estimating monthly bill: {e}")
            return 0
    
    def check_net_metering_availability(self, utility_provider, state='TX'):
        """
        Check if net metering is available for a given utility provider.
        
        Args:
            utility_provider: Name of the utility company
            state: State code (default: TX for Texas)
            
        Returns:
            Dictionary with net metering information
        """
        logger.info(f"Checking net metering for {utility_provider} in {state}")
        
        # This would typically involve checking a database of utility policies
        # For now, return mock data based on common Texas utilities
        
        # Texas utilities with net metering or similar programs
        net_metering_utilities = {
            'Austin Energy': {
                'has_net_metering': True,
                'net_metering_rate': 0.097,
                'notes': 'Value of Solar Tariff instead of traditional net metering'
            },
            'CPS Energy': {
                'has_net_metering': True,
                'net_metering_rate': 0.09,
                'notes': 'Net billing at avoided cost rate'
            },
            'El Paso Electric': {
                'has_net_metering': True,
                'net_metering_rate': 0.08,
                'notes': 'Limited net metering available'
            },
            'Green Mountain Energy': {
                'has_net_metering': True,
                'net_metering_rate': 0.11,
                'notes': 'Renewable Rewards buyback program'
            }
        }
        
        # Default response for utilities without specific net metering programs
        default_response = {
            'has_net_metering': False,
            'net_metering_rate': 0.0,
            'notes': 'No net metering program available'
        }
        
        return net_metering_utilities.get(utility_provider, default_response)
    
    def get_utility_provider_by_location(self, latitude, longitude):
        """
        Determine the utility provider for a given location.
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            Name of the utility provider
        """
        logger.info(f"Finding utility provider for location: {latitude}, {longitude}")
        
        # This would typically involve checking a geospatial database of utility service areas
        # For now, return a mock result based on Texas regions
        
        # Simple logic to assign utilities based on coordinates
        # In a real implementation, this would use GIS data
        
        # Approximate regions for major Texas utilities
        if latitude > 30.2 and longitude > -97.8:
            return "Austin Energy"  # Austin area
        elif latitude > 29.3 and longitude > -98.6:
            return "CPS Energy"  # San Antonio area
        elif latitude > 31.7 and longitude < -106.3:
            return "El Paso Electric"  # El Paso area
        elif latitude > 29.5 and longitude > -95.5:
            return "Centerpoint Energy"  # Houston area
        elif latitude > 32.7 and longitude > -96.8:
            return "Oncor Electric"  # Dallas area
        else:
            # Default to a common retail provider
            return "Green Mountain Energy"
    
    def _mock_utility_data(self, latitude, longitude):
        """Generate mock utility data for testing."""
        import random
        
        # Determine utility provider based on location
        utility_provider = self.get_utility_provider_by_location(latitude, longitude)
        
        # Generate realistic mock data
        residential_rate = random.uniform(0.09, 0.15)
        commercial_rate = random.uniform(0.08, 0.13)
        industrial_rate = random.uniform(0.06, 0.10)
        
        # Check if net metering is available
        net_metering_info = self.check_net_metering_availability(utility_provider)
        
        return {
            'utility_provider': utility_provider,
            'utility_rate_plan': 'Standard Residential',
            'residential': residential_rate,
            'commercial': commercial_rate,
            'industrial': industrial_rate,
            'base_rate': residential_rate * 0.7,  # Base rate is typically lower than total rate
            'tdu_rate': residential_rate * 0.3,  # TDU portion
            'has_net_metering': net_metering_info['has_net_metering'],
            'net_metering_rate': net_metering_info['net_metering_rate'],
            'data_source': 'mock_data'
        }
