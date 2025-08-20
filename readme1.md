# Neural Dream Weaver - Deployment & Setup Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- 8GB+ RAM recommended
- CUDA-compatible GPU (optional, for real AI models)

### Installation

```bash
# Clone or download the Neural Dream Weaver files
mkdir neural_dream_weaver && cd neural_dream_weaver

# Install core dependencies
pip install streamlit plotly pandas numpy scipy matplotlib seaborn
pip install scikit-learn requests beautifulsoup4 transformers torch
pip install mne faiss-cpu sentence-transformers huggingface-hub

# For advanced features (optional)
pip install opencv-python librosa soundfile pydub
pip install tensorflow keras pytorch-lightning
```

### Running the System

```bash
# Start the main Streamlit application
streamlit run neural_dream_weaver.py

# Run the data integration demo
python ndw_data_demo.py

# Access the web interface at: http://localhost:8501
```

## 📊 Data Integration

### Using Real EEG Data

The system can integrate with real EEG datasets:

```python
from neural_dream_weaver import RealEEGProcessor

# Load EDF files (European Data Format)
processor = RealEEGProcessor()
eeg_data = processor.load_edf_file('path/to/your/sleep_study.edf')

# Process sleep stages
sleep_stages = processor.extract_sleep_stages(eeg_data)
```

### Supported Data Formats
- **EDF/EDF+**: European Data Format (most common)
- **BDF**: BiosignalPlux Data Format
- **FIF**: Neuromag/Elekta MEG format
- **CSV**: Custom CSV formats with timestamp columns

### Public Datasets Integration

```python
# PhysioNet Sleep-EDF Database
dataset_url = "https://physionet.org/content/sleep-edfx/1.0.0/"

# Dream Bank Dataset
dreams_url = "https://www.dreambank.net/random_sample.cgi"

# Integration example
from ndw_data_demo import PublicDatasetLoader
loader = PublicDatasetLoader()
sample_data = loader.download_sample_data()
```

## 🧠 AI Model Configuration

### Hugging Face Integration

```python
# Configure AI models
MODELS = {
    'dream_interpretation': 'microsoft/DialoGPT-large',
    'emotion_analysis': 'cardiffnlp/twitter-roberta-base-emotion', 
    'symbol_detection': 'facebook/bart-large-mnli',
    'image_analysis': 'google/vit-base-patch16-224'
}

# Custom model loading
from transformers import pipeline
interpreter = pipeline('text-generation', model=MODELS['dream_interpretation'])
```

### RAG (Retrieval-Augmented Generation) Setup

```python
from sentence_transformers import SentenceTransformer
import faiss

# Initialize embeddings model
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Create FAISS vector store for dream symbolism
index = faiss.IndexFlatIP(384)  # 384 dimensions for all-MiniLM-L6-v2

# Add psychological and cultural knowledge base
knowledge_base = [
    "Water in dreams represents the unconscious mind and emotions",
    "Flying dreams indicate desire for freedom and transcendence",
    # ... more entries
]

embeddings = embedder.encode(knowledge_base)
index.add(embeddings)
```

## 🔧 BCI Hardware Integration

### Simulated BCI Interface

```python
class MockNeuralink:
    def __init__(self, channels=1024, sample_rate=30000):
        self.channels = channels
        self.sample_rate = sample_rate
        
    def get_neural_data(self, duration=30):
        # Generates realistic EEG-like signals
        # Replace with actual BCI API calls
        pass
```

### Real Hardware Integration

For actual BCI hardware, replace the `MockNeuralink` class:

```python
# Example for OpenBCI integration
import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams

class OpenBCIIntegration:
    def __init__(self):
        params = BrainFlowInputParams()
        self.board_id = BoardIds.SYNTHETIC_BOARD  # Replace with actual board
        self.board = BoardShim(self.board_id, params)
        
    def start_recording(self):
        self.board.prepare_session()
        self.board.start_stream()
        
    def get_neural_data(self, duration=30):
        data = self.board.get_board_data()
        return self.process_raw_data(data)
```

