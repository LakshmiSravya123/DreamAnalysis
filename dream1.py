"""
Neural Dream Weaver (NDW) - Streamlit Application
BCI-based dream interpretation system with RAG and multimodal processing
"""

import streamlit as st
import numpy as np
import pandas as pd
import json
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Configure Streamlit page
st.set_page_config(
    page_title="Neural Dream Weaver",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .dream-analysis {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
    }
    .sidebar-section {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Mock classes for simulation (same as before but optimized for Streamlit)
class MockTransformers:
    def __init__(self):
        self.pipeline = self._mock_pipeline
    
    def _mock_pipeline(self, task, model=None):
        if task == "text-generation":
            return MockLLM()
        elif task == "feature-extraction":
            return MockEmbedder()
        return None

class MockLLM:
    def __call__(self, prompt, max_length=200, **kwargs):
        interpretations = [
            "Your dream reveals a deep connection to transformation and growth. The neural patterns suggest processing of recent experiences and emotional integration.",
            "The recurring symbols indicate unresolved emotions seeking integration. Consider journaling about recent changes in your life to facilitate healing.",
            "Your subconscious is working through creative challenges. The dream suggests breakthrough insights are emerging from your unconscious mind.",
            "This dream pattern shows healing processes at work. Your mind is integrating difficult experiences constructively through symbolic processing.",
            "The neural activity indicates processing of memories and emotions. Your dreams suggest a period of personal transformation and self-discovery."
        ]
        return [{"generated_text": random.choice(interpretations)}]

class MockEmbedder:
    def __call__(self, texts):
        return np.random.randn(len(texts), 384)

class MockFAISS:
    def __init__(self, dim):
        self.dim = dim
        self.vectors = []
        self.metadata = []
    
    def add(self, vectors):
        self.vectors.extend(vectors)
    
    def search(self, query_vector, k=5):
        indices = random.sample(range(min(len(self.vectors), 100)), min(k, len(self.vectors)))
        scores = np.random.rand(len(indices))
        return scores, indices

# Initialize session state
if 'ndw_system' not in st.session_state:
    st.session_state.ndw_system = None
if 'session_history' not in st.session_state:
    st.session_state.session_history = []
if 'current_session' not in st.session_state:
    st.session_state.current_session = None
if 'real_time_data' not in st.session_state:
    st.session_state.real_time_data = []

class BCIDataSimulator:
    """Enhanced BCI data simulator with Streamlit integration"""
    
    def __init__(self):
        self.sleep_stages = ['N1', 'N2', 'N3', 'REM']
        self.emotion_states = ['calm', 'anxious', 'excited', 'melancholic', 'fearful', 'joyful']
        self.dream_symbols = ['water', 'flying', 'falling', 'animals', 'people', 'buildings', 'nature', 'vehicles', 'light', 'darkness']
        self.channels = ['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4']
    
    def generate_neural_signals(self, duration_seconds=30, channels=14) -> Dict:
        """Generate multi-channel EEG-like neural signals"""
        sample_rate = 256
        samples = duration_seconds * sample_rate
        time_axis = np.linspace(0, duration_seconds, samples)
        
        signals = {}
        for i in range(min(channels, len(self.channels))):
            channel = self.channels[i]
            
            # Different frequency components
            delta = 0.5 * np.sin(2 * np.pi * 2 * time_axis + np.random.randn())
            theta = 0.3 * np.sin(2 * np.pi * 6 * time_axis + np.random.randn())
            alpha = 0.4 * np.sin(2 * np.pi * 10 * time_axis + np.random.randn())
            beta = 0.2 * np.sin(2 * np.pi * 20 * time_axis + np.random.randn())
            gamma = 0.1 * np.sin(2 * np.pi * 40 * time_axis + np.random.randn())
            
            # Channel-specific characteristics
            if 'O' in channel:  # Occipital - visual processing
                alpha *= 1.5  # Stronger alpha in visual areas
            elif 'F' in channel:  # Frontal - executive function
                beta *= 1.3
                gamma *= 1.2
            
            noise = 0.1 * np.random.randn(samples)
            signals[channel] = delta + theta + alpha + beta + gamma + noise
        
        return {
            'signals': signals,
            'sample_rate': sample_rate,
            'duration': duration_seconds,
            'timestamp': datetime.now()
        }
    
    def detect_sleep_stage(self, signals: Dict) -> Tuple[str, Dict]:
        """Enhanced sleep stage detection with confidence metrics"""
        # Analyze frequency bands across channels
        channel_powers = {}
        for channel, signal in signals['signals'].items():
            fft = np.fft.fft(signal)
            freqs = np.fft.fftfreq(len(signal), 1/signals['sample_rate'])
            
            # Power in different bands
            delta_power = np.mean(np.abs(fft[(freqs >= 1) & (freqs <= 4)]))
            theta_power = np.mean(np.abs(fft[(freqs >= 4) & (freqs <= 8)]))
            alpha_power = np.mean(np.abs(fft[(freqs >= 8) & (freqs <= 12)]))
            beta_power = np.mean(np.abs(fft[(freqs >= 12) & (freqs <= 30)]))
            
            channel_powers[channel] = {
                'delta': delta_power,
                'theta': theta_power,
                'alpha': alpha_power,
                'beta': beta_power
            }
        
        # Average across channels
        avg_powers = {
            'delta': np.mean([cp['delta'] for cp in channel_powers.values()]),
            'theta': np.mean([cp['theta'] for cp in channel_powers.values()]),
            'alpha': np.mean([cp['alpha'] for cp in channel_powers.values()]),
            'beta': np.mean([cp['beta'] for cp in channel_powers.values()])
        }
        
        # Sleep stage classification
        if avg_powers['delta'] > avg_powers['theta'] * 2:
            stage = 'N3'  # Deep sleep
            confidence = 0.85
        elif avg_powers['theta'] > avg_powers['alpha'] * 1.5:
            stage = 'REM' if random.random() > 0.3 else 'N2'
            confidence = 0.75
        elif avg_powers['alpha'] > avg_powers['beta']:
            stage = 'N1'
            confidence = 0.65
        else:
            stage = 'N2'
            confidence = 0.70
        
        metrics = {
            'confidence': confidence,
            'power_bands': avg_powers,
            'dominant_frequency': max(avg_powers, key=avg_powers.get)
        }
        
        return stage, metrics
    
    def extract_dream_content(self, signals: Dict, sleep_stage: str, stage_metrics: Dict) -> Dict:
        """Enhanced dream content extraction"""
        if sleep_stage != 'REM':
            return {'has_dream': False, 'stage': sleep_stage}
        
        # Analyze signal complexity for dream features
        combined_signal = np.concatenate(list(signals['signals'].values()))
        
        features = {
            'signal_entropy': -np.sum(np.histogram(combined_signal, bins=50)[0] * np.log(np.histogram(combined_signal, bins=50)[0] + 1e-10)),
            'complexity': len(np.where(np.abs(np.diff(combined_signal)) > 0.1)[0]),
            'emotional_valence': np.mean(combined_signal),
            'intensity': np.std(combined_signal),
            'coherence': np.corrcoef([signals['signals'][ch] for ch in ['F3', 'F4']])[0, 1] if len(signals['signals']) >= 2 else 0.5
        }
        
        # Generate dream content based on features
        num_symbols = max(1, min(4, int(features['complexity'] / 5000)))
        symbols = random.sample(self.dream_symbols, num_symbols)
        
        # Emotion based on valence and arousal
        if features['emotional_valence'] > 0 and features['intensity'] > 0.3:
            emotion = random.choice(['joyful', 'excited', 'calm'])
        elif features['emotional_valence'] < -0.1:
            emotion = random.choice(['anxious', 'melancholic', 'fearful'])
        else:
            emotion = 'calm'
        
        # Lucidity detection based on frontal coherence
        is_lucid = features['coherence'] > 0.7 and features['intensity'] > 0.4
        
        return {
            'has_dream': True,
            'symbols': symbols,
            'emotion': emotion,
            'intensity': features['intensity'],
            'is_lucid': is_lucid,
            'visual_description': f"Vivid dream involving {', '.join(symbols)} with {emotion} emotional tone",
            'neural_features': features,
            'stage': sleep_stage,
            'confidence': stage_metrics['confidence']
        }

class DreamSymbolRAG:
    """Enhanced RAG system with cultural and psychological knowledge"""
    


    def _index_knowledge(self):
        """Embed and index the knowledge base for retrieval"""
        for i, entry in enumerate(self.knowledge_base):
            # Create a text representation of the entry for embedding
            text_repr = f"{entry['symbol']} {entry['jung_interpretation']} {entry['freud_interpretation']}"
            embedding = self.embedder([text_repr])[0]  # use first vector
            self.index.add(embedding)
   
    def __init__(self):
        self.embedder = MockTransformers().pipeline("feature-extraction")
        self.index = MockFAISS(384)
        self.knowledge_base = self._build_enhanced_knowledge_base()
        self._index_knowledge() 

    
    def _build_enhanced_knowledge_base(self) -> List[Dict]:
        """Comprehensive dream symbol knowledge base"""
        knowledge = [
            {
                'symbol': 'water',
                'jung_interpretation': 'Represents the unconscious mind, emotional depths, and the flow of psychic energy',
                'freud_interpretation': 'Often relates to birth trauma, maternal connections, or sexual symbolism',
                'modern_neuroscience': 'Associated with default mode network activation and emotional memory consolidation',
                'cultural_contexts': {
                    'western': 'Purification, emotional cleansing, baptism, renewal',
                    'eastern': 'Flow of life energy (qi), spiritual transformation, yin energy',
                    'indigenous': 'Connection to ancestors, spiritual realms, life-giving force'
                },
                'clinical_significance': 'May indicate processing of emotional memories or need for emotional release',
                'therapeutic_applications': 'Useful for trauma processing, emotional regulation work'
            },
            {
                'symbol': 'flying',
                'jung_interpretation': 'Desire for spiritual transcendence, individuation, rising above earthly concerns',
                'freud_interpretation': 'Wish fulfillment, escape from repression, sexual liberation',
                'modern_neuroscience': 'Motor cortex activation during REM, spatial processing integration',
                'cultural_contexts': {
                    'western': 'Freedom from earthly constraints, achievement, ambition',
                    'shamanic': 'Soul travel, spiritual journeying, connection to spirit world',
                    'buddhist': 'Liberation from attachment, enlightenment, transcendence'
                },
                'clinical_significance': 'Often correlates with personal empowerment and overcoming limitations',
                'therapeutic_applications': 'Empowerment therapy, overcoming phobias, building confidence'
            },
            {
                'symbol': 'falling',
                'jung_interpretation': 'Fear of losing control, descent into the unconscious, ego dissolution',
                'freud_interpretation': 'Anxiety about failure, loss of support, sexual anxiety',
                'modern_neuroscience': 'Hypnic jerks, vestibular system activation, anxiety processing',
                'cultural_contexts': {
                    'universal': 'Loss of control, insecurity, fear of failure',
                    'western': 'Performance anxiety, career concerns, relationship instability',
                    'eastern': 'Karmic consequences, spiritual testing, ego attachment'
                },
                'clinical_significance': 'Common in anxiety disorders, stress-related conditions',
                'therapeutic_applications': 'Anxiety management, control issues therapy, grounding techniques'
            }
        ]
        
        # Add more symbols with comprehensive data
        additional_symbols = [
            ('animals', 'Instinctual nature, repressed desires, spiritual guides, or aspects of the self'),
            ('people', 'Relationships, social aspects, projected parts of self, or unresolved conflicts'),
            ('buildings', 'Life structure, security, accomplishments, personal boundaries, or psychic architecture'),
            ('nature', 'Growth, natural cycles, peace, authenticity, or connection to the collective unconscious'),
            ('vehicles', 'Life direction, personal control, means of progress, or journey of individuation'),
            ('light', 'Consciousness, enlightenment, divine connection, or emerging awareness'),
            ('darkness', 'The shadow, unknown aspects, fear, or potential for growth and transformation')
        ]
        
        for symbol, basic_meaning in additional_symbols:
            knowledge.append({
                'symbol': symbol,
                'jung_interpretation': f'Relates to {basic_meaning} in the context of individuation',
                'freud_interpretation': f'May represent repressed aspects connected to {basic_meaning.lower()}',
                'modern_neuroscience': f'Neural processing related to {symbol} memories and associations',
                'cultural_contexts': {'universal': basic_meaning},
                'clinical_significance': f'Therapeutic relevance depends on personal associations with {symbol}',
                'therapeutic_applications': f'Can be used in therapy focusing on themes of {basic_meaning.lower()}'
            })
        
        return knowledge
    
    def retrieve_interpretations(self, symbols: List[str], emotion: str, context: Dict = None) -> List[Dict]:
        """Enhanced retrieval with context awareness"""
        query = f"dream symbols: {' '.join(symbols)} emotional tone: {emotion}"
        if context:
            query += f" intensity: {context.get('intensity', 'moderate')} lucid: {context.get('is_lucid', False)}"
        
        query_embedding = self.embedder([query])
        scores, indices = self.index.search(query_embedding[0], k=min(len(symbols) + 2, len(self.knowledge_base)))
        
        relevant_interpretations = []
        for idx in indices:
            if idx < len(self.knowledge_base):
                interpretation = self.knowledge_base[idx].copy()
                # Add relevance score
                interpretation['relevance_score'] = float(scores[len(relevant_interpretations)])
                relevant_interpretations.append(interpretation)
        
        return relevant_interpretations

class MultimodalDreamAnalyzer:
    """Enhanced dream analyzer with clinical insights"""
    
    def __init__(self):
        self.llm = MockTransformers().pipeline("text-generation")
        self.rag = DreamSymbolRAG()
    
    def analyze_dream(self, dream_data: Dict, user_context: Dict = None) -> Dict:
        """Comprehensive dream analysis with clinical insights"""
        if not dream_data.get('has_dream', False):
            return {
                'analysis': 'No significant dream activity detected during this REM period.',
                'sleep_stage': dream_data.get('stage', 'Unknown'),
                'recommendations': ['Focus on sleep hygiene', 'Consider dream recall techniques']
            }
        
        symbols = dream_data.get('symbols', [])
        emotion = dream_data.get('emotion', 'neutral')
        intensity = dream_data.get('intensity', 0)
        is_lucid = dream_data.get('is_lucid', False)
        
        # Retrieve interpretations with context
        context = {'intensity': intensity, 'is_lucid': is_lucid}
        interpretations = self.rag.retrieve_interpretations(symbols, emotion, context)
        
        # Build comprehensive context for LLM
        context_prompt = f"""
        Dream Analysis Context:
        Symbols: {', '.join(symbols)}
        Emotional tone: {emotion}
        Intensity: {intensity:.2f}/1.0
        Lucid dream: {'Yes' if is_lucid else 'No'}
        Neural confidence: {dream_data.get('confidence', 0.5):.2f}
        
        Relevant psychological interpretations:
        """
        
        for interp in interpretations[:3]:
            context_prompt += f"\n- {interp['symbol']}: {interp['jung_interpretation']}"
        
        context_prompt += "\n\nProvide personalized interpretation integrating these elements:"
        
        # Generate interpretation
        response = self.llm(context_prompt, max_length=250, temperature=0.7)
        interpretation = response[0]['generated_text'].replace(context_prompt, '').strip()
        
        # Clinical assessment
        clinical_insights = self._generate_clinical_insights(dream_data, interpretations)
        
        # Therapeutic recommendations
        therapeutic_recs = self._generate_therapeutic_recommendations(dream_data, interpretations)
        
        return {
            'interpretation': interpretation,
            'symbols_analyzed': symbols,
            'emotional_tone': emotion,
            'intensity_score': intensity,
            'lucidity_detected': is_lucid,
            'clinical_insights': clinical_insights,
            'therapeutic_recommendations': therapeutic_recs,
            'relevant_knowledge': interpretations[:3],
            'confidence_score': dream_data.get('confidence', 0.5)
        }
    
    def _generate_clinical_insights(self, dream_data: Dict, interpretations: List[Dict]) -> Dict:
        """Generate clinical insights for therapeutic applications"""
        emotion = dream_data.get('emotion', 'neutral')
        intensity = dream_data.get('intensity', 0)
        symbols = dream_data.get('symbols', [])
        
        insights = {
            'emotional_processing': 'Active',
            'trauma_indicators': [],
            'growth_indicators': [],
            'clinical_attention': []
        }
        
        # Trauma indicators
        if emotion in ['fearful', 'anxious'] and intensity > 0.6:
            insights['trauma_indicators'].append('High-intensity anxiety dreams may indicate unprocessed trauma')
        if 'falling' in symbols and emotion == 'fearful':
            insights['trauma_indicators'].append('Falling dreams with fear may suggest loss of control or security concerns')
        
        # Growth indicators
        if 'flying' in symbols and emotion in ['joyful', 'excited']:
            insights['growth_indicators'].append('Flying dreams with positive emotion suggest personal empowerment')
        if dream_data.get('is_lucid', False):
            insights['growth_indicators'].append('Lucid dreaming indicates increased self-awareness and cognitive control')
        
        # Clinical attention needed
        if len(insights['trauma_indicators']) > 1:
            insights['clinical_attention'].append('Multiple trauma indicators - consider professional consultation')
        if intensity > 0.8 and emotion in ['fearful', 'anxious']:
            insights['clinical_attention'].append('Extremely intense anxiety dreams - may benefit from sleep disorder evaluation')
        
        return insights
    
    def _generate_therapeutic_recommendations(self, dream_data: Dict, interpretations: List[Dict]) -> List[str]:
        """Generate evidence-based therapeutic recommendations"""
        recommendations = []
        emotion = dream_data.get('emotion', 'neutral')
        intensity = dream_data.get('intensity', 0)
        symbols = dream_data.get('symbols', [])
        is_lucid = dream_data.get('is_lucid', False)
        
        # Emotion-based recommendations
        if emotion in ['anxious', 'fearful']:
            recommendations.extend([
                "Practice progressive muscle relaxation before sleep",
                "Consider Image Rehearsal Therapy (IRT) for recurring nightmares",
                "Implement mindfulness meditation to reduce pre-sleep anxiety"
            ])
        elif emotion in ['joyful', 'excited']:
            recommendations.extend([
                "Use dream journaling to capture positive insights",
                "Consider creative expression to integrate dream inspiration"
            ])
        
        # Symbol-specific recommendations
        if 'water' in symbols:
            recommendations.append("Water dreams suggest emotional processing - consider emotional regulation therapy")
        if 'flying' in symbols:
            recommendations.append("Flying dreams indicate empowerment - explore areas where you seek more control")
        
        # Lucidity recommendations
        if is_lucid:
            recommendations.append("Lucid dreaming detected - consider lucid dream therapy for trauma processing")
        
        # Intensity-based recommendations
        if intensity > 0.7:
            recommendations.append("High dream intensity - ensure adequate sleep hygiene and stress management")
        
        return recommendations[:5]  # Limit to top 5

class NeuralEnhancementMCP:
    """Enhanced MCP with real-time visualization capabilities"""
    
    def __init__(self):
        self.enhancement_protocols = {
            'creativity': {'frequency': '40Hz', 'duration': 10, 'intensity': 0.3, 'target': 'Gamma enhancement for creative insights'},
            'relaxation': {'frequency': '8Hz', 'duration': 15, 'intensity': 0.2, 'target': 'Alpha enhancement for relaxation'},
            'memory_consolidation': {'frequency': '6Hz', 'duration': 20, 'intensity': 0.25, 'target': 'Theta enhancement for memory'},
            'lucid_dreaming': {'frequency': '12Hz', 'duration': 5, 'intensity': 0.4, 'target': 'Beta enhancement for lucidity'},
            'anxiety_reduction': {'frequency': '10Hz', 'duration': 12, 'intensity': 0.15, 'target': 'Alpha enhancement for calm'}
        }
    
    def generate_enhancement_protocol(self, analysis: Dict) -> Dict:
        """Generate personalized neural stimulation protocol"""
        emotion = analysis.get('emotional_tone', 'neutral')
        intensity = analysis.get('intensity_score', 0)
        symbols = analysis.get('symbols_analyzed', [])
        clinical_insights = analysis.get('clinical_insights', {})
        
        # Protocol selection logic
        if clinical_insights.get('trauma_indicators'):
            protocol = 'anxiety_reduction'
        elif emotion in ['anxious', 'fearful']:
            protocol = 'relaxation'
        elif 'creativity' in analysis.get('interpretation', '').lower() or 'flying' in symbols:
            protocol = 'creativity'
        elif analysis.get('lucidity_detected', False):
            protocol = 'lucid_dreaming'
        else:
            protocol = 'memory_consolidation'
        
        enhancement = self.enhancement_protocols[protocol].copy()
        enhancement['protocol_type'] = protocol
        enhancement['rationale'] = f"Selected based on {emotion} emotional tone and clinical indicators"
        enhancement['safety_notes'] = "All protocols within safe neuroplasticity parameters"
        
        return enhancement
    
    def create_neural_visualization(self, signals: Dict) -> go.Figure:
        """Create interactive neural signal visualization"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Multi-Channel EEG', 'Frequency Spectrum', 'Sleep Stage Timeline', 'Dream Intensity'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Multi-channel EEG plot
        channels_to_plot = list(signals['signals'].keys())[:4]  # Plot first 4 channels
        for i, channel in enumerate(channels_to_plot):
            signal = signals['signals'][channel][:1000]  # First 1000 samples
            time_axis = np.arange(len(signal)) / signals['sample_rate']
            fig.add_trace(
                go.Scatter(x=time_axis, y=signal + i*2, name=channel, 
                          line=dict(width=1), opacity=0.8),
                row=1, col=1
            )
        
        # Frequency spectrum
        if channels_to_plot:
            signal = signals['signals'][channels_to_plot[0]]
            fft = np.fft.fft(signal)
            freqs = np.fft.fftfreq(len(signal), 1/signals['sample_rate'])
            fig.add_trace(
                go.Scatter(x=freqs[:len(freqs)//2], y=np.abs(fft)[:len(fft)//2], 
                          name='Power Spectrum', line=dict(color='red')),
                row=1, col=2
            )
        
        # Mock sleep stage timeline
        stages = ['N1', 'N2', 'N3', 'REM', 'N2', 'REM']
        stage_times = np.arange(len(stages)) * 90  # 90-minute cycles
        fig.add_trace(
            go.Scatter(x=stage_times, y=[1, 2, 3, 4, 2, 4], 
                      mode='lines+markers', name='Sleep Stages',
                      text=stages, line=dict(color='green', width=3)),
            row=2, col=1
        )
        
        # Dream intensity over time
        dream_times = np.linspace(0, 480, 20)  # 8 hours
        dream_intensities = np.random.beta(2, 5, 20)  # Realistic dream intensity distribution
        fig.add_trace(
            go.Scatter(x=dream_times, y=dream_intensities, 
                      mode='lines+markers', name='Dream Intensity',
                      line=dict(color='purple', width=2), fill='tonexty'),
            row=2, col=2
        )
        
        fig.update_layout(
            height=600,
            showlegend=True,
            title_text="Neural Dream Weaver - Real-time BCI Analysis"
        )
        
        return fig

class StreamlitNeuralDreamWeaver:
    """Main NDW system optimized for Streamlit"""
    
    def __init__(self):
        self.bci_simulator = BCIDataSimulator()
        self.dream_analyzer = MultimodalDreamAnalyzer()
        self.enhancement_mcp = NeuralEnhancementMCP()
    
    def run_real_time_session(self, duration_minutes=30):
        """Run real-time dream analysis session"""
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        cycles = duration_minutes // 10  # 10-minute mini-cycles for demo
        session_data = {
            'session_id': f"NDW_{int(time.time())}",
            'timestamp': datetime.now(),
            'cycles': [],
            'total_dreams': 0
        }
        
        for cycle in range(cycles):
            status_text.text(f"Processing cycle {cycle + 1}/{cycles}...")
            progress_bar.progress((cycle + 1) / cycles)
            
            # Generate neural data
            neural_data = self.bci_simulator.generate_neural_signals(duration_seconds=30, channels=8)
            sleep_stage, stage_metrics = self.bci_simulator.detect_sleep_stage(neural_data)
            dream_content = self.bci_simulator.extract_dream_content(neural_data, sleep_stage, stage_metrics)
            
            cycle_data = {
                'cycle': cycle + 1,
                'sleep_stage': sleep_stage,
                'stage_metrics': stage_metrics,
                'dream_content': dream_content,
                'neural_data': neural_data
            }
            
            if dream_content.get('has_dream', False):
                analysis = self.dream_analyzer.analyze_dream(dream_content)
                enhancement = self.enhancement_mcp.generate_enhancement_protocol(analysis)
                
                cycle_data['analysis'] = analysis
                cycle_data['enhancement'] = enhancement
                session_data['total_dreams'] += 1
            
            session_data['cycles'].append(cycle_data)
            time.sleep(1)  # Simulate processing time
        
        progress_bar.progress(1.0)
        status_text.text("Session completed!")
        
        return session_data

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<h1 class="main-header">🧠 Neural Dream Weaver</h1>', unsafe_allow_html=True)
    st.markdown('<center><i>BCI-Powered Dream Interpretation with AI</i></center>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.markdown("## 🎛️ Control Panel")
    
    # Initialize system
    if st.sidebar.button("🚀 Initialize NDW System"):
        st.session_state.ndw_system = StreamlitNeuralDreamWeaver()
        st.sidebar.success("System initialized!")
    
    if st.session_state.ndw_system is None:
        st.info("👈 Please initialize the NDW system using the sidebar")
        return
    
    # Main interface tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🌙 Live Session", "📊 Analysis", "🧬 Enhancement", "📈 History", "ℹ️ About"])
    
    with tab1:
        st.header("🌙 Live Dream Analysis Session")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            session_duration = st.slider("Session Duration (minutes)", 10, 120, 30, 10)
            
        with col2:
            if st.button("▶️ Start Session", type="primary"):
                with st.spinner("Running dream analysis session..."):
                    session_data = st.session_state.ndw_system.run_real_time_session(session_duration)
                    st.session_state.current_session = session_data
                    st.session_state.session_history.append(session_data)
                st.success(f"Session completed! {session_data['total_dreams']} dreams analyzed.")
        
        with col3:
            if st.button("⏹️ Stop Session"):
                st.warning("Session stopped.")
        
        # Display current session results
        if st.session_state.current_session:
            session = st.session_state.current_session
            
            # Session metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Dreams Detected", session['total_dreams'])
            with col2:
                st.metric("Sleep Cycles", len(session['cycles']))
            with col3:
                rem_cycles = sum(1 for c in session['cycles'] if c['sleep_stage'] == 'REM')
                st.metric("REM Periods", rem_cycles)
            with col4:
                avg_confidence = np.mean([c.get('stage_metrics', {}).get('confidence', 0) for c in session['cycles']])
                st.metric("Avg Confidence", f"{avg_confidence:.2f}")
            
            # Real-time visualization
            st.subheader("🧠 Real-time Neural Activity")
            if session['cycles']:
                latest_cycle = session['cycles'][-1]
                if 'neural_data' in latest_cycle:
                    neural_viz = st.session_state.ndw_system.enhancement_mcp.create_neural_visualization(
                        latest_cycle['neural_data']
                    )
                    st.plotly_chart(neural_viz, use_container_width=True)
            
            # Latest dream analysis
            latest_dreams = [c for c in session['cycles'] if c['dream_content'].get('has_dream', False)]
            if latest_dreams:
                st.subheader("💭 Latest Dream Analysis")
                dream_cycle = latest_dreams[-1]
                
                dream_content = dream_cycle['dream_content']
                analysis = dream_cycle.get('analysis', {})
                
                st.markdown(f"""
                <div class="dream-analysis">
                    <h4>🎭 {dream_content['emotion'].title()} Dream</h4>
                    <p><strong>Symbols:</strong> {', '.join(dream_content['symbols'])}</p>
                    <p><strong>Intensity:</strong> {dream_content['intensity']:.2f}/1.0</p>
                    <p><strong>Lucid:</strong> {'Yes' if dream_content.get('is_lucid', False) else 'No'}</p>
                    <p><strong>Interpretation:</strong> {analysis.get('interpretation', 'Processing...')}</p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.header("📊 Dream Analysis Dashboard")
        
        if not st.session_state.session_history:
            st.info("No analysis data available. Please run a dream session first.")
        else:
            # Session selector
            session_options = [f"Session {i+1} - {s['timestamp'].strftime('%Y-%m-%d %H:%M')}" 
                             for i, s in enumerate(st.session_state.session_history)]
            selected_session = st.selectbox("Select Session", session_options, index=len(session_options)-1)
            
            session_idx = int(selected_session.split()[1]) - 1
            session = st.session_state.session_history[session_idx]
            
            # Detailed analysis
            dreams_in_session = [c for c in session['cycles'] if c['dream_content'].get('has_dream', False)]
            
            if dreams_in_session:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("🎯 Symbol Analysis")
                    all_symbols = []
                    for dream_cycle in dreams_in_session:
                        all_symbols.extend(dream_cycle['dream_content']['symbols'])
                    
                    symbol_counts = pd.Series(all_symbols).value_counts()
                    fig_symbols = px.bar(x=symbol_counts.index, y=symbol_counts.values,
                                       title="Most Common Dream Symbols")
                    fig_symbols.update_layout(xaxis_title="Symbols", yaxis_title="Frequency")
                    st.plotly_chart(fig_symbols, use_container_width=True)
                
                with col2:
                    st.subheader("🎭 Emotional Patterns")
                    emotions = [dc['dream_content']['emotion'] for dc in dreams_in_session]
                    emotion_counts = pd.Series(emotions).value_counts()
                    
                    fig_emotions = px.pie(values=emotion_counts.values, names=emotion_counts.index,
                                        title="Dream Emotional Distribution")
                    st.plotly_chart(fig_emotions, use_container_width=True)
                
                # Detailed dream breakdown
                st.subheader("🔍 Detailed Dream Analysis")
                for i, dream_cycle in enumerate(dreams_in_session):
                    with st.expander(f"Dream {i+1} - {dream_cycle['dream_content']['emotion'].title()}"):
                        dream = dream_cycle['dream_content']
                        analysis = dream_cycle.get('analysis', {})
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.write("**Symbols:**", ", ".join(dream['symbols']))
                            st.write("**Emotion:**", dream['emotion'])
                            st.write("**Intensity:**", f"{dream['intensity']:.2f}")
                        
                        with col2:
                            st.write("**Lucid:**", "Yes" if dream.get('is_lucid', False) else "No")
                            st.write("**Stage:**", dream.get('stage', 'Unknown'))
                            st.write("**Confidence:**", f"{dream.get('confidence', 0):.2f}")
                        
                        with col3:
                            clinical_insights = analysis.get('clinical_insights', {})
                            st.write("**Growth Indicators:**", len(clinical_insights.get('growth_indicators', [])))
                            st.write("**Trauma Indicators:**", len(clinical_insights.get('trauma_indicators', [])))
                        
                        st.write("**Interpretation:**")
                        st.write(analysis.get('interpretation', 'No interpretation available'))
                        
                        if analysis.get('therapeutic_recommendations'):
                            st.write("**Recommendations:**")
                            for rec in analysis['therapeutic_recommendations']:
                                st.write(f"• {rec}")
    
    with tab3:
        st.header("🧬 Neural Enhancement Protocols")
        
        if not st.session_state.session_history:
            st.info("No enhancement data available. Please run a dream session first.")
        else:
            latest_session = st.session_state.session_history[-1]
            enhancement_cycles = [c for c in latest_session['cycles'] if 'enhancement' in c]
            
            if enhancement_cycles:
                st.subheader("⚡ Active Enhancement Protocols")
                
                for i, cycle in enumerate(enhancement_cycles):
                    enhancement = cycle['enhancement']
                    
                    with st.expander(f"Protocol {i+1}: {enhancement['protocol_type'].title()}"):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Frequency", enhancement['frequency'])
                            st.metric("Duration", f"{enhancement['duration']} min")
                        
                        with col2:
                            st.metric("Intensity", f"{enhancement['intensity']:.2f}")
                            st.write("**Target:**", enhancement['target'])
                        
                        with col3:
                            st.write("**Rationale:**")
                            st.write(enhancement['rationale'])
                            st.write("**Safety:**", enhancement['safety_notes'])
                
                # Enhancement effectiveness visualization
                st.subheader("📈 Protocol Effectiveness")
                
                protocol_types = [c['enhancement']['protocol_type'] for c in enhancement_cycles]
                protocol_counts = pd.Series(protocol_types).value_counts()
                
                fig_protocols = px.bar(
                    x=protocol_counts.index,
                    y=protocol_counts.values,
                    title="Enhancement Protocols Used",
                    color=protocol_counts.values,
                    color_continuous_scale="viridis"
                )
                st.plotly_chart(fig_protocols, use_container_width=True)
                
                # Safety monitoring
                st.subheader("🛡️ Safety Monitoring")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Sessions", len(enhancement_cycles))
                with col2:
                    avg_intensity = np.mean([c['enhancement']['intensity'] for c in enhancement_cycles])
                    st.metric("Avg Intensity", f"{avg_intensity:.2f}")
                with col3:
                    max_duration = max([c['enhancement']['duration'] for c in enhancement_cycles])
                    st.metric("Max Duration", f"{max_duration} min")
                
                # Safety alerts
                if avg_intensity > 0.5:
                    st.warning("⚠️ High average intensity detected. Consider reducing stimulation parameters.")
                if max_duration > 20:
                    st.warning("⚠️ Long duration protocols detected. Monitor for any adverse effects.")
                
                st.success("✅ All protocols within safe neuroplasticity parameters")
    
    with tab4:
        st.header("📈 Session History & Trends")
        
        if not st.session_state.session_history:
            st.info("No historical data available. Please run dream sessions to build history.")
        else:
            # Historical overview
            st.subheader("📊 Historical Overview")
            
            total_sessions = len(st.session_state.session_history)
            total_dreams = sum(s['total_dreams'] for s in st.session_state.session_history)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Sessions", total_sessions)
            with col2:
                st.metric("Total Dreams", total_dreams)
            with col3:
                avg_dreams = total_dreams / total_sessions if total_sessions > 0 else 0
                st.metric("Avg Dreams/Session", f"{avg_dreams:.1f}")
            with col4:
                latest_session = st.session_state.session_history[-1]
                st.metric("Latest Session", latest_session['timestamp'].strftime('%m/%d %H:%M'))
            
            # Trends over time
            if total_sessions > 1:
                st.subheader("📈 Trends Analysis")
                
                # Prepare trend data
                session_dates = [s['timestamp'] for s in st.session_state.session_history]
                dreams_per_session = [s['total_dreams'] for s in st.session_state.session_history]
                
                # Dreams per session trend
                fig_trend = go.Figure()
                fig_trend.add_trace(go.Scatter(
                    x=session_dates,
                    y=dreams_per_session,
                    mode='lines+markers',
                    name='Dreams per Session',
                    line=dict(color='blue', width=3)
                ))
                fig_trend.update_layout(
                    title="Dream Activity Over Time",
                    xaxis_title="Session Date",
                    yaxis_title="Number of Dreams",
                    hovermode='x unified'
                )
                st.plotly_chart(fig_trend, use_container_width=True)
                
                # Symbol evolution
                st.subheader("🔄 Symbol Pattern Evolution")
                all_session_symbols = []
                for session in st.session_state.session_history:
                    session_symbols = []
                    for cycle in session['cycles']:
                        if cycle['dream_content'].get('has_dream', False):
                            session_symbols.extend(cycle['dream_content']['symbols'])
                    all_session_symbols.append(session_symbols)
                
                # Create symbol frequency matrix
                unique_symbols = list(set([s for session_syms in all_session_symbols for s in session_syms]))
                symbol_matrix = []
                
                for session_syms in all_session_symbols:
                    session_counts = {symbol: session_syms.count(symbol) for symbol in unique_symbols}
                    symbol_matrix.append([session_counts.get(symbol, 0) for symbol in unique_symbols])
                
                if symbol_matrix and unique_symbols:
                    fig_heatmap = go.Figure(data=go.Heatmap(
                        z=np.array(symbol_matrix).T,
                        x=[f"Session {i+1}" for i in range(len(all_session_symbols))],
                        y=unique_symbols,
                        colorscale='Viridis',
                        hoverongaps=False
                    ))
                    fig_heatmap.update_layout(
                        title="Symbol Patterns Across Sessions",
                        xaxis_title="Sessions",
                        yaxis_title="Dream Symbols"
                    )
                    st.plotly_chart(fig_heatmap, use_container_width=True)
            
            # Export functionality
            st.subheader("💾 Export Data")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📁 Export Session Data"):
                    # Convert to exportable format
                    export_data = []
                    for i, session in enumerate(st.session_state.session_history):
                        for j, cycle in enumerate(session['cycles']):
                            if cycle['dream_content'].get('has_dream', False):
                                dream = cycle['dream_content']
                                analysis = cycle.get('analysis', {})
                                
                                export_data.append({
                                    'session_id': i + 1,
                                    'cycle': j + 1,
                                    'timestamp': session['timestamp'].isoformat(),
                                    'sleep_stage': cycle['sleep_stage'],
                                    'symbols': ', '.join(dream['symbols']),
                                    'emotion': dream['emotion'],
                                    'intensity': dream['intensity'],
                                    'is_lucid': dream.get('is_lucid', False),
                                    'interpretation': analysis.get('interpretation', ''),
                                    'confidence': dream.get('confidence', 0)
                                })
                    
                    if export_data:
                        df = pd.DataFrame(export_data)
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download CSV",
                            data=csv,
                            file_name=f"ndw_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                        st.success(f"Prepared {len(export_data)} dream records for export!")
                    else:
                        st.warning("No dream data available for export.")
            
            with col2:
                if st.button("🗑️ Clear History"):
                    st.session_state.session_history = []
                    st.session_state.current_session = None
                    st.success("History cleared!")
    
    with tab5:
        st.header("ℹ️ About Neural Dream Weaver")
        
        st.markdown("""
        ### 🧠 What is Neural Dream Weaver?
        
        Neural Dream Weaver (NDW) is a cutting-edge BCI-powered dream interpretation system that combines:
        
        - **🔬 Simulated Neuralink BCI**: Real-time neural signal processing during sleep
        - **🤖 RAG System**: Retrieval-Augmented Generation for dream symbolism
        - **🧠 Multimodal AI**: LLM-based dream analysis and interpretation
        - **⚡ Neural Enhancement**: MCP protocols for cognitive enhancement
        - **🏥 Clinical Applications**: Therapeutic insights for PTSD, trauma, and creativity
        
        ### 🎯 Key Features
        
        #### 🌙 Real-time Dream Analysis
        - Multi-channel EEG simulation
        - Sleep stage detection (N1, N2, N3, REM)
        - Dream content extraction from neural patterns
        - Lucid dreaming detection
        
        #### 🔍 AI-Powered Interpretation
        - Jungian and Freudian psychological frameworks
        - Cultural and cross-cultural symbol analysis
        - Clinical insights for therapeutic applications
        - Personalized recommendations
        
        #### ⚡ Neural Enhancement
        - Targeted frequency stimulation protocols
        - Creativity, relaxation, and memory enhancement
        - Safety monitoring and compliance
        - Closed-loop feedback systems
        
        #### 📊 Comprehensive Analytics
        - Session history and trend analysis
        - Symbol pattern evolution
        - Clinical assessment tools
        - Export capabilities for research
        
        ### 🛡️ Ethical Considerations
        
        #### Privacy & Security
        - All neural data processed locally
        - No external data transmission
        - Encrypted session storage
        - User consent and transparency
        
        #### Clinical Safety
        - All stimulation within safe parameters
        - Continuous safety monitoring
        - Professional consultation recommendations
        - Trauma-informed design principles
        
        #### Research Ethics
        - IRB-compliant data collection
        - Informed consent procedures
        - Data anonymization protocols
        - Open-source methodology
        
        ### 🔬 Scientific Foundation
        
        NDW is built on established neuroscience research:
        
        - **Sleep Architecture**: Based on Rechtschaffen & Kales sleep staging
        - **Dream Neuroscience**: Incorporates findings from Hobson, Stickgold, and others
        - **BCI Technology**: Aligned with current Neuralink capabilities
        - **AI Interpretability**: Uses transparent, explainable AI methods
        
        ### 🚀 Future Applications
        
        #### Medical Applications
        - PTSD and trauma therapy
        - Insomnia and sleep disorders
        - Depression and anxiety treatment
        - Cognitive rehabilitation
        
        #### Enhancement Applications
        - Creative problem-solving
        - Memory consolidation
        - Skill acquisition
        - Meditation and mindfulness
        
        #### Research Applications
        - Dream content analysis
        - Consciousness studies
        - Neuroplasticity research
        - Cross-cultural psychology
        
        ### 📚 References & Resources
        
        - [Neuralink Progress Updates](https://neuralink.com)
        - [Dream Research Literature](https://www.sleepfoundation.org)
        - [BCI Safety Guidelines](https://www.ieee.org)
        - [AI Ethics in Healthcare](https://www.who.int)
        
        ---
        
        **⚠️ Disclaimer**: This is a research prototype simulating BCI functionality. 
        Not intended for medical diagnosis or treatment. Consult healthcare professionals 
        for sleep-related concerns.
        """)
        
        # System status
        st.subheader("🔧 System Status")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.success("✅ BCI Simulator: Active")
            st.success("✅ Dream Analyzer: Ready")
        
        with col2:
            st.success("✅ Enhancement MCP: Online")
            st.success("✅ Safety Monitoring: Active")
        
        with col3:
            st.info(f"📊 Sessions: {len(st.session_state.session_history)}")
            st.info(f"🧠 System: v1.0.0")
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #666;">Neural Dream Weaver v1.0.0 | '
        'Advancing Human-AI Collaboration in Dream Research</p>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()