"""
Test script for the Solar Lead Generation System.
Validates the system's functionality with sample data.
"""

import logging
import os
import sys
import json
import sqlite3
from datetime import datetime

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.test_data_generator import TestDataGenerator
from src.lead_scoring import LeadScoringEngine
from src.bill_estimator import BillEstimator
from src.roof_analyzer import RoofAnalyzer
from src.lead_scoring_service import LeadScoringService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SystemTester:
    """Class to test the Solar Lead Generation System."""
    
    def __init__(self, test_data_dir="test_data", db_file="solar_leads.db"):
        """
        Initialize the system tester.
        
        Args:
            test_data_dir: Directory to store test data
            db_file: Path to the SQLite database file
        """
        self.test_data_dir = test_data_dir
        self.db_file = db_file
        
        # Create test data directory if it doesn't exist
        if not os.path.exists(test_data_dir):
            os.makedirs(test_data_dir)
        
        # Initialize test data generator
        self.data_generator = TestDataGenerator()
        
        # Initialize lead scoring components
        self.lead_scoring_engine = LeadScoringEngine()
        self.bill_estimator = BillEstimator()
        self.roof_analyzer = RoofAnalyzer()
        self.lead_scoring_service = LeadScoringService()
        
        logger.info("System tester initialized")
    
    def generate_test_data(self, count=100):
        """
        Generate test data for the system.
        
        Args:
            count: Number of properties to generate
            
        Returns:
            Dictionary with all generated data
        """
        logger.info(f"Generating {count} test records")
        
        # Generate all test data
        data = self.data_generator.generate_all_test_data(count, self.test_data_dir)
        
        # Create SQLite database
        self.data_generator.create_sqlite_database(data, os.path.join(self.test_data_dir, self.db_file))
        
        return data
    
    def test_bill_estimator(self, properties, utilities):
        """
        Test the bill estimator component.
        
        Args:
            properties: List of property dictionaries
            utilities: List of utility dictionaries
            
        Returns:
            Dictionary with test results
        """
        logger.info("Testing bill estimator component")
        
        results = {
            "total_tested": 0,
            "within_10_percent": 0,
            "within_20_percent": 0,
            "over_20_percent": 0,
            "examples": []
        }
        
        # Create lookup for utilities
        utility_lookup = {u["property_id"]: u for u in utilities}
        
        # Test a sample of properties
        sample_size = min(20, len(properties))
        sample_properties = properties[:sample_size]
        
        for prop in sample_properties:
            property_id = prop["property_id"]
            utility_data = utility_lookup.get(property_id)
            
            if utility_data:
                # Get the actual bill from test data
                actual_bill = utility_data["estimated_monthly_bill"]
                
                # Estimate bill using our algorithm
                estimated_bill = self.bill_estimator.estimate_monthly_bill(prop, utility_data)
                
                # Calculate percentage difference
                if actual_bill > 0:
                    percent_diff = abs(estimated_bill - actual_bill) / actual_bill * 100
                else:
                    percent_diff = 100
                
                # Categorize result
                results["total_tested"] += 1
                if percent_diff <= 10:
                    results["within_10_percent"] += 1
                elif percent_diff <= 20:
                    results["within_20_percent"] += 1
                else:
                    results["over_20_percent"] += 1
                
                # Add example
                if len(results["examples"]) < 5:
                    results["examples"].append({
                        "property_id": property_id,
                        "address": prop["address_line_1"],
                        "square_footage": prop["square_footage"],
                        "year_built": prop["year_built"],
                        "actual_bill": actual_bill,
                        "estimated_bill": estimated_bill,
                        "percent_diff": round(percent_diff, 2)
                    })
        
        # Calculate accuracy percentages
        if results["total_tested"] > 0:
            results["accuracy_10_percent"] = round(results["within_10_percent"] / results["total_tested"] * 100, 2)
            results["accuracy_20_percent"] = round((results["within_10_percent"] + results["within_20_percent"]) / results["total_tested"] * 100, 2)
        
        return results
    
    def test_roof_analyzer(self, properties, roofs):
        """
        Test the roof analyzer component.
        
        Args:
            properties: List of property dictionaries
            roofs: List of roof dictionaries
            
        Returns:
            Dictionary with test results
        """
        logger.info("Testing roof analyzer component")
        
        results = {
            "total_tested": 0,
            "excellent_count": 0,
            "good_count": 0,
            "average_count": 0,
            "poor_count": 0,
            "unsuitable_count": 0,
            "examples": []
        }
        
        # Create lookup for properties
        property_lookup = {p["property_id"]: p for p in properties}
        
        # Test all roofs
        for roof in roofs:
            property_id = roof["property_id"]
            property_data = property_lookup.get(property_id)
            
            if property_data:
                # Analyze roof suitability
                analysis = self.roof_analyzer.analyze_roof_suitability(roof)
                
                # Categorize result
                results["total_tested"] += 1
                suitability = analysis.get("suitability", "unknown")
                
                if suitability == "excellent":
                    results["excellent_count"] += 1
                elif suitability == "good":
                    results["good_count"] += 1
                elif suitability == "average":
                    results["average_count"] += 1
                elif suitability == "poor":
                    results["poor_count"] += 1
                elif suitability == "unsuitable":
                    results["unsuitable_count"] += 1
                
                # Add example
                if len(results["examples"]) < 5:
                    results["examples"].append({
                        "property_id": property_id,
                        "address": property_data["address_line_1"],
                        "roof_type": roof["roof_type"],
                        "orientation": roof["primary_orientation"],
                        "usable_area": roof["usable_roof_area"],
                        "suitability": suitability,
                        "overall_score": analysis.get("overall_score", 0),
                        "recommendations": analysis.get("recommendations", [])
                    })
        
        # Calculate percentages
        if results["total_tested"] > 0:
            results["excellent_percent"] = round(results["excellent_count"] / results["total_tested"] * 100, 2)
            results["good_percent"] = round(results["good_count"] / results["total_tested"] * 100, 2)
            results["average_percent"] = round(results["average_count"] / results["total_tested"] * 100, 2)
            results["poor_percent"] = round(results["poor_count"] / results["total_tested"] * 100, 2)
            results["unsuitable_percent"] = round(results["unsuitable_count"] / results["total_tested"] * 100, 2)
        
        return results
    
    def test_lead_scoring(self, properties, homeowners, roofs, utilities):
        """
        Test the lead scoring component.
        
        Args:
            properties: List of property dictionaries
            homeowners: List of homeowner dictionaries
            roofs: List of roof dictionaries
            utilities: List of utility dictionaries
            
        Returns:
            Dictionary with test results
        """
        logger.info("Testing lead scoring component")
        
        results = {
            "total_tested": 0,
            "excellent_count": 0,
            "good_count": 0,
            "average_count": 0,
            "poor_count": 0,
            "unsuitable_count": 0,
            "examples": [],
            "score_distribution": {}
        }
        
        # Create lookups
        property_lookup = {p["property_id"]: p for p in properties}
        homeowner_lookup = {h["property_id"]: h for h in homeowners}
        roof_lookup = {r["property_id"]: r for r in roofs}
        utility_lookup = {u["property_id"]: u for u in utilities}
        
        # Prepare data for lead scoring
        leads_data = []
        
        for property_id, prop in property_lookup.items():
            # Skip properties with solar permits
            if prop.get("has_solar_permit", False):
                continue
                
            # Skip non-owner-occupied properties
            if not prop.get("is_owner_occupied", True):
                continue
                
            homeowner = homeowner_lookup.get(property_id)
            roof = roof_lookup.get(property_id)
            utility = utility_lookup.get(property_id)
            
            if homeowner and roof and utility:
                leads_data.append({
                    "property_data": prop,
                    "owner_data": homeowner,
                    "roof_data": roof,
                    "utility_data": utility
                })
        
        # Score leads in batch
        batch_results = self.lead_scoring_service.batch_score_leads(leads_data)
        
        # Process results
        results["total_tested"] = len(batch_results["results"])
        
        for lead_result in batch_results["results"]:
            if "lead_score" in lead_result:
                score = lead_result["lead_score"].get("overall_score", 0)
                qualification = lead_result["lead_score"].get("qualification", "unknown")
                
                # Count by qualification
                if qualification == "excellent":
                    results["excellent_count"] += 1
                elif qualification == "good":
                    results["good_count"] += 1
                elif qualification == "average":
                    results["average_count"] += 1
                elif qualification == "poor":
                    results["poor_count"] += 1
                elif qualification == "unsuitable":
                    results["unsuitable_count"] += 1
                
                # Track score distribution
                score_range = f"{(score // 10) * 10}-{(score // 10) * 10 + 9}"
                results["score_distribution"][score_range] = results["score_distribution"].get(score_range, 0) + 1
                
                # Add example
                if len(results["examples"]) < 10:
                    property_id = lead_result["lead_score"].get("property_id", "unknown")
                    prop = property_lookup.get(property_id, {})
                    utility = utility_lookup.get(property_id, {})
                    
                    results["examples"].append({
                        "property_id": property_id,
                        "address": prop.get("address_line_1", "Unknown"),
                        "city": prop.get("city", "Unknown"),
                        "overall_score": score,
                        "qualification": qualification,
                        "estimated_bill": utility.get("estimated_monthly_bill", 0),
                        "component_scores": lead_result["lead_score"].get("component_scores", {})
                    })
        
        # Calculate percentages
        if results["total_tested"] > 0:
            results["excellent_percent"] = round(results["excellent_count"] / results["total_tested"] * 100, 2)
            results["good_percent"] = round(results["good_count"] / results["total_tested"] * 100, 2)
            results["average_percent"] = round(results["average_count"] / results["total_tested"] * 100, 2)
            results["poor_percent"] = round(results["poor_count"] / results["total_tested"] * 100, 2)
            results["unsuitable_percent"] = round(results["unsuitable_count"] / results["total_tested"] * 100, 2)
        
        # Add score distribution analysis
        results["distribution_analysis"] = batch_results["analysis"]
        
        return results
    
    def test_database_integration(self):
        """
        Test database integration by performing queries.
        
        Returns:
            Dictionary with test results
        """
        logger.info("Testing database integration")
        
        results = {
            "queries_tested": 0,
            "queries_passed": 0,
            "examples": []
        }
        
        db_path = os.path.join(self.test_data_dir, self.db_file)
        
        try:
            # Connect to database
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Test query 1: Count properties by city
            cursor.execute('''
            SELECT city, COUNT(*) as count
            FROM properties
            GROUP BY city
            ORDER BY count DESC
            ''')
            query1_result = cursor.fetchall()
            
            results["queries_tested"] += 1
            if query1_result and len(query1_result) > 0:
                results["queries_passed"] += 1
                results["examples"].append({
                    "query": "Count properties by city",
                    "result": [{"city": city, "count": count} for city, count in query1_result]
                })
            
            # Test query 2: Find properties with high bills
            cursor.execute('''
            SELECT p.property_id, p.address_line_1, p.city, u.estimated_monthly_bill
            FROM properties p
            JOIN utilities u ON p.property_id = u.property_id
            WHERE u.estimated_monthly_bill > 150
            ORDER BY u.estimated_monthly_bill DESC
            LIMIT 5
            ''')
            query2_result = cursor.fetchall()
            
            results["queries_tested"] += 1
            if query2_result and len(query2_result) > 0:
                results["queries_passed"] += 1
                results["examples"].append({
                    "query": "Find properties with high bills",
                    "result": [{"property_id": pid, "address": addr, "city": city, "bill": bill} 
                              for pid, addr, city, bill in query2_result]
                })
            
            # Test query 3: Find south-facing roofs
            cursor.execute('''
            SELECT p.property_id, p.address_line_1, r.primary_orientation, r.usable_roof_area
            FROM properties p
            JOIN roofs r ON p.property_id = r.property_id
            WHERE r.primary_orientation IN ('S', 'SE', 'SW')
            AND p.has_solar_permit = 0
            LIMIT 5
            ''')
            query3_result = cursor.fetchall()
            
            results["queries_tested"] += 1
            if query3_result and len(quer
(Content truncated due to size limit. Use line ranges to read in chunks)