### Supported BCI Systems
- **OpenBCI**: Open-source EEG systems
- **Emotiv EPOC**: Consumer EEG headset
- **NeuroSky**: Single-channel EEG
- **Custom Arduino-based**: DIY solutions
- **Research-grade**: ANT Neuro, Brain Products, etc.

## 🌐 Web Application Deployment

### Local Development

```bash
# Run with debug mode
streamlit run neural_dream_weaver.py --server.runOnSave true --server.port 8501

# Custom configuration
mkdir .streamlit
echo '[server]
runOnSave = true
port = 8501
enableCORS = false

[theme]
primaryColor = "#4ECDC4"
backgroundColor = "#1E1E1E" 
secondaryBackgroundColor = "#2D2D2D"
textColor = "#FFFFFF"' > .streamlit/config.toml
```

### Cloud Deployment

#### Streamlit Cloud
```bash
# 1. Push code to GitHub
git init
git add .
git commit -m "Neural Dream Weaver initial commit"
git remote add origin https://github.com/yourusername/neural-dream-weaver.git
git push -u origin main

# 2. Deploy on Streamlit Cloud
# Visit: https://share.streamlit.io
# Connect GitHub repo and deploy
```

#### Docker Deployment
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "neural_dream_weaver.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
# Build and run
docker build -t neural-dream-weaver .
docker run -p 8501:8501 neural-dream-weaver
```

#### AWS/GCP/Azure Deployment
```bash
# AWS EC2 deployment
aws ec2 run-instances --image-id ami-0abcdef1234567890 --instance-type t3.large
# Configure security groups for port 8501
# SSH and install dependencies

# Google Cloud Run
gcloud run deploy neural-dream-weaver --image gcr.io/PROJECT_ID/neural-dream-weaver --platform managed

# Azure Container Instances
az container create --resource-group myResourceGroup --name neural-dream-weaver --image myregistry.azurecr.io/neural-dream-weaver
```

## 🔒 Security & Privacy Configuration

### Data Encryption

```python
import cryptography
from cryptography.fernet import Fernet

class SecureDataHandler:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
    
    def encrypt_neural_data(self, data):
        serialized = json.dumps(data, default=str).encode()
        return self.cipher.encrypt(serialized)
    
    def decrypt_neural_data(self, encrypted_data):
        decrypted = self.cipher.decrypt(encrypted_data)
        return json.loads(decrypted.decode())
```

### HIPAA Compliance Setup

```python
# HIPAA-compliant configuration
SECURITY_CONFIG = {
    'encryption_at_rest': True,
    'encryption_in_transit': True,
    'access_logging': True,
    'audit_trails': True,
    'automatic_logout': 900,  # 15 minutes
    'session_timeout': 3600,  # 1 hour
    'data_retention_days': 30,
    'backup_encryption': True
}

# Environment variables for sensitive data
import os
DATABASE_URL = os.getenv('SECURE_DATABASE_URL')
ENCRYPTION_KEY = os.getenv('HIPAA_ENCRYPTION_KEY')
```

### User Authentication

```python
import streamlit_authenticator as stauth
import yaml

# config.yaml
authentication = {
    'usernames': {
        'researcher1': {
            'email': 'researcher1@institution.edu',
            'name': 'Dr. Research One',
            'password': 'hashed_password_here'
        }
    }
}

authenticator = stauth.Authenticate(
    authentication['usernames'],
    'neural_dream_weaver',
    'secure_key_here',
    cookie_expiry_days=1
)
```

## 📊 Database Integration

### SQLite (Local Development)
```python
import sqlite3

