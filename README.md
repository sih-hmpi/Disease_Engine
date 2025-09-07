# Health Impact Engine 🏥💧

A comprehensive water quality assessment system that evaluates health risks from heavy metals in water samples. Built for the Smart India Hackathon (SIH), this engine provides detailed risk analysis, disease predictions, and health impact assessments based on heavy metal concentrations in drinking water.

## 🌟 Features

- **Real-time Risk Assessment**: Instant evaluation of water samples for heavy metal contamination
- **Comprehensive Health Analysis**: Detailed disease predictions, symptoms, and health effects
- **Multi-element Support**: Analysis of 18+ heavy metals including Arsenic, Lead, Mercury, Cadmium, and more
- **Risk Classification**: Four-tier risk system (Safe, Elevated Risk, High Risk, Severe Risk)
- **RESTful API**: Easy integration with web applications and mobile apps
- **Location-based Analysis**: Geographic tracking of contamination patterns
- **Unit Conversion**: Automatic handling of different measurement units (ppm, ppb, mg/L)

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Disease_Engine
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health-check

## 📊 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information and available endpoints |
| GET | `/health-check` | System health status |
| POST | `/evaluate` | Evaluate water sample for health risks |
| GET | `/rules` | Get current health assessment rules |
| GET | `/elements` | List supported heavy metals |

### Sample API Usage

**Evaluate Water Sample:**
```bash
curl -X POST "http://localhost:8000/evaluate" \
     -H "Content-Type: application/json" \
     -d '{
       "Location": "Test Site",
       "State": "Maharashtra", 
       "District": "Mumbai",
       "Fe_ppm": 0.5,
       "As_ppb": 15,
       "Pb_ppm": 0.02
     }'
```

**Response:**
```json
{
  "Location": "Test Site",
  "State": "Maharashtra",
  "District": "Mumbai",
  "Overall_Risk": "High Risk",
  "Elements_Tested": 3,
  "Results": {
    "Fe": {
      "Concentration": 0.5,
      "Unit": "mg/L",
      "Risk Level": "Elevated Risk",
      "Diseases": ["Aesthetic Problems"],
      "Health Effects": ["Unpleasant taste and staining"],
      "Symptoms": ["Metallic taste", "Red/brown staining"]
    }
  }
}
```

## 🧪 Testing

Run the test suite to verify engine functionality:

```bash
python test_engine.py
```

The test script includes:
- Engine initialization tests
- Sample data evaluation
- Risk classification validation
- Unit conversion testing

## 🏗️ Architecture

### Core Components

1. **HealthImpactEngine** (`engine.py`)
   - Main processing engine
   - Risk classification logic
   - Unit conversion system
   - Health rules interpretation

2. **FastAPI Application** (`app.py`)
   - REST API endpoints
   - Request/response handling
   - Error management
   - API documentation

3. **Health Rules Database** (`health_rules.json`)
   - Heavy metal thresholds
   - Disease mappings
   - Risk level definitions
   - Health effects database

### Data Flow

```
Water Sample Input → Unit Conversion → Risk Classification → Health Impact Analysis → JSON Response
```

## 📋 Supported Heavy Metals

| Element | Name | Unit | Permissible Limit | Health Concerns |
|---------|------|------|-------------------|-----------------|
| As | Arsenic | mg/L | 0.01 | Cancer, skin lesions, cardiovascular disease |
| Pb | Lead | mg/L | 0.01 | Neurological damage, developmental issues |
| Hg | Mercury | mg/L | 0.001 | Neurological syndrome, birth defects |
| Cd | Cadmium | mg/L | 0.003 | Kidney damage, bone disease |
| Cr | Chromium | mg/L | 0.05 | Organ damage, cancer risk |
| Fe | Iron | mg/L | 0.3 | Aesthetic issues, GI distress |
| Cu | Copper | mg/L | 2.0 | Liver/kidney damage |
| Zn | Zinc | mg/L | 5.0 | GI irritation, metal deficiency |
| Ni | Nickel | mg/L | 0.07 | Allergic reactions, respiratory issues |
| Mn | Manganese | mg/L | 0.4 | Neurological effects, Parkinsonian symptoms |

*And 8 more elements...*

## 🔧 Configuration

### Input Data Format

The engine accepts water sample data with the following fields:

**Location Information (Optional):**
- `Location`: Sample location name
- `State`: State/province
- `District`: District/county
- `Latitude`, `Longitude`: GPS coordinates
- `Year`: Sample collection year

**Heavy Metal Concentrations:**
- `Fe_ppm`: Iron in parts per million
- `As_ppb`: Arsenic in parts per billion
- `Pb_ppm`: Lead in parts per million
- `Cd_ppb`: Cadmium in parts per billion
- `Cr_ppm`: Chromium in parts per million
- `Hg_ppb`: Mercury in parts per billion
- `U_ppb`: Uranium in parts per billion

**Water Quality Parameters (Optional):**
- `pH`: pH level
- `EC`: Electrical conductivity
- `Total_Hardness`: Water hardness
- Various ions (Cl, SO4, NO3, etc.)

### Risk Classification System

1. **Safe**: Below permissible limits, no health concerns
2. **Elevated Risk**: Above limits, early health effects possible
3. **High Risk**: Significant health risks, medical attention recommended
4. **Severe Risk**: Immediate health danger, emergency response needed

## 🚧 Future Enhancements

Based on `improvements.txt`, planned features include:

1. **Security & Access Control**
   - Token-based authentication
   - Secure admin routes for rule management
   - Web interface for configuration

2. **Bulk Processing**
   - Batch API endpoints
   - Asynchronous processing
   - Geographic region analysis

3. **Advanced Analytics**
   - Disease severity mapping
   - Contamination spread analysis
   - Time series data support

4. **Data Management**
   - Data versioning system
   - Big data integration (MongoDB)
   - ML model training pipeline

5. **Extended Capabilities**
   - Heavy metal compounds analysis
   - Precautions recommendation engine
   - Real-time monitoring integration

## 📁 Project Structure

```
Disease_Engine/
├── app.py                 # FastAPI application
├── engine.py              # Core health impact engine
├── health_rules.json      # Health assessment rules
├── test_engine.py         # Test suite
├── requirements.txt       # Python dependencies
├── Data.json             # Sample data
├── improvements.txt      # Future enhancement plans
├── excel-to-json.json    # Data conversion utilities
└── README.md             # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is developed for the Smart India Hackathon. Please refer to the competition guidelines for usage terms.

## 🆘 Support

For support and questions:
- Check the API documentation at `/docs`
- Run the test suite to verify installation
- Review the health rules in `health_rules.json`
- Check the improvements roadmap in `improvements.txt`

## 🏆 Smart India Hackathon

This project addresses critical water quality assessment challenges in India, providing:
- Automated health risk evaluation
- Standardized assessment protocols
- Scalable API architecture
- Real-time contamination monitoring
- Public health decision support

---

**Built with ❤️ for Smart India Hackathon**