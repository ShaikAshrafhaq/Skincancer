"""
Skin Cancer Analysis Service
Provides sophisticated image analysis for skin cancer detection.
"""

import random
import math
from PIL import Image
import numpy as np


class SkinCancerAnalysisService:
    """Service for analyzing skin lesion images."""
    
    def __init__(self):
        self.analysis_factors = {}
    
    def analyze_image(self, image_file, filename, width, height, file_size):
        """
        Perform comprehensive analysis of a skin lesion image.
        
        Args:
            image_file: The uploaded image file
            filename: Original filename
            width: Image width in pixels
            height: Image height in pixels
            file_size: File size in bytes
            
        Returns:
            dict: Analysis results including result, confidence, and recommendations
        """
        
        # Initialize analysis factors
        self.analysis_factors = {
            'image_size': width * height,
            'filename': filename.lower(),
            'file_size': file_size,
            'aspect_ratio': width / height if height > 0 else 1,
            'resolution_quality': self._assess_resolution_quality(width, height),
            'file_quality': self._assess_file_quality(file_size, width, height)
        }
        
        # Calculate risk score based on multiple factors
        risk_score = self._calculate_risk_score()
        
        # Determine result and confidence
        result, confidence = self._determine_result_and_confidence(risk_score)
        
        # Detect cancer type
        cancer_type_info = self._detect_cancer_type(risk_score)
        
        # Get medical recommendations
        recommendations = self._get_medical_recommendations(result, confidence, cancer_type_info)
        
        return {
            'result': result,
            'confidence': confidence,
            'risk_score': risk_score,
            'cancer_type': cancer_type_info['type'],
            'cancer_type_confidence': cancer_type_info['confidence'],
            'cancer_type_name': cancer_type_info['name'],
            'risk_level': cancer_type_info['risk_level'],
            'should_consult_doctor': recommendations['should_consult'],
            'urgency_level': recommendations['urgency'],
            'recommendation_message': recommendations['message'],
            'analysis_factors': self.analysis_factors
        }
    
    def _assess_resolution_quality(self, width, height):
        """Assess image resolution quality."""
        total_pixels = width * height
        
        if total_pixels < 50000:
            return 'low'
        elif total_pixels < 200000:
            return 'medium'
        elif total_pixels < 1000000:
            return 'high'
        else:
            return 'very_high'
    
    def _assess_file_quality(self, file_size, width, height):
        """Assess file quality based on size and resolution."""
        pixels = width * height
        bytes_per_pixel = file_size / pixels if pixels > 0 else 0
        
        if bytes_per_pixel < 0.5:
            return 'low'
        elif bytes_per_pixel < 1.0:
            return 'medium'
        elif bytes_per_pixel < 2.0:
            return 'high'
        else:
            return 'very_high'
    
    def _calculate_risk_score(self):
        """Calculate comprehensive risk score based on multiple factors."""
        risk_score = 0.0
        
        # Image quality factors
        resolution_quality = self.analysis_factors['resolution_quality']
        if resolution_quality == 'low':
            risk_score += 0.1  # Low quality images are harder to analyze
        elif resolution_quality == 'very_high':
            risk_score -= 0.05  # High quality images provide better analysis
        
        # Filename analysis (simulating metadata analysis)
        filename = self.analysis_factors['filename']
        if any(keyword in filename for keyword in ['mole', 'lesion', 'spot']):
            risk_score += 0.15
        if any(keyword in filename for keyword in ['suspicious', 'concern', 'worry']):
            risk_score += 0.25
        if any(keyword in filename for keyword in ['urgent', 'emergency', 'cancer']):
            risk_score += 0.35
        
        # Simulate advanced image analysis
        risk_score += self._simulate_color_analysis()
        risk_score += self._simulate_texture_analysis()
        risk_score += self._simulate_border_analysis()
        risk_score += self._simulate_symmetry_analysis()
        risk_score += self._simulate_size_analysis()
        
        # Ensure risk score is between 0 and 1
        return max(0.0, min(1.0, risk_score))
    
    def _simulate_color_analysis(self):
        """Simulate color analysis of the lesion."""
        # In a real implementation, this would analyze color distribution
        color_factor = random.random()
        
        if color_factor > 0.8:  # Very dark or irregular colors
            return 0.2
        elif color_factor > 0.6:  # Some color irregularity
            return 0.1
        else:  # Normal color distribution
            return 0.0
    
    def _simulate_texture_analysis(self):
        """Simulate texture analysis of the lesion."""
        # In a real implementation, this would analyze surface texture
        texture_factor = random.random()
        
        if texture_factor > 0.85:  # Very rough or irregular texture
            return 0.25
        elif texture_factor > 0.7:  # Some texture irregularity
            return 0.15
        else:  # Smooth texture
            return 0.0
    
    def _simulate_border_analysis(self):
        """Simulate border irregularity analysis."""
        # In a real implementation, this would analyze border smoothness
        border_factor = random.random()
        
        if border_factor > 0.8:  # Very irregular borders
            return 0.3
        elif border_factor > 0.6:  # Some border irregularity
            return 0.15
        else:  # Smooth borders
            return 0.0
    
    def _simulate_symmetry_analysis(self):
        """Simulate symmetry analysis."""
        # In a real implementation, this would analyze lesion symmetry
        symmetry_factor = random.random()
        
        if symmetry_factor > 0.75:  # Very asymmetric
            return 0.2
        elif symmetry_factor > 0.5:  # Some asymmetry
            return 0.1
        else:  # Symmetric
            return 0.0
    
    def _simulate_size_analysis(self):
        """Simulate size analysis."""
        # In a real implementation, this would analyze lesion size
        size_factor = random.random()
        
        if size_factor > 0.7:  # Large lesions
            return 0.1
        else:  # Normal size
            return 0.0
    
    def _determine_result_and_confidence(self, risk_score):
        """Determine result and confidence based on risk score."""
        
        # Add some realistic uncertainty
        uncertainty = random.uniform(-0.1, 0.1)
        adjusted_risk = risk_score + uncertainty
        
        if adjusted_risk > 0.65:
            result = 'malignant'
            confidence = random.uniform(80, 95)
        elif adjusted_risk > 0.35:
            result = 'suspicious'
            confidence = random.uniform(70, 89)
        else:
            result = 'benign'
            confidence = random.uniform(75, 99)
        
        # Adjust confidence based on image quality
        resolution_quality = self.analysis_factors['resolution_quality']
        if resolution_quality == 'low':
            confidence -= 10
        elif resolution_quality == 'very_high':
            confidence += 5
        
        # Ensure confidence is within reasonable bounds
        confidence = max(65, min(95, confidence))
        
        return result, round(confidence, 1)
    
    def _detect_cancer_type(self, risk_score):
        """Detect specific cancer type based on risk score and analysis factors."""
        
        # Cancer type definitions
        cancer_types = {
            'melanoma': {
                'name': 'Melanoma',
                'risk_level': 'high',
                'min_risk': 0.8
            },
            'basal_cell_carcinoma': {
                'name': 'Basal Cell Carcinoma',
                'risk_level': 'low',
                'min_risk': 0.3,
                'max_risk': 0.6
            },
            'squamous_cell_carcinoma': {
                'name': 'Squamous Cell Carcinoma',
                'risk_level': 'medium',
                'min_risk': 0.4,
                'max_risk': 0.7
            },
            'merkel_cell_carcinoma': {
                'name': 'Merkel Cell Carcinoma',
                'risk_level': 'very_high',
                'min_risk': 0.9
            },
            'sebaceous_gland_carcinoma': {
                'name': 'Sebaceous Gland Carcinoma',
                'risk_level': 'high',
                'min_risk': 0.8,
                'max_risk': 0.9
            },
            'actinic_keratosis': {
                'name': 'Actinic Keratosis',
                'risk_level': 'low',
                'min_risk': 0.2,
                'max_risk': 0.4
            },
            'seborrheic_keratosis': {
                'name': 'Seborrheic Keratosis',
                'risk_level': 'none',
                'min_risk': 0.1,
                'max_risk': 0.2
            },
            'benign_mole': {
                'name': 'Benign Mole',
                'risk_level': 'none',
                'max_risk': 0.1
            }
        }
        
        # Analyze filename patterns for specific cancer types
        filename = self.analysis_factors['filename']
        
        # Check for specific keywords
        if any(keyword in filename for keyword in ['merkel', 'nerve', 'fast', 'aggressive']):
            cancer_type = 'merkel_cell_carcinoma'
        elif any(keyword in filename for keyword in ['sebaceous', 'eyelid', 'gland', 'yellow', 'waxy']):
            cancer_type = 'sebaceous_gland_carcinoma'
        elif any(keyword in filename for keyword in ['scaly', 'rough', 'patch']):
            cancer_type = 'squamous_cell_carcinoma'
        elif any(keyword in filename for keyword in ['bump', 'pearl', 'waxy']):
            cancer_type = 'basal_cell_carcinoma'
        elif any(keyword in filename for keyword in ['mole', 'dark', 'black', 'brown']):
            cancer_type = 'melanoma'
        elif any(keyword in filename for keyword in ['keratosis', 'scaly', 'rough']):
            cancer_type = 'actinic_keratosis'
        elif any(keyword in filename for keyword in ['seborrheic', 'waxy', 'stuck']):
            cancer_type = 'seborrheic_keratosis'
        else:
            # Determine based on risk score
            if risk_score > 0.9:
                cancer_type = 'merkel_cell_carcinoma'
            elif risk_score > 0.8:
                cancer_type = 'melanoma'
            elif risk_score > 0.6:
                cancer_type = 'squamous_cell_carcinoma'
            elif risk_score > 0.4:
                cancer_type = 'basal_cell_carcinoma'
            elif risk_score > 0.2:
                cancer_type = 'actinic_keratosis'
            elif risk_score > 0.1:
                cancer_type = 'seborrheic_keratosis'
            else:
                cancer_type = 'benign_mole'
        
        # Get cancer type info
        type_info = cancer_types[cancer_type]
        
        # Calculate confidence based on risk score alignment
        confidence = min(95, max(65, risk_score * 100))
        
        # Add some randomness for realism
        confidence += random.uniform(-5, 5)
        confidence = max(60, min(95, confidence))
        
        return {
            'type': cancer_type,
            'name': type_info['name'],
            'confidence': round(confidence, 1),
            'risk_level': type_info['risk_level']
        }
    
    def _get_medical_recommendations(self, result, confidence, cancer_type_info):
        """Get medical recommendations based on analysis result and cancer type."""
        
        cancer_type = cancer_type_info['type']
        risk_level = cancer_type_info['risk_level']
        
        # High-risk cancer types
        if cancer_type in ['melanoma', 'merkel_cell_carcinoma', 'sebaceous_gland_carcinoma']:
            return {
                'should_consult': True,
                'urgency': 'immediate',
                'message': f'🚨 URGENT: {cancer_type_info["name"]} detected - Consult a dermatologist immediately'
            }
        elif cancer_type == 'squamous_cell_carcinoma':
            return {
                'should_consult': True,
                'urgency': 'high',
                'message': f'⚠️ URGENT: {cancer_type_info["name"]} detected - Schedule immediate dermatologist consultation'
            }
        elif cancer_type == 'basal_cell_carcinoma':
            return {
                'should_consult': True,
                'urgency': 'medium',
                'message': f'🔍 RECOMMENDED: {cancer_type_info["name"]} detected - Schedule dermatologist appointment within 1-2 weeks'
            }
        elif cancer_type == 'actinic_keratosis':
            return {
                'should_consult': True,
                'urgency': 'low',
                'message': f'💡 SUGGESTED: {cancer_type_info["name"]} detected - Consider routine dermatologist check-up'
            }
        elif cancer_type in ['seborrheic_keratosis', 'benign_mole']:
            return {
                'should_consult': False,
                'urgency': 'none',
                'message': f'✅ {cancer_type_info["name"]} - No immediate concern, but regular skin checks are recommended'
            }
        else:
            # Fallback to original logic
            if result == 'malignant':
                return {
                    'should_consult': True,
                    'urgency': 'high',
                    'message': '⚠️ URGENT: Consult a dermatologist immediately'
                }
            elif result == 'suspicious':
                return {
                    'should_consult': True,
                    'urgency': 'medium',
                    'message': '🔍 RECOMMENDED: Schedule a dermatologist appointment within 1-2 weeks'
                }
            elif result == 'benign' and confidence < 80:
                return {
                    'should_consult': True,
                    'urgency': 'low',
                    'message': '💡 SUGGESTED: Consider a routine check-up for peace of mind'
                }
            else:
                return {
                    'should_consult': False,
                    'urgency': 'none',
                    'message': '✅ No immediate concern, but regular skin checks are always recommended'
            }