def init_database():
    conn = sqlite3.connect('neural_dreams.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dream_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            session_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            sleep_stage TEXT,
            neural_activity REAL,
            dream_content TEXT,
            symbols TEXT,
            emotions TEXT,
            enhancement_type TEXT
        )
    ''')
    
    conn.commit()
    return conn
```

### PostgreSQL (Production)
```python
import psycopg2
from sqlalchemy import create_engine

# Production database setup
DATABASE_URL = "postgresql://user:password@localhost:5432/neural_dreams"
engine = create_engine(DATABASE_URL)

# Store session data
def store_dream_analysis(analysis_data):
    query = """
    INSERT INTO dream_analyses (
        session_id, timestamp, sleep_stage, neural_activity,
        dream_description, detected_symbols, emotional_profile,
        enhancement_recommendations
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    # Execute with proper error handling and logging
```

### MongoDB (Document Store)
```python
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.neural_dream_weaver

def store_session_data(session_data):
    collection = db.dream_sessions
    return collection.insert_one(session_data)
```

## 🧪 Testing & Validation

### Unit Testing

```python
import unittest
from neural_dream_weaver import NDWSystem, DreamSymbolDatabase

class TestNeuralDreamWeaver(unittest.TestCase):
    
    def setUp(self):
        self.ndw_system = NDWSystem()
        self.symbol_db = DreamSymbolDatabase()
    
    def test_dream_analysis_pipeline(self):
        # Test complete analysis pipeline
        result = self.ndw_system.analyze_dream(duration=30)
        
        self.assertIsNotNone(result)
        self.assertIn('timestamp', result)
        self.assertIn('dream_content', result)
        self.assertIn('enhancement_recommendations', result)
    
    def test_symbol_interpretation(self):
        # Test symbol database
        symbols = ['water', 'flying', 'chase']
        interpretation = self.symbol_db.get_interpretation(symbols)
        
        self.assertGreater(len(interpretation['individual_symbols']), 0)
        self.assertIsInstance(interpretation['overall_significance'], float)

if __name__ == '__main__':
    unittest.main()
```

### Performance Testing

```python
import time
import memory_profiler

@memory_profiler.profile
def test_memory_usage():
    ndw_system = NDWSystem()
    
    # Test memory usage during extended operation
    for i in range(100):
        analysis = ndw_system.analyze_dream(duration=30)
        time.sleep(0.1)

def test_processing_speed():
    ndw_system = NDWSystem()
    
    start_time = time.time()
    for i in range(10):
        analysis = ndw_system.analyze_dream(duration=30)
    end_time = time.time()
    
    avg_processing_time = (end_time - start_time) / 10
    print(f"Average processing time: {avg_processing_time:.2f} seconds")
```

### Integration Testing

```python
import requests
import json

def test_api_endpoints():
    base_url = "http://localhost:8501"
    
    # Test health endpoint
    response = requests.get(f"{base_url}/health")
    assert response.status_code == 200
    
    # Test dream analysis endpoint
    test_data = {
        "duration": 30,
        "neural_data": "mock_data_here"
    }
    
    response = requests.post(
        f"{base_url}/api/analyze_dream",
        json=test_data
    )
    assert response.status_code == 200
    assert "dream_content" in response.json()
```

## 🏥 Clinical Integration

### Electronic Health Record (EHR) Integration

```python
import hl7
from fhir.resources.observation import Observation

class EHRIntegrator:
    def __init__(self):
        self.ehr_endpoint = "https://your-ehr-system.com/api"
        
    def create_sleep_study_report(self, session_data):
        # Create FHIR-compliant observation
        observation = Observation(
            status="final",
            category=[{
                "coding": [{
                    "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                    "code": "survey",
                    "display": "Survey"
                }]
            }],
            code={
                "coding": [{
                    "system": "http://loinc.org",
                    "code": "72133-2",
                    "display": "Sleep study"
                }]
            },
            subject={"reference": f"Patient/{session_data['patient_id']}"},
            effectiveDateTime=session_data['timestamp'],
            valueString=json.dumps(session_data['analysis'])
        )
        
        return observation.dict()
```

### Medical Device Integration

```python
# FDA 510(k) compliance framework
class MedicalDeviceCompliance:
    def __init__(self):
        self.device_class = "Class II"  # Moderate risk
        self.product_code = "QXX"  # Custom neural monitoring device
        
    def validate_safety_parameters(self, stimulation_params):
        safety_checks = {
            'current_density': stimulation_params['intensity'] <= 2.0,  # mA/cm²
            'frequency_range': 0.1 <= stimulation_params['frequency'] <= 100,
            'session_duration': stimulation_params['duration'] <= 1800,  # 30 min max
            'electrode_impedance': stimulation_params.get('impedance', 0) < 50000  # Ohms
        }
        
        return all(safety_checks.values())
    
    def generate_adverse_event_report(self, event_data):
        # MDR (Medical Device Reporting) format
        return {
            'report_date': datetime.now().isoformat(),
            'device_info': {
                'manufacturer': 'Neural Dream Weaver Inc.',
                'model': 'NDW-1.0',
                'serial_number': event_data.get('device_serial')
            },
            'event_description': event_data['description'],
            'patient_outcome': event_data['outcome'],
            'corrective_actions': event_data['actions_taken']
        }
```

## 📈 Analytics & Monitoring

### Real-time Monitoring

```python
import logging
from prometheus_client import Counter, Histogram, start_http_server

# Metrics collection
DREAM_ANALYSES_TOTAL = Counter('dream_analyses_total', 'Total dream analyses performed')
PROCESSING_TIME = Histogram('processing_time_seconds', 'Time spent processing dreams')
ENHANCEMENT_PROTOCOLS = Counter('enhancement_protocols_total', 'Enhancement protocols generated', ['type'])

class SystemMonitor:
    def __init__(self):
        # Start Prometheus metrics server
        start_http_server(8000)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('ndw_system.log'),
                logging.StreamHandler()
            ]
        )
    
    def log_dream_analysis(self, analysis_result):
        DREAM_ANALYSES_TOTAL.inc()
        
        if analysis_result.get('enhancement_recommendations'):
            enhancement_type = analysis_result['enhancement_recommendations']['top_recommendation']['type']
            ENHANCEMENT_PROTOCOLS.labels(type=enhancement_type).inc()
        
        logging.info(f"Dream analysis completed: {analysis_result['sleep_stage']}")
```

### Usage Analytics

```python
import pandas as pd
import plotly.express as px

class UsageAnalytics:
    def __init__(self):
        self.session_data = []
    
    def generate_usage_report(self):
        df = pd.DataFrame(self.session_data)
        
        # Sleep stage distribution
        stage_dist = df['sleep_stage'].value_counts()
        
        # Enhancement effectiveness
        effectiveness = df.groupby('enhancement_type')['user_satisfaction'].mean()
        
        # Create visualizations
        fig1 = px.pie(values=stage_dist.values, names=stage_dist.index, 
                      title='Sleep Stage Distribution')
        
        fig2 = px.bar(x=effectiveness.index, y=effectiveness.values,
                      title='Enhancement Protocol Effectiveness')
        
        return {
            'sleep_distribution': fig1,
            'enhancement_effectiveness': fig2,
            'total_sessions': len(df),
            'avg_session_duration': df['duration'].mean()
        }
```

## 🔬 Research Integration

### Clinical Trial Management

```python
class ClinicalTrialManager:
    def __init__(self, trial_id):
        self.trial_id = trial_id
        self.participants = {}
        self.protocol_versions = {}
    
    def enroll_participant(self, participant_data):
        # Validate inclusion/exclusion criteria
        eligibility = self.check_eligibility(participant_data)
        
        if eligibility['eligible']:
            participant_id = f"NDW-{len(self.participants)+1:04d}"
            self.participants[participant_id] = {
                'enrolled_date': datetime.now(),
                'demographics': participant_data['demographics'],
                'medical_history': participant_data['medical_history'],
                'baseline_assessments': participant_data['baseline']
            }
            return participant_id
        else:
            return None
    
    def randomize_treatment_group(self, participant_id):
        # Randomization algorithm for treatment assignment
        groups = ['active_treatment', 'sham_control']
        assignment = np.random.choice(groups)
        
        self.participants[participant_id]['treatment_group'] = assignment
        return assignment
    
    def collect_outcome_data(self, participant_id, session_data):
        # Primary endpoints: sleep quality, dream recall, cognitive performance
        # Secondary endpoints: mood, creativity, quality of life
        
        outcomes = {
            'sleep_quality_index': self.calculate_sleep_quality(session_data),
            'dream_recall_frequency': session_data['dream_recall_rate'],
            'cognitive_performance': self.assess_cognitive_performance(participant_id),
            'mood_assessment': self.collect_mood_data(participant_id),
            'adverse_events': session_data.get('adverse_events', [])
        }
        
        return outcomes
```

### Data Export for Publications

```python
def generate_research_dataset(sessions_data, anonymize=True):
    """Generate anonymized dataset for research publications"""
    
    research_data = {
        'study_metadata': {
            'title': 'Neural Dream Weaver Clinical Trial',
            'n_participants': len(sessions_data),
            'study_period': '2025-2026',
            'primary_endpoints': ['sleep_quality', 'dream_recall', 'cognitive_enhancement'],
            'ethics_approval': 'IRB-2025-001'
        },
        'participant_demographics': [],
        'sleep_architecture_data': [],
        'dream_content_analysis': [],
        'enhancement_protocols': [],
        'outcome_measures': []
    }
    
    for session in sessions_data:
        if anonymize:
            session = anonymize_participant_data(session)
        
        # Extract relevant research variables
        research_data['sleep_architecture_data'].append({
            'participant_id': session['participant_id'],
            'sleep_efficiency': session['sleep_metrics']['efficiency'],
            'rem_percentage': session['sleep_metrics']['rem_percent'],
            'slow_wave_sleep': session['sleep_metrics']['sws_percent'],
            'sleep_onset_latency': session['sleep_metrics']['onset_latency']
        })
        
        research_data['dream_content_analysis'].append({
            'participant_id': session['participant_id'],
            'dream_recall_score': session['dream_data']['recall_score'],
            'symbol_diversity': len(session['dream_data']['symbols']),
            'emotional_valence': session['dream_data']['emotional_valence'],
            'narrative_complexity': session['dream_data']['complexity_score']
        })
    
    return research_data

def export_to_formats(research_data):
    """Export data in multiple research formats"""
    
    # SPSS format
    df_spss = pd.DataFrame(research_data['outcome_measures'])
    df_spss.to_spss('ndw_research_data.sav')
    
    # R format
    df_r = pd.DataFrame(research_data['sleep_architecture_data'])
    df_r.to_feather('ndw_sleep_data.feather')
    
    # MATLAB format
    from scipy.io import savemat
    savemat('ndw_analysis.mat', research_data)
    
    # CSV for general use
    for key, data in research_data.items():
        if isinstance(data, list) and data:
            df = pd.DataFrame(data)
            df.to_csv(f'ndw_{key}.csv', index=False)
```

## 🚨 Troubleshooting

### Common Issues and Solutions

```python
class TroubleshootingGuide:
    def __init__(self):
        self.common_issues = {
            'no_neural_data': {
                'symptoms': ['Empty neural data arrays', 'Connection errors'],
                'solutions': [
                    'Check BCI device connection',
                    'Verify electrode placement',
                    'Restart recording session',
                    'Check impedance levels'
                ]
            },
            'poor_sleep_detection': {
                'symptoms': ['Incorrect sleep stage classification', 'Noisy data'],
                'solutions': [
                    'Improve electrode contact',
                    'Reduce environmental interference',
                    'Adjust frequency filtering parameters',
                    'Calibrate system for individual user'
                ]
            },
            'low_dream_recall': {
                'symptoms': ['No dream content detected', 'Sparse symbolic analysis'],
                'solutions': [
                    'Wake during REM sleep phases',
                    'Improve sleep hygiene',
                    'Reduce alcohol/medication interference',
                    'Train dream recall techniques'
                ]
            },
            'stimulation_artifacts': {
                'symptoms': ['Distorted EEG signals', 'False sleep stage detection'],
                'solutions': [
                    'Adjust stimulation intensity',
                    'Use different electrode montage',
                    'Implement real-time artifact removal',
                    'Increase electrode-stimulator separation'
                ]
            }
        }
    
    def diagnose_issue(self, symptoms):
        matches = []
        for issue, details in self.common_issues.items():
            if any(symptom in details['symptoms'] for symptom in symptoms):
                matches.append((issue, details))
        return matches
    
    def get_solutions(self, issue_name):
        return self.common_issues.get(issue_name, {}).get('solutions', [])
```

### System Health Checks

```python
def run_system_diagnostics():
    """Comprehensive system health check"""
    
    diagnostics = {
        'timestamp': datetime.now(),
        'system_status': 'OK',
        'checks': {}
    }
    
    # Memory usage check
    import psutil
    memory_percent = psutil.virtual_memory().percent
    diagnostics['checks']['memory_usage'] = {
        'status': 'OK' if memory_percent < 80 else 'WARNING',
        'value': f"{memory_percent:.1f}%"
    }
    
    # CPU usage check
    cpu_percent = psutil.cpu_percent(interval=1)
    diagnostics['checks']['cpu_usage'] = {
        'status': 'OK' if cpu_percent < 70 else 'WARNING',
        'value': f"{cpu_percent:.1f}%"
    }
    
    # Disk space check
    disk_usage = psutil.disk_usage('/').percent
    diagnostics['checks']['disk_space'] = {
        'status': 'OK' if disk_usage < 85 else 'WARNING',
        'value': f"{disk_usage:.1f}% used"
    }
    
    # Network connectivity
    try:
        requests.get('https://huggingface.co', timeout=5)
        diagnostics['checks']['network'] = {'status': 'OK', 'value': 'Connected'}
    except:
        diagnostics['checks']['network'] = {'status': 'ERROR', 'value': 'No connection'}
    
    # Model availability
    try:
        from transformers import pipeline
        test_pipeline = pipeline('sentiment-analysis')
        diagnostics['checks']['ai_models'] = {'status': 'OK', 'value': 'Models loaded'}
    except:
        diagnostics['checks']['ai_models'] = {'status': 'ERROR', 'value': 'Model loading failed'}
    
    return diagnostics
```

## 📞 Support & Community

### Getting Help

- **Documentation**: https://neural-dream-weaver.readthedocs.io
- **GitHub Issues**: https://github.com/neural-dream-weaver/issues
- **Community Forum**: https://forum.neural-dream-weaver.com
- **Discord Server**: https://discord.gg/neural-dream-weaver

### Contributing

```bash
# Development setup
git clone https://github.com/neural-dream-weaver/neural-dream-weaver.git
cd neural-dream-weaver

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Code formatting
black neural_dream_weaver/
flake8 neural_dream_weaver/

# Submit pull request
git checkout -b feature/your-feature
git commit -m "Add your feature"
git push origin feature/your-feature
```

### License and Citations

```
Neural Dream Weaver
Copyright (C) 2025 Neural Dream Weaver Project

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Citation:
Neural Dream Weaver Research Team (2025). Neural Dream Weaver: 
AI-Powered Dream Analysis and Enhancement System. 
Journal of Sleep and AI, 1(1), 1-25.
```

---

## 🎉 Congratulations!

You have successfully set up the Neural Dream Weaver system. This research prototype demonstrates the potential integration of BCI technology with AI for dream analysis and cognitive enhancement.

**⚠️ Important Reminders:**
- This is a research prototype - not for medical use
- Real BCI integration requires medical supervision
- Obtain proper approvals before human studies
- Follow ethical guidelines for neurotechnology research

**🚀 Next Steps:**
1. Explore the web interface and run sample analyses
2. Integrate your own EEG data sources
3. Customize the AI models for your research needs
4. Join the community to collaborate with other researchers

Happy dream weaving! 🌙✨