"""
Roof data collection module for the Solar Lead Generation System.
Handles fetching roof data and solar potential information.
"""

import requests
import json
import os
import logging
import random
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RoofDataCollector:
    """Class to collect roof data and solar potential information."""
    
    def __init__(self, api_keys=None):
        """Initialize with API keys for different services."""
        self.api_keys = api_keys or {}
        
    def fetch_roof_data(self, latitude, longitude, address=None):
        """
        Fetch roof data using Google Maps Platform Solar API.
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            address: Optional address for logging purposes
            
        Returns:
            Dictionary with roof data or None if not found
        """
        address_str = address if address else f"{latitude}, {longitude}"
        logger.info(f"Fetching roof data for: {address_str}")
        
        try:
            # Check if we have a Google Maps API key
            if 'google_maps' in self.api_keys:
                api_key = self.api_keys['google_maps']
                
                # Construct API URL and parameters for Google Solar API
                url = "https://solar.googleapis.com/v1/buildingInsights:findClosest"
                params = {
                    "key": api_key,
                    "location.latitude": latitude,
                    "location.longitude": longitude
                }
                
                # Make the API request
                # response = requests.get(url, params=params)
                # if response.status_code == 200:
                #     return self._parse_google_solar_response(response.json())
                
                # For now, return mock data
                return self._mock_roof_data(latitude, longitude)
            else:
                logger.warning("No Google Maps API key provided")
                return self._mock_roof_data(latitude, longitude)
                
        except Exception as e:
            logger.error(f"Error fetching roof data: {e}")
            return None
    
    def _parse_google_solar_response(self, response_data):
        """
        Parse the response from Google Solar API.
        
        Args:
            response_data: JSON response from Google Solar API
            
        Returns:
            Dictionary with parsed roof data
        """
        try:
            # Extract relevant information from the response
            # This would be customized based on the actual API response structure
            
            # Example parsing logic (adjust based on actual API response)
            building_insights = response_data.get('buildingInsights', {})
            
            # Extract roof information
            roof_data = {
                'total_roof_area': building_insights.get('roofSegmentStats', {}).get('totalAreaMeters2', 0) * 10.764,  # Convert m² to ft²
                'usable_roof_area': building_insights.get('solarPotential', {}).get('maxArrayAreaMeters2', 0) * 10.764,  # Convert m² to ft²
                'primary_orientation': self._get_primary_orientation(building_insights.get('roofSegmentStats', {}).get('pitches', [])),
                'azimuth': building_insights.get('roofSegmentStats', {}).get('azimuthDegrees', 0),
                'pitch': building_insights.get('roofSegmentStats', {}).get('pitchDegrees', 0),
                'estimated_solar_potential': building_insights.get('solarPotential', {}).get('maxSunshineHoursPerYear', 0),
                'data_source': 'google_solar_api'
            }
            
            return roof_data
            
        except Exception as e:
            logger.error(f"Error parsing Google Solar API response: {e}")
            return None
    
    def _get_primary_orientation(self, pitches):
        """
        Determine primary roof orientation from pitch data.
        
        Args:
            pitches: List of pitch data from Google Solar API
            
        Returns:
            Primary orientation as string (N, NE, E, SE, S, SW, W, NW)
        """
        # This would be customized based on the actual API response structure
        # For now, return a placeholder implementation
        
        # Convert azimuth to cardinal direction
        if not pitches:
            return 'Unknown'
        
        # Get the azimuth of the largest roof segment
        largest_segment = max(pitches, key=lambda x: x.get('areaMeters2', 0))
        azimuth = largest_segment.get('azimuthDegrees', 0)
        
        # Convert azimuth to cardinal direction
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N']
        index = round(azimuth / 45)
        return directions[index]
    
    def estimate_solar_potential(self, roof_data, utility_data=None):
        """
        Estimate solar potential based on roof characteristics and utility data.
        
        Args:
            roof_data: Dictionary with roof information
            utility_data: Optional dictionary with utility rate information
            
        Returns:
            Dictionary with solar potential estimates
        """
        logger.info("Estimating solar potential")
        
        try:
            # Extract roof characteristics
            usable_area = roof_data.get('usable_roof_area', 0)
            orientation = roof_data.get('primary_orientation', 'S')
            azimuth = roof_data.get('azimuth', 180)
            pitch = roof_data.get('pitch', 20)
            
            # Default values for Texas
            solar_irradiance = 5.0  # kWh/m²/day (typical for Texas)
            
            # Adjust for orientation
            orientation_factors = {
                'S': 1.0,
                'SE': 0.95,
                'SW': 0.95,
                'E': 0.85,
                'W': 0.85,
                'NE': 0.75,
                'NW': 0.75,
                'N': 0.65,
                'Unknown': 0.9
            }
            orientation_factor = orientation_factors.get(orientation, 0.9)
            
            # Adjust for pitch (optimal is around 20-30 degrees for Texas)
            pitch_factor = 1.0
            if pitch < 10:
                pitch_factor = 0.9
            elif pitch > 40:
                pitch_factor = 0.95
            
            # Calculate system size (kW)
            # Typical solar panel is about 17-18 sq ft and produces about 300W
            panel_area = 17.5  # sq ft
            panel_power = 0.3  # kW
            
            # Number of panels that can fit on the roof
            num_panels = int(usable_area / panel_area)
            
            # System size in kW
            system_size = num_panels * panel_power
            
            # Annual energy production (kWh)
            # Formula: System Size (kW) * Solar Irradiance (kWh/m²/day) * 365 days * Efficiency Factors
            annual_production = system_size * solar_irradiance * 365 * orientation_factor * pitch_factor * 0.75  # 0.75 accounts for system losses
            
            # Calculate financial metrics if utility data is provided
            financial_metrics = {}
            if utility_data:
                # Extract utility rate
                rate = utility_data.get('residential', 0.12)  # $/kWh
                
                # Annual savings
                annual_savings = annual_production * rate
                
                # System cost (assuming $3 per watt)
                system_cost = system_size * 1000 * 3  # $3000 per kW
                
                # Payback period
                payback_period = system_cost / annual_savings if annual_savings > 0 else 0
                
                financial_metrics = {
                    'annual_savings': annual_savings,
                    'system_cost': system_cost,
                    'payback_period': payback_period
                }
            
            return {
                'system_size': system_size,
                'annual_production': annual_production,
                'num_panels': num_panels,
                **financial_metrics
            }
            
        except Exception as e:
            logger.error(f"Error estimating solar potential: {e}")
            return {}
    
    def _mock_roof_data(self, latitude, longitude):
        """Generate mock roof data for testing."""
        # Generate realistic mock data
        
        # Roof area (typical single-family home)
        total_roof_area = random.uniform(1500, 3500)  # sq ft
        
        # Usable area (typically 40-80% of total)
        usable_percentage = random.uniform(0.4, 0.8)
        usable_roof_area = total_roof_area * usable_percentage
        
        # Orientation (south-facing is optimal)
        orientations = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        orientation_weights = [0.05, 0.1, 0.1, 0.15, 0.3, 0.15, 0.1, 0.05]  # South is most common
        primary_orientation = random.choices(orientations, weights=orientation_weights)[0]
        
        # Azimuth (180° is south)
        azimuth_map = {'N': 0, 'NE': 45, 'E': 90, 'SE': 135, 'S': 180, 'SW': 225, 'W': 270, 'NW': 315}
        azimuth = azimuth_map[primary_orientation] + random.uniform(-10, 10)
        
        # Pitch (typical roof pitch is 4/12 to 9/12, which is about 18-37 degrees)
        pitch = random.uniform(15, 40)
        
        # Shading (0-100%)
        shading_percentage = random.uniform(0, 30)
        
        # Estimated solar potential (based on orientation and shading)
        orientation_factor = 1.0 - (abs(azimuth - 180) / 180) * 0.4  # South (180°) is optimal
        shading_factor = 1.0 - (shading_percentage / 100)
        estimated_solar_potential = 1800 * orientation_factor * shading_factor  # Base value of 1800 kWh/kW/year
        
        return {
            'roof_type': random.choice(['asphalt shingle', 'metal', 'tile', 'flat']),
            'roof_age': random.randint(0, 25),
            'roof_condition': random.choice(['excellent', 'good', 'fair', 'poor']),
            'total_roof_area': total_roof_area,
            'usable_roof_area': usable_roof_area,
            'primary_orientation': primary_orientation,
            'azimuth': azimuth,
            'pitch': pitch,
            'shading_percentage': shading_percentage,
            'estimated_solar_potential': estimated_solar_potential,
            'data_source': 'mock_data'
        }
