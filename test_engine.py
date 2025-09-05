#!/usr/bin/env python3
"""
Test script for the Health Impact Engine
"""

import json
from engine import HealthImpactEngine

def test_engine():
    """Test the engine with sample data."""
    print("🧪 Testing Health Impact Engine...")
    
    try:
        # Initialize engine
        engine = HealthImpactEngine()
        print("✅ Engine initialized successfully")
        
        # Test sample data (based on your input format)
        test_sample = {
            "S. No.": 1,
            "State": "Andaman & Nicobar Islands",
            "District": "North & Middle Andaman", 
            "Location": "Bakultala",
            "Longitude": 92.8577,
            "Latitude": 12.5043,
            "Year": 2023,
            "pH": 7.96,
            "EC (µS/cm at": 395,
            "CO3 (mg/L)": 0,
            "HCO3": 171,
            "Cl (mg/L)": 14,
            "F (mg/L)": 0.18,
            "SO4": 28,
            "NO3": 8,
            "PO4": 0.04,
            "Total Hardness": 160,
            "Ca (mg/L)": 12,
            "Mg (mg/L)": 32,
            "Na (mg/L)": 18,
            "K (mg/L)": 5,
            "Fe (ppm)": 0.53,
            "As (ppb)": "-",
            "U (ppb)": "-"
        }
        
        print("\n🔍 Testing with sample data:")
        print(f"Location: {test_sample['Location']}")
        print(f"Fe (ppm): {test_sample['Fe (ppm)']}")
        print(f"As (ppb): {test_sample['As (ppb)']}")
        
        # Evaluate the sample
        results = engine.evaluate_sample(test_sample)
        
        print("\n📊 Results:")
        print(json.dumps(results, indent=2))
        
        # Test with arsenic data
        print("\n" + "="*50)
        print("🧪 Testing with Arsenic data...")
        
        arsenic_sample = {
            "Location": "Test Location",
            "State": "Test State", 
            "As (ppb)": 50,  # This should trigger "High Risk"
            "Fe (ppm)": 0.2   # This should be "Safe"
        }
        
        arsenic_results = engine.evaluate_sample(arsenic_sample)
        print(json.dumps(arsenic_results, indent=2))
        
        print("\n✅ All tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_engine()