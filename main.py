"""
Main module for integrating all components of the Solar Lead Generation System.
"""

import os
import logging
import json
import argparse
from datetime import datetime

# Import component modules
from database import Database
from property_data import PropertyDataCollector
from utility_data import UtilityDataCollector
from roof_data import RoofDataCollector
from skip_tracer import SkipTracer
from data_enrichment import DataEnrichmentPipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("solar_leads.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_config(config_file):
    """Load configuration from JSON file."""
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading config file: {e}")
        return {}

def main():
    """Main entry point for the application."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Solar Lead Generation System')
    parser.add_argument('--config', default='config.json', help='Path to configuration file')
    parser.add_argument('--import-csv', help='Import properties from CSV file')
    parser.add_argument('--zip-code', help='Process properties in a specific ZIP code')
    parser.add_argument('--address', help='Process a specific address')
    parser.add_argument('--min-score', type=int, default=60, help='Minimum lead score to include in results')
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Initialize database
    db_path = config.get('database', {}).get('path', 'solar_leads.db')
    db = Database(db_path)
    if not db.connect():
        logger.error("Failed to connect to database. Exiting.")
        return
    
    # Create tables if they don't exist
    db.create_tables()
    
    # Initialize data collectors with API keys from config
    api_keys = config.get('api_keys', {})
    property_collector = PropertyDataCollector(api_keys)
    utility_collector = UtilityDataCollector(api_keys)
    roof_collector = RoofDataCollector(api_keys)
    skip_tracer = SkipTracer(api_keys)
    
    # Initialize data enrichment pipeline
    pipeline = DataEnrichmentPipeline(
        db, property_collector, utility_collector, roof_collector, skip_tracer
    )
    
    # Process based on command line arguments
    if args.import_csv:
        logger.info(f"Importing properties from CSV: {args.import_csv}")
        results = pipeline.import_and_process_csv(args.import_csv)
        logger.info(f"Processed {len(results)} properties from CSV")
    elif args.zip_code:
        logger.info(f"Processing properties in ZIP code: {args.zip_code}")
        properties = property_collector.fetch_properties_by_zip(args.zip_code)
        results = pipeline.batch_process_properties(properties)
        logger.info(f"Processed {len(results)} properties in ZIP code {args.zip_code}")
    elif args.address:
        # Parse address (simplified)
        parts = args.address.split(',')
        if len(parts) >= 3:
            address = parts[0].strip()
            city = parts[1].strip()
            state_zip = parts[2].strip().split()
            state = state_zip[0] if state_zip else ''
            zip_code = state_zip[1] if len(state_zip) > 1 else ''
            
            logger.info(f"Processing address: {address}, {city}, {state} {zip_code}")
            result = pipeline.process_property(address, city, state, zip_code)
            if result:
                logger.info(f"Successfully processed address with property ID: {result.get('property_id')}")
            else:
                logger.warning("Failed to process address")
        else:
            logger.error("Invalid address format. Use: 'Street Address, City, State ZIP'")
    else:
        logger.info("No specific action requested. Use --help for options.")
    
    # Close database connection
    db.close()

if __name__ == "__main__":
    main()
