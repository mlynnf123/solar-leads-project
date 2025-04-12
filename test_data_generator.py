"""
Test data generator for the Solar Lead Generation System.
Creates realistic sample data for testing the system.
"""

import logging
import random
import json
import os
import sqlite3
import csv
from datetime import datetime, timedelta
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TestDataGenerator:
    """Class to generate test data for the Solar Lead Generation System."""
    
    def __init__(self, config=None):
        """
        Initialize with optional configuration parameters.
        
        Args:
            config: Dictionary with configuration parameters
        """
        self.config = config or {}
        
        # Texas cities with coordinates and ZIP codes
        self.texas_cities = [
            {"name": "Austin", "lat": 30.2672, "lng": -97.7431, "zip_codes": ["78701", "78702", "78703", "78704", "78705"]},
            {"name": "Houston", "lat": 29.7604, "lng": -95.3698, "zip_codes": ["77001", "77002", "77003", "77004", "77005"]},
            {"name": "Dallas", "lat": 32.7767, "lng": -96.7970, "zip_codes": ["75201", "75202", "75203", "75204", "75205"]},
            {"name": "San Antonio", "lat": 29.4241, "lng": -98.4936, "zip_codes": ["78201", "78202", "78203", "78204", "78205"]},
            {"name": "Fort Worth", "lat": 32.7555, "lng": -97.3308, "zip_codes": ["76101", "76102", "76103", "76104", "76105"]},
            {"name": "El Paso", "lat": 31.7619, "lng": -106.4850, "zip_codes": ["79901", "79902", "79903", "79904", "79905"]}
        ]
        
        # Utility providers in Texas
        self.utility_providers = [
            {"name": "Austin Energy", "cities": ["Austin"], "rate": 0.12, "net_metering": True},
            {"name": "CenterPoint Energy", "cities": ["Houston"], "rate": 0.115, "net_metering": True},
            {"name": "Oncor Electric", "cities": ["Dallas", "Fort Worth"], "rate": 0.11, "net_metering": False},
            {"name": "CPS Energy", "cities": ["San Antonio"], "rate": 0.125, "net_metering": True},
            {"name": "El Paso Electric", "cities": ["El Paso"], "rate": 0.13, "net_metering": False}
        ]
        
        # Common street names
        self.street_names = [
            "Main", "Oak", "Pine", "Maple", "Cedar", "Elm", "Washington", "Lake", "Hill", 
            "River", "View", "Park", "Spring", "North", "South", "East", "West", "Center", 
            "Church", "Mill", "Walnut", "Ridge", "Valley", "Meadow", "Forest", "Sunset"
        ]
        
        # Street types
        self.street_types = ["St", "Ave", "Blvd", "Dr", "Ln", "Rd", "Way", "Pl", "Ct", "Ter"]
        
        # First names
        self.first_names = [
            "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles",
            "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen",
            "Jose", "Luis", "Carlos", "Juan", "Miguel", "Maria", "Ana", "Rosa", "Guadalupe", "Elena",
            "Wei", "Li", "Min", "Yan", "Ling", "Yong", "Jie", "Xin", "Hui", "Ming"
        ]
        
        # Last names
        self.last_names = [
            "Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor",
            "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson",
            "Rodriguez", "Hernandez", "Lopez", "Gonzalez", "Perez", "Sanchez", "Ramirez", "Torres", "Flores", "Rivera",
            "Wang", "Li", "Zhang", "Liu", "Chen", "Yang", "Huang", "Zhao", "Wu", "Zhou"
        ]
        
        # Email domains
        self.email_domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com", "icloud.com"]
        
        # Roof types
        self.roof_types = ["Asphalt Shingle", "Metal", "Tile", "Slate", "Flat/Built-Up"]
        
        # Roof orientations
        self.roof_orientations = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        
        # Roof conditions
        self.roof_conditions = ["excellent", "good", "fair", "poor", "very poor"]
        
        # Current date for reference
        self.current_date = datetime.now()
    
    def generate_properties(self, count=100, output_file=None):
        """
        Generate sample property data.
        
        Args:
            count: Number of properties to generate
            output_file: Optional file path to save the data
            
        Returns:
            List of property dictionaries
        """
        logger.info(f"Generating {count} sample properties")
        
        properties = []
        
        for i in range(count):
            # Select a random city
            city = random.choice(self.texas_cities)
            
            # Generate coordinates with some random variation
            lat_variation = random.uniform(-0.05, 0.05)
            lng_variation = random.uniform(-0.05, 0.05)
            latitude = city["lat"] + lat_variation
            longitude = city["lng"] + lng_variation
            
            # Generate address
            street_number = random.randint(100, 9999)
            street_name = random.choice(self.street_names)
            street_type = random.choice(self.street_types)
            zip_code = random.choice(city["zip_codes"])
            
            # Generate property characteristics
            year_built = random.randint(1950, 2020)
            square_footage = random.randint(1000, 4000)
            bedrooms = random.randint(2, 5)
            bathrooms = random.randint(1, 4)
            
            # Determine if it's a single-family home (90% chance)
            is_single_family = random.random() < 0.9
            
            # Determine if it's owner-occupied (80% chance)
            is_owner_occupied = random.random() < 0.8
            
            # Generate property value based on size, age, and location
            base_value = square_footage * 100
            age_factor = max(0.5, 1 - (self.current_date.year - year_built) / 100)
            location_factor = 1.0
            if city["name"] in ["Austin", "Dallas"]:
                location_factor = 1.3
            elif city["name"] in ["Houston", "San Antonio"]:
                location_factor = 1.1
            
            property_value = int(base_value * age_factor * location_factor)
            
            # Generate a property ID
            property_id = f"PROP-{i+1:06d}"
            
            # Create property dictionary
            property_data = {
                "property_id": property_id,
                "address_line_1": f"{street_number} {street_name} {street_type}",
                "city": city["name"],
                "state": "TX",
                "zip_code": zip_code,
                "latitude": latitude,
                "longitude": longitude,
                "year_built": year_built,
                "square_footage": square_footage,
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "property_type": "Single-Family" if is_single_family else "Multi-Family",
                "is_owner_occupied": is_owner_occupied,
                "property_value": property_value,
                "has_solar_permit": random.random() < 0.05,  # 5% chance of having a solar permit
                "last_sale_date": (self.current_date - timedelta(days=random.randint(30, 3650))).strftime("%Y-%m-%d")
            }
            
            properties.append(property_data)
        
        # Save to file if specified
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(properties, f, indent=2)
            logger.info(f"Saved {count} properties to {output_file}")
        
        return properties
    
    def generate_homeowners(self, properties, output_file=None):
        """
        Generate sample homeowner data for properties.
        
        Args:
            properties: List of property dictionaries
            output_file: Optional file path to save the data
            
        Returns:
            List of homeowner dictionaries
        """
        logger.info(f"Generating homeowner data for {len(properties)} properties")
        
        homeowners = []
        
        for property_data in properties:
            # Skip if not owner-occupied
            if not property_data.get("is_owner_occupied", True):
                continue
            
            # Generate homeowner name
            first_name = random.choice(self.first_names)
            last_name = random.choice(self.last_names)
            
            # Generate contact information
            phone = f"({random.randint(200, 999)}) {random.randint(200, 999)}-{random.randint(1000, 9999)}"
            email_domain = random.choice(self.email_domains)
            email = f"{first_name.lower()}.{last_name.lower()}@{email_domain}"
            
            # Calculate length of ownership based on last sale date
            last_sale_date = datetime.strptime(property_data["last_sale_date"], "%Y-%m-%d")
            ownership_years = (self.current_date - last_sale_date).days / 365
            
            # Determine if on do-not-call list (10% chance)
            do_not_call = random.random() < 0.1
            
            # Create homeowner dictionary
            homeowner_data = {
                "property_id": property_data["property_id"],
                "first_name": first_name,
                "last_name": last_name,
                "full_name": f"{first_name} {last_name}",
                "phone": phone,
                "email": email,
                "ownership_years": round(ownership_years, 1),
                "do_not_call": do_not_call
            }
            
            homeowners.append(homeowner_data)
        
        # Save to file if specified
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(homeowners, f, indent=2)
            logger.info(f"Saved {len(homeowners)} homeowners to {output_file}")
        
        return homeowners
    
    def generate_roof_data(self, properties, output_file=None):
        """
        Generate sample roof data for properties.
        
        Args:
            properties: List of property dictionaries
            output_file: Optional file path to save the data
            
        Returns:
            List of roof data dictionaries
        """
        logger.info(f"Generating roof data for {len(properties)} properties")
        
        roof_data_list = []
        
        for property_data in properties:
            # Generate roof characteristics
            roof_type = random.choice(self.roof_types)
            
            # Determine roof age (typically younger than the house)
            property_age = self.current_date.year - property_data["year_built"]
            roof_age = min(property_age, random.randint(0, 25))
            
            # Calculate total roof area based on square footage
            total_roof_area = property_data["square_footage"] * random.uniform(1.1, 1.4)
            
            # South-facing roofs are more common in newer homes
            if property_data["year_built"] > 2000:
                orientation_weights = [0.05, 0.05, 0.05, 0.15, 0.4, 0.15, 0.05, 0.1]  # Higher weight for South
            else:
                orientation_weights = [0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125]  # Equal weights
            
            primary_orientation = random.choices(self.roof_orientations, weights=orientation_weights, k=1)[0]
            
            # Convert orientation to azimuth
            orientation_to_azimuth = {
                "N": 0, "NE": 45, "E": 90, "SE": 135, 
                "S": 180, "SW": 225, "W": 270, "NW": 315
            }
            azimuth = orientation_to_azimuth[primary_orientation] + random.randint(-10, 10)
            
            # Generate pitch (steeper in northern areas)
            if property_data["city"] in ["Dallas", "Fort Worth"]:
                pitch = random.randint(20, 40)
            else:
                pitch = random.randint(15, 30)
            
            # Calculate usable area (less for older roofs and non-south facing)
            usable_factor = 0.7  # Base factor
            if primary_orientation in ["S", "SE", "SW"]:
                usable_factor += 0.1
            if roof_age < 10:
                usable_factor += 0.1
            
            usable_roof_area = total_roof_area * usable_factor
            
            # Generate shading percentage (higher for older neighborhoods)
            if property_data["year_built"] < 1980:
                shading_percentage = random.randint(10, 40)
            else:
                shading_percentage = random.randint(5, 25)
            
            # Determine roof condition based on age
            if roof_age < 3:
                condition = "excellent"
            elif roof_age < 8:
                condition = "good"
            elif roof_age < 15:
                condition = "fair"
            elif roof_age < 20:
                condition = "poor"
            else:
                condition = "very poor"
            
            # Create roof data dictionary
            roof_data = {
                "property_id": property_data["property_id"],
                "roof_type": roof_type,
                "roof_age": roof_age,
                "total_roof_area": round(total_roof_area),
                "usable_roof_area": round(usable_roof_area),
                "primary_orientation": primary_orientation,
                "azimuth": azimuth,
                "pitch": pitch,
                "shading_percentage": shading_percentage,
                "roof_condition": condition
            }
            
            roof_data_list.append(roof_data)
        
        # Save to file if specified
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(roof_data_list, f, indent=2)
            logger.info(f"Saved {len(roof_data_list)} roof data records to {output_file}")
        
        return roof_data_list
    
    def generate_utility_data(self, properties, output_file=None):
        """
        Generate sample utility data for properties.
        
        Args:
            properties: List of property dictionaries
            output_file: Optional file path to save the data
            
        Returns:
            List of utility data dictionaries
        """
        logger.info(f"Generating utility data for {len(properties)} properties")
        
        utility_data_list = []
        
        for property_data in properties:
            # Find the utility provider for this city
            city = property_data["city"]
            provider = None
            
            for util in self.utility_providers:
                if city in util["cities"]:
                    provider = util
                    break
            
            # If no specific provider found, use a random one
            if not provider:
                provider = random.choice(self.utility_providers)
            
            # Calculate base rate with some variation
            base_rate = provider["rate"] * random.uniform(0.95, 1.05)
            
            # Calculate estimated monthly bill based on property characteristics
            # Larger and older homes have higher bills
            base_bill = property_data["square_footage"] * 0.1
            age_factor = 1 + max(0, (self.current_date.year - property_data["year_built"] - 10) / 100)
            
            # Seasonal factors (assuming current month)
            month = self.current_date.month
            if month in [6, 7, 8, 9]:  # Summer months in Texas
                seasonal_factor = 1.3
            elif month in [12, 1, 2]:  # Winter months
                seasonal_factor = 1.1
            else: 
(Content truncated due to size limit. Use line ranges to read in chunks)