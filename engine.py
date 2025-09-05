import json
from typing import Dict, Any, Optional, List
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HealthImpactEngine:
    def __init__(self, rules_file: str = "health_rules.json"):
        """Initialize the engine with health rules."""
        self.rules = {}
        self.load_rules(rules_file)
    
    def load_rules(self, rules_file: str):
        """Load health rules from JSON file."""
        try:
            with open(rules_file, 'r') as f:
                self.rules = json.load(f)
            logger.info(f"Successfully loaded rules from {rules_file}")
        except FileNotFoundError:
            logger.error(f"Rules file {rules_file} not found!")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {rules_file}: {e}")
            raise
    
    def convert_units(self, element: str, value: float, input_unit: str) -> float:
        """Convert input units to the standard unit defined in rules."""
        if element not in self.rules.get('heavy_metals', {}):
            return value
        
        standard_unit = self.rules['heavy_metals'][element].get('unit', 'mg/L')
        
        # Unit conversion logic
        conversions = {
            ('ppm', 'mg/L'): 1.0,  # ppm is essentially mg/L for water
            ('ppb', 'mg/L'): 0.001,  # 1 ppb = 0.001 mg/L
            ('µg/L', 'mg/L'): 0.001,  # 1 µg/L = 0.001 mg/L
            ('mg/L', 'mg/L'): 1.0,   # same unit
        }
        
        conversion_factor = conversions.get((input_unit, standard_unit), 1.0)
        converted_value = value * conversion_factor
        
        logger.info(f"Converted {element}: {value} {input_unit} → {converted_value} {standard_unit}")
        return converted_value
    
    def clean_input_data(self, raw_data: Dict[str, Any]) -> Dict[str, float]:
        """Clean and standardize input data."""
        cleaned_data = {}
        
        # Mapping of input keys to element symbols
        key_mappings = {
            'Fe (ppm)': ('Fe', 'ppm'),
            'As (ppb)': ('As', 'ppb'),
            'U (ppb)': ('U', 'ppb'),
            'Pb (ppm)': ('Pb', 'ppm'),
            'Cd (ppb)': ('Cd', 'ppb'),
            'Cr (ppm)': ('Cr', 'ppm'),
            'Hg (ppb)': ('Hg', 'ppb'),
            # Add more as needed
        }
        
        for input_key, (element, unit) in key_mappings.items():
            if input_key in raw_data:
                raw_value = raw_data[input_key]
                
                # Handle missing values
                if raw_value == "-" or raw_value is None or raw_value == "":
                    logger.info(f"No data for {element}")
                    continue
                
                try:
                    # Convert to float and then convert units
                    numeric_value = float(raw_value)
                    converted_value = self.convert_units(element, numeric_value, unit)
                    cleaned_data[element] = converted_value
                except (ValueError, TypeError) as e:
                    logger.warning(f"Could not convert {element} value '{raw_value}': {e}")
                    continue
        
        return cleaned_data
    
    def classify_risk(self, element: str, concentration: float) -> Dict[str, Any]:
        """Classify risk level for a given element and concentration."""
        if element not in self.rules.get('heavy_metals', {}):
            return {
                'Risk Level': 'Unknown Element',
                'Diseases': [],
                'Health Effects': ['Element not in database.'],
                'Symptoms': []
            }
        
        element_rules = self.rules['heavy_metals'][element]
        risk_levels = element_rules.get('risk_levels', [])
        
        # Find matching risk level
        for risk_level in risk_levels:
            min_val = risk_level.get('min_value', 0)
            max_val = risk_level.get('max_value', float('inf'))
            
            if min_val <= concentration < max_val:
                return {
                    'Risk Level': risk_level.get('level', 'Unknown'),
                    'Diseases': risk_level.get('diseases', []),
                    'Health Effects': risk_level.get('health_effects', []),
                    'Symptoms': risk_level.get('symptoms', [])
                }
        
        # If no match found, assume highest risk
        if risk_levels:
            highest_risk = risk_levels[-1]  # Assuming last entry is highest risk
            return {
                'Risk Level': highest_risk.get('level', 'Unknown'),
                'Diseases': highest_risk.get('diseases', []),
                'Health Effects': highest_risk.get('health_effects', []),
                'Symptoms': highest_risk.get('symptoms', [])
            }
        
        return {
            'Risk Level': 'No Classification Available',
            'Diseases': [],
            'Health Effects': [],
            'Symptoms': []
        }
    
    def evaluate_sample(self, raw_sample_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main method to evaluate a water sample."""
        # Extract location info if available
        location_info = {
            'Location': raw_sample_data.get('Location', 'Unknown'),
            'State': raw_sample_data.get('State', 'Unknown'),
            'District': raw_sample_data.get('District', 'Unknown'),
            'Year': raw_sample_data.get('Year', 'Unknown'),
            'Coordinates': {
                'Latitude': raw_sample_data.get('Latitude'),
                'Longitude': raw_sample_data.get('Longitude')
            }
        }
        
        # Clean the input data
        cleaned_data = self.clean_input_data(raw_sample_data)
        
        if not cleaned_data:
            return {
                **location_info,
                'Status': 'No heavy metals data available',
                'Results': {}
            }
        
        # Evaluate each element
        results = {}
        overall_risk_levels = []
        
        for element, concentration in cleaned_data.items():
            risk_classification = self.classify_risk(element, concentration)
            
            results[element] = {
                'Concentration': concentration,
                'Unit': self.rules.get('heavy_metals', {}).get(element, {}).get('unit', 'mg/L'),
                'Permissible_Limit': self.rules.get('heavy_metals', {}).get(element, {}).get('permissible_limit'),
                **risk_classification
            }
            
            # Collect risk levels for overall assessment
            overall_risk_levels.append(risk_classification['Risk Level'])
        
        # Determine overall risk
        overall_risk = self.determine_overall_risk(overall_risk_levels)
        
        return {
            **location_info,
            'Overall_Risk': overall_risk,
            'Elements_Tested': len(results),
            'Results': results
        }
    
    def determine_overall_risk(self, risk_levels: List[str]) -> str:
        """Determine overall risk based on individual element risks."""
        risk_priority = {
            'Safe': 0,
            'Elevated Risk': 1,
            'High Risk': 2,
            'Severe Risk': 3,
            'Unknown Element': 0,
            'No Classification Available': 0
        }
        
        if not risk_levels:
            return 'No Data'
        
        max_risk_score = max(risk_priority.get(level, 0) for level in risk_levels)
        
        for level, score in risk_priority.items():
            if score == max_risk_score:
                return level
        
        return 'Unknown'
    
    def get_summary_statistics(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary statistics for the evaluation."""
        if 'Results' not in results:
            return {}
        
        element_results = results['Results']
        
        risk_counts = {}
        elements_above_limit = []
        
        for element, data in element_results.items():
            risk_level = data.get('Risk Level', 'Unknown')
            risk_counts[risk_level] = risk_counts.get(risk_level, 0) + 1
            
            # Check if above permissible limit
            concentration = data.get('Concentration', 0)
            limit = data.get('Permissible_Limit', float('inf'))
            if limit and concentration > limit:
                elements_above_limit.append({
                    'element': element,
                    'concentration': concentration,
                    'limit': limit,
                    'times_above_limit': round(concentration / limit, 2)
                })
        
        return {
            'Risk_Level_Counts': risk_counts,
            'Elements_Above_Permissible_Limit': elements_above_limit,
            'Total_Elements_Tested': len(element_results)
        }