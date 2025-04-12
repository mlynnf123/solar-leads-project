"""
Roof suitability analysis module for the Solar Lead Generation System.
Implements algorithms for evaluating roof characteristics for solar installation.
"""

import logging
import numpy as np
from datetime import datetime
import math

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RoofAnalyzer:
    """Class to analyze roof characteristics for solar suitability."""
    
    def __init__(self, config=None):
        """
        Initialize with optional configuration parameters.
        
        Args:
            config: Dictionary with configuration parameters
        """
        self.config = config or {}
        
        # Default weights for different roof factors
        self.weights = self.config.get('weights', {
            'orientation': 0.35,    # 35% weight for orientation
            'area': 0.25,           # 25% weight for usable area
            'shading': 0.20,        # 20% weight for shading
            'pitch': 0.10,          # 10% weight for roof pitch
            'condition': 0.10       # 10% weight for roof condition
        })
        
        # Minimum requirements for solar installation
        self.min_requirements = self.config.get('min_requirements', {
            'usable_area': 400,     # Minimum usable roof area (sq ft)
            'max_shading': 40,      # Maximum acceptable shading percentage
        })
        
        # Optimal values for Texas
        self.optimal_values = self.config.get('optimal_values', {
            'azimuth': 180,         # South-facing (180°) is optimal
            'pitch': 25,            # ~25° pitch is optimal for Texas
        })
    
    def analyze_roof_suitability(self, roof_data):
        """
        Analyze roof suitability for solar installation.
        
        Args:
            roof_data: Dictionary with roof information
            
        Returns:
            Dictionary with suitability scores and analysis
        """
        logger.info(f"Analyzing roof suitability")
        
        if not roof_data:
            return {
                'overall_score': 0,
                'message': 'No roof data available'
            }
        
        try:
            # Calculate component scores
            orientation_score = self.calculate_orientation_score(roof_data)
            area_score = self.calculate_area_score(roof_data)
            shading_score = self.calculate_shading_score(roof_data)
            pitch_score = self.calculate_pitch_score(roof_data)
            condition_score = self.calculate_condition_score(roof_data)
            
            # Check if any component scores disqualify the roof
            if area_score == 0 or shading_score == 0:
                overall_score = 0
                suitability = "unsuitable"
                message = "Roof does not meet minimum requirements for solar installation"
            else:
                # Calculate weighted overall score
                overall_score = (
                    orientation_score * self.weights['orientation'] +
                    area_score * self.weights['area'] +
                    shading_score * self.weights['shading'] +
                    pitch_score * self.weights['pitch'] +
                    condition_score * self.weights['condition']
                )
                
                # Determine suitability category
                if overall_score >= 80:
                    suitability = "excellent"
                    message = "Roof is excellent for solar installation"
                elif overall_score >= 65:
                    suitability = "good"
                    message = "Roof is well-suited for solar installation"
                elif overall_score >= 50:
                    suitability = "average"
                    message = "Roof is acceptable for solar installation"
                elif overall_score >= 35:
                    suitability = "poor"
                    message = "Roof has significant limitations for solar installation"
                else:
                    suitability = "unsuitable"
                    message = "Roof is not recommended for solar installation"
            
            # Return comprehensive analysis results
            return {
                'overall_score': round(overall_score),
                'suitability': suitability,
                'message': message,
                'component_scores': {
                    'orientation': round(orientation_score),
                    'area': round(area_score),
                    'shading': round(shading_score),
                    'pitch': round(pitch_score),
                    'condition': round(condition_score)
                },
                'weights': self.weights,
                'recommendations': self.generate_recommendations(roof_data, overall_score),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing roof suitability: {e}")
            return {
                'overall_score': 0,
                'error': str(e)
            }
    
    def calculate_orientation_score(self, roof_data):
        """
        Calculate score component based on roof orientation.
        
        Args:
            roof_data: Dictionary with roof information
            
        Returns:
            Score from 0-100 for this component
        """
        # Check if we have azimuth or orientation
        if 'azimuth' in roof_data:
            azimuth = roof_data['azimuth']
            
            # Calculate deviation from optimal (180° is south-facing)
            optimal_azimuth = self.optimal_values['azimuth']
            deviation = abs(azimuth - optimal_azimuth)
            
            # Normalize deviation to 0-180 range (180° is worst case)
            if deviation > 180:
                deviation = 360 - deviation
            
            # Convert to score (0-100)
            # 0° deviation = 100 points
            # 90° deviation = 50 points
            # 180° deviation = 0 points
            score = 100 - (deviation / 180) * 100
            
            return score
            
        elif 'primary_orientation' in roof_data:
            # Score based on cardinal direction
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
            
            return orientation_scores.get(orientation, 50)
        
        else:
            # No orientation data
            return 50  # Neutral score
    
    def calculate_area_score(self, roof_data):
        """
        Calculate score component based on usable roof area.
        
        Args:
            roof_data: Dictionary with roof information
            
        Returns:
            Score from 0-100 for this component
        """
        # Check if we have usable area
        if 'usable_roof_area' in roof_data:
            usable_area = roof_data['usable_roof_area']
            min_area = self.min_requirements['usable_area']
            
            # Check minimum requirement
            if usable_area < min_area:
                return 0  # Disqualify if too small
            
            # Score increases with usable area
            # 400 sq ft = 50 points (minimum qualifying)
            # 800 sq ft = 80 points
            # 1200+ sq ft = 100 points
            
            if usable_area >= 1200:
                return 100
            elif usable_area >= 800:
                return 80 + (usable_area - 800) * 20 / 400
            else:
                return 50 + (usable_area - min_area) * 30 / (800 - min_area)
        
        elif 'total_roof_area' in roof_data:
            # Estimate usable area as 60% of total area
            total_area = roof_data['total_roof_area']
            estimated_usable = total_area * 0.6
            
            # Use the same scoring logic
            min_area = self.min_requirements['usable_area']
            
            if estimated_usable < min_area:
                return 0
            elif estimated_usable >= 1200:
                return 100
            elif estimated_usable >= 800:
                return 80 + (estimated_usable - 800) * 20 / 400
            else:
                return 50 + (estimated_usable - min_area) * 30 / (800 - min_area)
        
        else:
            # No area data
            return 0  # Cannot qualify without area data
    
    def calculate_shading_score(self, roof_data):
        """
        Calculate score component based on roof shading.
        
        Args:
            roof_data: Dictionary with roof information
            
        Returns:
            Score from 0-100 for this component
        """
        # Check if we have shading data
        if 'shading_percentage' in roof_data:
            shading_pct = roof_data['shading_percentage']
            max_shading = self.min_requirements['max_shading']
            
            # Check maximum requirement
            if shading_pct > max_shading:
                return 0  # Disqualify if too shaded
            
            # Score decreases with shading
            # 0% shading = 100 points
            # 20% shading = 50 points
            # 40% shading = 0 points
            
            return 100 - (shading_pct / max_shading) * 100
        
        else:
            # No shading data
            return 50  # Neutral score
    
    def calculate_pitch_score(self, roof_data):
        """
        Calculate score component based on roof pitch.
        
        Args:
            roof_data: Dictionary with roof information
            
        Returns:
            Score from 0-100 for this component
        """
        # Check if we have pitch data
        if 'pitch' in roof_data:
            pitch = roof_data['pitch']
            optimal_pitch = self.optimal_values['pitch']
            
            # Calculate deviation from optimal
            deviation = abs(pitch - optimal_pitch)
            
            # Score decreases with deviation
            # 0° deviation = 100 points
            # 15° deviation = 50 points
            # 30°+ deviation = 0 points
            
            if deviation >= 30:
                return 0
            else:
                return 100 - (deviation / 30) * 100
        
        else:
            # No pitch data
            return 50  # Neutral score
    
    def calculate_condition_score(self, roof_data):
        """
        Calculate score component based on roof condition.
        
        Args:
            roof_data: Dictionary with roof information
            
        Returns:
            Score from 0-100 for this component
        """
        # Check if we have condition data
        if 'roof_condition' in roof_data:
            condition = roof_data['roof_condition'].lower()
            
            # Score based on condition
            condition_scores = {
                'excellent': 100,
                'good': 80,
                'fair': 60,
                'poor': 30,
                'very poor': 10
            }
            
            return condition_scores.get(condition, 50)
        
        # Check if we have age data as a proxy for condition
        elif 'roof_age' in roof_data:
            age = roof_data['roof_age']
            
            # Score based on age
            if age <= 2:
                return 100  # New roof
            elif age <= 5:
                return 90
            elif age <= 10:
                return 75
            elif age <= 15:
                return 60
            elif age <= 20:
                return 40
            else:
                return 20  # Old roof
        
        else:
            # No condition data
            return 50  # Neutral score
    
    def generate_recommendations(self, roof_data, overall_score):
        """
        Generate recommendations based on roof analysis.
        
        Args:
            roof_data: Dictionary with roof information
            overall_score: Overall suitability score
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        # Check if roof is suitable at all
        if overall_score < 35:
            recommendations.append("This roof is not well-suited for solar installation. Consider alternative options.")
            return recommendations
        
        # Orientation recommendations
        if 'azimuth' in roof_data or 'primary_orientation' in roof_data:
            orientation_score = self.calculate_orientation_score(roof_data)
            
            if orientation_score < 50:
                recommendations.append("Roof orientation is not ideal. Consider panel tilt optimization to improve energy production.")
            
            if 'primary_orientation' in roof_data:
                orientation = roof_data['primary_orientation']
                if orientation in ['E', 'W']:
                    recommendations.append("East/West orientation will produce less energy than south-facing installations. Consider high-efficiency panels.")
                elif orientation in ['NE', 'NW', 'N']:
                    recommendations.append("Northern orientation significantly reduces solar production. Consider ground-mounted system if land is available.")
        
        # Area recommendations
        if 'usable_roof_area' in roof_data:
            usable_area = roof_data['usable_roof_area']
            
            # Estimate system size based on area
            # Typical solar panel is about 17-18 sq ft and produces about 300W
            panel_area = 17.5  # sq ft
            panel_power = 0.3  # kW
            
            # Number of panels that can fit on the roof
            num_panels = int(usable_area / panel_area)
            
            # System size in kW
            system_size = num_panels * panel_power
            
            if system_size < 5:
                recommendations.append(f"Limited roof area allows for approximately {system_size:.1f} kW system. Consider high-efficiency panels to maximize production.")
            elif system_size >= 10:
                recommendations.append(f"Large roof area can support a {system_size:.1f} kW system, which may exceed typical residential needs. Consider battery storage for excess production.")
            else:
                recommendations.append(f"Roof area can support approximately {system_size:.1f} kW system, which is well-suited for typical residential needs.")
        
        # Shading recommendations
        if 'shading_percentage' in roof_data:
            shading_pct = roof_data['shading_percentage']
            
            if shading_pct > 20:
                recommendations.append(f"Significant shading ({shading_pct}%) will reduce system performance. Consider tree trimming or microinverters/optimizers to mitigate shading impacts.")
            elif shading_pct > 10:
                recommendations.append(f"Moderate shading ({shading_pct}%) may affect system performance. Microinverters or power optimizers are recommended.")
        
        # Pitch recommendations
        if 'pitch' in roof_data:
            pitch = roof_data['pitch']
            
            if pitch < 10:
                recommendations.append(f"Low roof pitch ({pitch}°) may lead to debris accumulation and reduced self-cleaning. Consider more frequent maintenance.")
            elif pitch > 40:
                recommendations.append(f"Steep roof pitch (
(Content truncated due to size limit. Use line ranges to read in chunks)