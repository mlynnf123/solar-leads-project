"""
Integration module for the lead scoring components of the Solar Lead Generation System.
Combines bill estimation, roof analysis, and lead scoring into a unified workflow.
"""

import logging
from datetime import datetime
import json
import os

from src.lead_scoring import LeadScoringEngine
from src.bill_estimator import BillEstimator
from src.roof_analyzer import RoofAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LeadScoringService:
    """Class to integrate and manage all lead scoring components."""
    
    def __init__(self, config_file=None):
        """
        Initialize with optional configuration file.
        
        Args:
            config_file: Path to JSON configuration file
        """
        # Load configuration if provided
        self.config = {}
        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    self.config = json.load(f)
                logger.info(f"Loaded configuration from {config_file}")
            except Exception as e:
                logger.error(f"Error loading configuration: {e}")
        
        # Initialize component engines
        self.lead_engine = LeadScoringEngine(self.config.get('lead_scoring', {}))
        self.bill_estimator = BillEstimator(self.config.get('bill_estimation', {}))
        self.roof_analyzer = RoofAnalyzer(self.config.get('roof_analysis', {}))
        
        logger.info("Lead scoring service initialized")
    
    def score_lead(self, property_data, utility_data=None, roof_data=None, owner_data=None):
        """
        Score a potential lead using all available data.
        
        Args:
            property_data: Dictionary with property information
            utility_data: Optional dictionary with utility information
            roof_data: Optional dictionary with roof information
            owner_data: Optional dictionary with homeowner information
            
        Returns:
            Dictionary with comprehensive lead scoring results
        """
        logger.info(f"Scoring lead for property: {property_data.get('address_line_1', 'Unknown')}")
        
        try:
            # Step 1: Ensure we have utility data with bill estimate
            if not utility_data:
                utility_data = {}
            
            if 'estimated_monthly_bill' not in utility_data and property_data:
                monthly_bill = self.bill_estimator.estimate_monthly_bill(property_data, utility_data)
                utility_data['estimated_monthly_bill'] = monthly_bill
                
                # Also add annual profile
                annual_profile = self.bill_estimator.estimate_annual_bill_profile(property_data, utility_data)
                utility_data['annual_bill_profile'] = annual_profile
            
            # Step 2: Analyze roof if data is available
            roof_analysis = None
            if roof_data:
                roof_analysis = self.roof_analyzer.analyze_roof_suitability(roof_data)
                
                # Add system size estimate if we have energy usage data
                annual_usage = None
                if utility_data and 'annual_bill_profile' in utility_data:
                    annual_usage = utility_data['annual_bill_profile'].get('annual_total', 0) / utility_data.get('residential', 0.12)
                
                system_size_estimate = self.roof_analyzer.estimate_system_size(roof_data, annual_usage)
                roof_analysis['system_size_estimate'] = system_size_estimate
            
            # Step 3: Calculate lead score
            lead_score = self.lead_engine.calculate_overall_score(
                property_data, utility_data, roof_data, owner_data
            )
            
            # Step 4: Analyze bill factors if we have property data
            bill_analysis = None
            if property_data:
                bill_analysis = self.bill_estimator.analyze_bill_factors(property_data, utility_data)
            
            # Step 5: Combine all results into comprehensive report
            result = {
                'lead_score': lead_score,
                'roof_analysis': roof_analysis,
                'bill_analysis': bill_analysis,
                'timestamp': datetime.now().isoformat(),
                'data_completeness': {
                    'property_data': bool(property_data),
                    'utility_data': bool(utility_data),
                    'roof_data': bool(roof_data),
                    'owner_data': bool(owner_data)
                }
            }
            
            # Add summary for quick reference
            result['summary'] = self._generate_summary(result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error scoring lead: {e}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def batch_score_leads(self, leads_data):
        """
        Score multiple leads in batch.
        
        Args:
            leads_data: List of dictionaries, each containing property_data and optionally
                        utility_data, roof_data, and owner_data
            
        Returns:
            List of scoring results and batch analysis
        """
        logger.info(f"Batch scoring {len(leads_data)} leads")
        
        results = []
        for lead in leads_data:
            property_data = lead.get('property_data')
            utility_data = lead.get('utility_data')
            roof_data = lead.get('roof_data')
            owner_data = lead.get('owner_data')
            
            if property_data:
                result = self.score_lead(property_data, utility_data, roof_data, owner_data)
                results.append(result)
        
        # Analyze the distribution of scores
        scores_analysis = self.lead_engine.analyze_lead_distribution(
            [r['lead_score'] for r in results if 'lead_score' in r]
        )
        
        return {
            'results': results,
            'analysis': scores_analysis
        }
    
    def _generate_summary(self, result):
        """
        Generate a summary of the lead scoring result.
        
        Args:
            result: Full lead scoring result dictionary
            
        Returns:
            Dictionary with summary information
        """
        summary = {}
        
        # Extract lead score information
        if 'lead_score' in result:
            lead_score = result['lead_score']
            summary['overall_score'] = lead_score.get('overall_score', 0)
            summary['qualification'] = lead_score.get('qualification', 'unknown')
            
            # Extract component scores if available
            if 'component_scores' in lead_score:
                summary['component_scores'] = lead_score['component_scores']
        
        # Extract roof analysis if available
        if 'roof_analysis' in result and result['roof_analysis']:
            roof_analysis = result['roof_analysis']
            summary['roof_suitability'] = roof_analysis.get('suitability', 'unknown')
            
            # Extract system size estimate if available
            if 'system_size_estimate' in roof_analysis:
                system_size = roof_analysis['system_size_estimate']
                summary['recommended_system_size'] = system_size.get('recommended_system_size', 0)
                summary['estimated_annual_production'] = system_size.get('estimated_annual_production', 0)
        
        # Extract bill information if available
        if 'bill_analysis' in result and result['bill_analysis']:
            bill_analysis = result['bill_analysis']
            summary['estimated_monthly_bill'] = bill_analysis.get('base_bill', 0)
        
        return summary
    
    def save_result_to_file(self, result, filename):
        """
        Save lead scoring result to a JSON file.
        
        Args:
            result: Lead scoring result dictionary
            filename: Path to output file
            
        Returns:
            Boolean indicating success
        """
        try:
            with open(filename, 'w') as f:
                json.dump(result, f, indent=2)
            logger.info(f"Saved lead scoring result to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error saving result to file: {e}")
            return False
    
    def load_result_from_file(self, filename):
        """
        Load lead scoring result from a JSON file.
        
        Args:
            filename: Path to input file
            
        Returns:
            Lead scoring result dictionary or None if error
        """
        try:
            with open(filename, 'r') as f:
                result = json.load(f)
            logger.info(f"Loaded lead scoring result from {filename}")
            return result
        except Exception as e:
            logger.error(f"Error loading result from file: {e}")
            return None
