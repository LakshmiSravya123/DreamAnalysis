import { useState, useEffect } from "react";
import { Sidebar } from "@/components/sidebar";
import { NeuralBackground } from "@/components/neural-background";
import { MetricCard } from "@/components/metric-card";
import { MoodChart } from "@/components/charts/mood-chart";
import { SleepChart } from "@/components/charts/sleep-chart";
import { EEGChart } from "@/components/charts/eeg-chart";
import { NeuralNetwork } from "@/components/neural-network";
import { AIAnalysis } from "@/components/ai-analysis";
import { AICompanion } from "@/components/ai-companion";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";
import { 
  Heart, 
  AlertTriangle, 
  Bed, 
  Brain, 
  Activity,
  BarChart3,
  Moon,
  Bot,
  Settings,
  Download,
  CheckCircle,
  TriangleAlert,
  Lightbulb,
  Star
} from "lucide-react";
import { useMetrics } from "@/hooks/use-metrics";
import { useTheme } from "@/hooks/use-theme";
import { generateHealthInsights, generateDreamSymbols, generateEmotionData } from "@/lib/data-simulation";

export default function Dashboard() {
  const [currentSection, setCurrentSection] = useState("dashboard");
  const [currentTime, setCurrentTime] = useState(new Date());
  const { currentMetrics, eegData, neuralActivity, moodData, sleepData, userId } = useMetrics();
  const { theme, setTheme } = useTheme();

  // Update time every second
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  const sectionTitles = {
    'dashboard': 'Neural Dashboard',
    'monitoring': 'Real-Time Monitor',
    'analytics': 'Health Analytics',
    'dreams': 'Dream Analysis',
    'companion': 'AI Companion',
    'settings': 'Settings'
  };

  const handleDataExport = async () => {
    try {
      const response = await fetch(`/api/export/${userId}`);
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'neural_data.csv';
      a.click();
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Export failed:', error);
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground">
      <NeuralBackground />
      
      <Sidebar 
        currentSection={currentSection} 
        onSectionChange={setCurrentSection}
      />

      {/* Main Content */}
      <div className="md:ml-64 min-h-screen">
        {/* Header */}
        <header className="glass-card border-b border-primary/20 p-4 md:p-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-futuristic font-bold text-gradient" data-testid="page-title">
                {sectionTitles[currentSection as keyof typeof sectionTitles]}
              </h2>
              <p className="text-foreground/70 text-sm" data-testid="current-time">
                {currentTime.toLocaleDateString('en-US', { 
                  weekday: 'long', 
                  year: 'numeric', 
                  month: 'long', 
                  day: 'numeric' 
                })} - {currentTime.toLocaleTimeString('en-US', { hour12: false })}
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 glass-card px-3 py-2 rounded-lg">
                <div className="status-indicator w-2 h-2"></div>
                <span className="text-sm font-mono text-success">98.7% Signal</span>
              </div>
              <Button 
                variant="outline" 
                size="icon"
                className="glass-card border-primary/20 hover-glow"
                onClick={handleDataExport}
                data-testid="button-export"
              >
                <Download className="h-4 w-4 text-primary" />
              </Button>
            </div>
          </div>
        </header>

        {/* Dashboard Section */}
        {currentSection === 'dashboard' && (
          <main className="p-4 md:p-6 space-y-6">
            {/* Real-time Metrics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <MetricCard
                title="Heart Rate"
                value={currentMetrics.heartRate}
                unit="BPM"
                change="+2.3%"
                icon={Heart}
                color="success"
                animated={true}
              >
                <div className="flex space-x-1">
                  {[0, 0.1, 0.2, 0.3].map((delay, index) => (
                    <div 
                      key={index}
                      className="w-1 h-8 bg-success/30 rounded animate-brain-wave"
                      style={{ 
                        animationDelay: `${delay}s`,
                        backgroundColor: index === 3 ? 'var(--success)' : undefined
                      }}
                    />
                  ))}
                </div>
              </MetricCard>

              <MetricCard
                title="Stress Level"
                value={currentMetrics.stressLevel}
                unit="STRESS"
                change="-5.2%"
                icon={AlertTriangle}
                color="warning"
              >
                <Progress value={currentMetrics.stressLevel} className="h-2" />
              </MetricCard>

              <MetricCard
                title="Sleep Quality"
                value={currentMetrics.sleepQuality}
                unit="QUALITY"
                change="+12%"
                icon={Bed}
                color="secondary"
              >
                <div className="flex space-x-1">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <Star 
                      key={star} 
                      className={`h-3 w-3 ${star <= 4 ? 'text-secondary fill-secondary' : 'text-secondary/30'}`} 
                    />
                  ))}
                </div>
              </MetricCard>

              <MetricCard
                title="Neural Activity"
                value={currentMetrics.neuralActivity}
                unit="NEURAL"
                change="+8.7%"
                icon={Brain}
                color="primary"
              >
                <div className="relative">
                  {[0, 25, 50, 75].map((left, index) => (
                    <div 
                      key={index}
                      className="neural-particle"
                      style={{ 
                        left: `${left}%`, 
                        animationDelay: `${index * 0.5}s` 
                      }}
                    />
                  ))}
                </div>
              </MetricCard>
            </div>

            {/* Charts Row */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card className="glass-card p-6 rounded-xl hover-glow">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-lg font-futuristic font-semibold">7-Day Mood Timeline</h3>
                  <BarChart3 className="text-primary" />
                </div>
                <MoodChart data={moodData} />
              </Card>

              <Card className="glass-card p-6 rounded-xl hover-glow">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-lg font-futuristic font-semibold">Sleep & Dream Activity</h3>
                  <Moon className="text-secondary" />
                </div>
                <SleepChart data={sleepData} />
              </Card>
            </div>

            {/* AI Analysis Section */}
            <AIAnalysis userId={userId} />
          </main>
        )}

        {/* Real-Time Monitoring Section */}
        {currentSection === 'monitoring' && (
          <main className="p-4 md:p-6 space-y-6">
            <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
              {/* EEG Brain Waves */}
              <div className="xl:col-span-2 glass-card p-6 rounded-xl hover-glow">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-lg font-futuristic font-semibold">EEG Brain Wave Activity</h3>
                  <div className="flex items-center space-x-2">
                    <div className="status-indicator w-2 h-2"></div>
                    <span className="text-sm font-mono text-success">LIVE</span>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4 mb-6">
                  <div className="text-center">
                    <p className="text-sm text-primary font-mono">Alpha Waves</p>
                    <p className="text-2xl font-bold text-primary" data-testid="alpha-waves">8.5 Hz</p>
                  </div>
                  <div className="text-center">
                    <p className="text-sm text-secondary font-mono">Beta Waves</p>
                    <p className="text-2xl font-bold text-secondary" data-testid="beta-waves">23.2 Hz</p>
                  </div>
                </div>
                <EEGChart alphaWaves={eegData.alphaWaves} betaWaves={eegData.betaWaves} />
              </div>

              {/* Neural Network Graph */}
              <div className="glass-card p-6 rounded-xl hover-glow neural-glow">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-lg font-futuristic font-semibold">Brain Regions</h3>
                  <Activity className="text-accent" />
                </div>
                <NeuralNetwork />
              </div>
            </div>

            {/* Electrode Status Grid */}
            <Card className="glass-card p-6 rounded-xl hover-glow">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-futuristic font-semibold">Electrode Status Grid</h3>
                <span className="text-sm text-foreground/70 font-mono">64 Channels</span>
              </div>
              <div className="grid grid-cols-8 gap-2 mb-4">
                {Array.from({length: 64}, (_, i) => {
                  const status = Math.random();
                  const statusClass = status > 0.9 ? 'border-destructive/30 bg-destructive/20' :
                                    status > 0.8 ? 'border-warning/30 bg-warning/20' :
                                    'border-success/30 bg-success/20';
                  
                  return (
                    <div key={i} className={`w-8 h-8 rounded border flex items-center justify-center text-xs font-mono ${statusClass}`}>
                      {String.fromCharCode(65 + Math.floor(i / 8))}{(i % 8) + 1}
                    </div>
                  );
                })}
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-success">60 Active</span>
                <span className="text-warning">3 Weak</span>
                <span className="text-destructive">1 Error</span>
              </div>
            </Card>
          </main>
        )}

        {/* Health Analytics Section */}
        {currentSection === 'analytics' && (
          <main className="p-4 md:p-6 space-y-6">
            {/* Health Metrics Overview */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <Card className="glass-card p-6 rounded-xl hover-glow">
                <h3 className="text-lg font-futuristic font-semibold mb-4">Daily Steps</h3>
                <div className="text-3xl font-bold text-primary font-mono mb-2">{currentMetrics.dailySteps?.toLocaleString()}</div>
                <div className="text-sm text-foreground/70 mb-4">Target: 10,000 steps</div>
                <Progress value={((currentMetrics.dailySteps || 0) / 10000) * 100} className="h-2" />
              </Card>

              <Card className="glass-card p-6 rounded-xl hover-glow">
                <h3 className="text-lg font-futuristic font-semibold mb-4">Sleep Duration</h3>
                <div className="text-3xl font-bold text-secondary font-mono mb-2">
                  {Math.floor(currentMetrics.sleepDuration || 0)}h {Math.round(((currentMetrics.sleepDuration || 0) % 1) * 60)}m
                </div>
                <div className="text-sm text-foreground/70 mb-4">Recommended: 8h</div>
                <div className="flex items-center space-x-2">
                  <Bed className="text-secondary h-4 w-4" />
                  <span className="text-sm text-secondary">Good quality sleep</span>
                </div>
              </Card>

              <Card className="glass-card p-6 rounded-xl hover-glow">
                <h3 className="text-lg font-futuristic font-semibold mb-4">Avg Heart Rate</h3>
                <div className="text-3xl font-bold text-success font-mono mb-2">{currentMetrics.heartRate}</div>
                <div className="text-sm text-foreground/70 mb-4">Resting: 65-75 BPM</div>
                <div className="flex items-center space-x-2">
                  <Heart className="text-success h-4 w-4" />
                  <span className="text-sm text-success">Optimal range</span>
                </div>
              </Card>
            </div>

            {/* Personalized Insights */}
            <Card className="glass-card p-6 rounded-xl hover-glow">
              <h3 className="text-lg font-futuristic font-semibold mb-6">AI-Powered Health Insights</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {generateHealthInsights().map((insight, index) => {
                  const iconMap = {
                    'check-circle': CheckCircle,
                    'exclamation-triangle': TriangleAlert,
                    'lightbulb': Lightbulb,
                    'moon': Moon
                  };
                  
                  const Icon = iconMap[insight.icon as keyof typeof iconMap];
                  const colorClasses = {
                    success: 'bg-success/10 border-success/30 text-success',
                    warning: 'bg-warning/10 border-warning/30 text-warning',
                    info: 'bg-primary/10 border-primary/30 text-primary',
                    secondary: 'bg-secondary/10 border-secondary/30 text-secondary'
                  };

                  return (
                    <div key={index} className={`flex items-start space-x-3 p-4 rounded-lg border ${colorClasses[insight.type as keyof typeof colorClasses]}`}>
                      <Icon className="mt-1 h-5 w-5" />
                      <div>
                        <h4 className="font-semibold mb-1">{insight.title}</h4>
                        <p className="text-sm text-foreground/80">{insight.description}</p>
                      </div>
                    </div>
                  );
                })}
              </div>
            </Card>
          </main>
        )}

        {/* Dream Analysis Section */}
        {currentSection === 'dreams' && (
          <main className="p-4 md:p-6 space-y-6">
            {/* Dream Visual Gallery */}
            <Card className="glass-card p-6 rounded-xl hover-glow">
              <h3 className="text-lg font-futuristic font-semibold mb-6">Dream Visualization Gallery</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="relative group cursor-pointer">
                  <img 
                    src="/attached_assets/generated_images/Stone_bridge_over_water_937b9eb2.png"
                    alt="Bridge over water - symbolizing connection and transition"
                    className="w-full h-32 object-cover rounded-lg hover:scale-105 transition-transform duration-300"
                    data-testid="dream-image-bridge"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end">
                    <p className="text-white text-xs p-2">Bridge - Connection & Transition</p>
                  </div>
                </div>
                <div className="relative group cursor-pointer">
                  <img 
                    src="/attached_assets/generated_images/Dreamy_ocean_underwater_scene_960ab45b.png"
                    alt="Underwater ocean scene with fish - representing emotional depths"
                    className="w-full h-32 object-cover rounded-lg hover:scale-105 transition-transform duration-300"
                    data-testid="dream-image-ocean"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end">
                    <p className="text-white text-xs p-2">Ocean - Emotional Depths</p>
                  </div>
                </div>
                <div className="relative group cursor-pointer">
                  <img 
                    src="/attached_assets/generated_images/Flying_through_clouds_freedom_d3128361.png"
                    alt="Flying through clouds - representing freedom and transcendence"
                    className="w-full h-32 object-cover rounded-lg hover:scale-105 transition-transform duration-300"
                    data-testid="dream-image-flying"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end">
                    <p className="text-white text-xs p-2">Flying - Freedom & Liberation</p>
                  </div>
                </div>
                <div className="relative group cursor-pointer">
                  <img 
                    src="/attached_assets/generated_images/Geometric_neural_patterns_brain_d8b55873.png"
                    alt="Geometric neural patterns - representing structured thinking"
                    className="w-full h-32 object-cover rounded-lg hover:scale-105 transition-transform duration-300"
                    data-testid="dream-image-patterns"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end">
                    <p className="text-white text-xs p-2">Patterns - Analytical Mind</p>
                  </div>
                </div>
              </div>
            </Card>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Dream Symbol Analysis */}
              <Card className="glass-card p-6 rounded-xl hover-glow">
                <h3 className="text-lg font-futuristic font-semibold mb-6">Dream Symbol Analysis</h3>
                <div className="space-y-4">
                  {generateDreamSymbols().map((symbol, index) => {
                    const iconMap = {
                      'Water/Ocean': '🌊',
                      'Flying/Heights': '🕊️',
                      'People/Faces': '👥',
                      'Animals': '🦋'
                    };
                    return (
                      <div key={index} className="flex justify-between items-center p-3 rounded-lg bg-card/20 border border-primary/10">
                        <div className="flex items-center space-x-3">
                          <span className="text-lg">{iconMap[symbol.symbol as keyof typeof iconMap]}</span>
                          <span className="text-sm font-medium">{symbol.symbol}</span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <div className="w-20 h-3 bg-card rounded-full overflow-hidden">
                            <div 
                              className="h-full rounded-full transition-all duration-500"
                              style={{ 
                                width: `${symbol.frequency}%`,
                                backgroundColor: symbol.color
                              }}
                            />
                          </div>
                          <span className="text-xs font-mono font-bold" style={{ color: symbol.color }}>
                            {symbol.frequency}%
                          </span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </Card>

              {/* Emotion Intensity */}
              <Card className="glass-card p-6 rounded-xl hover-glow">
                <h3 className="text-lg font-futuristic font-semibold mb-6">Dream Emotion Intensity</h3>
                <div className="space-y-4">
                  {[
                    { emotion: 'Joy/Happiness', value: 7.8, color: 'text-success', icon: '😊' },
                    { emotion: 'Curiosity', value: 6.2, color: 'text-primary', icon: '🤔' },
                    { emotion: 'Anxiety', value: 3.4, color: 'text-warning', icon: '😰' },
                    { emotion: 'Confusion', value: 2.1, color: 'text-secondary', icon: '😕' }
                  ].map((item, index) => (
                    <div key={index} className="flex items-center justify-between p-3 rounded-lg bg-card/20 border border-primary/10">
                      <div className="flex items-center space-x-3">
                        <span className="text-lg">{item.icon}</span>
                        <span className="text-sm font-medium">{item.emotion}</span>
                      </div>
                      <div className="flex items-center space-x-3">
                        <div className="w-16 h-2 bg-card rounded-full overflow-hidden">
                          <div 
                            className={`h-full rounded-full transition-all duration-500 ${
                              item.color === 'text-success' ? 'bg-success' :
                              item.color === 'text-primary' ? 'bg-primary' :
                              item.color === 'text-warning' ? 'bg-warning' : 'bg-secondary'
                            }`}
                            style={{ width: `${(item.value / 10) * 100}%` }}
                          />
                        </div>
                        <span className={`text-sm font-bold font-mono ${item.color}`}>
                          {item.value}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </Card>
            </div>

            {/* Enhanced Dream Analysis */}
            <Card className="glass-card p-6 rounded-xl hover-glow">
              <h3 className="text-lg font-futuristic font-semibold mb-6">Latest Dream Interpretation</h3>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div>
                  <div className="relative overflow-hidden rounded-lg mb-4">
                    <img 
                      src="/attached_assets/generated_images/Stone_bridge_over_water_937b9eb2.png"
                      alt="Bridge over ocean dream visualization"
                      className="w-full h-48 object-cover"
                      data-testid="main-dream-image"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
                    <div className="absolute bottom-4 left-4">
                      <h4 className="font-semibold text-white text-lg">Bridge Over Ocean</h4>
                      <p className="text-white/80 text-sm">Latest dream visualization</p>
                    </div>
                  </div>
                  <div className="bg-card/30 p-4 rounded-lg border border-secondary/20">
                    <h4 className="font-semibold text-secondary mb-2">Dream Narrative</h4>
                    <p className="text-foreground/80 text-sm mb-4">
                      "I was standing on a bridge over a vast ocean. The water was crystal clear, and I could see colorful fish swimming far below. 
                      Suddenly, I had the ability to fly and soared over the water, feeling completely free and weightless. 
                      The sky was filled with geometric patterns that seemed to pulse with light..."
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {['Water', 'Flying', 'Freedom', 'Geometric Patterns'].map((tag, index) => (
                        <Badge key={index} variant="outline" className="border-primary/30 text-primary">
                          {tag}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </div>
                <div className="space-y-4">
                  <div className="bg-card/30 rounded-lg p-4 border border-primary/20">
                    <h4 className="font-semibold text-primary mb-3 flex items-center">
                      <Brain className="mr-2 h-4 w-4" />
                      AI Analysis
                    </h4>
                    <div className="space-y-3 text-sm text-foreground/80">
                      <div className="flex items-start space-x-2">
                        <span className="text-lg">🌊</span>
                        <div>
                          <p className="font-medium text-primary">Water Symbolism</p>
                          <p>Represents emotional depths and unconscious mind. Clear water indicates clarity of thought.</p>
                        </div>
                      </div>
                      <div className="flex items-start space-x-2">
                        <span className="text-lg">🕊️</span>
                        <div>
                          <p className="font-medium text-secondary">Flying Experience</p>
                          <p>Indicates desire for freedom and transcendence of current limitations.</p>
                        </div>
                      </div>
                      <div className="flex items-start space-x-2">
                        <span className="text-lg">🔮</span>
                        <div>
                          <p className="font-medium text-accent">Geometric Patterns</p>
                          <p>Suggest structured thinking and analytical approach to problem-solving.</p>
                        </div>
                      </div>
                      <div className="p-3 bg-success/10 rounded-lg border border-success/20">
                        <p className="text-success font-semibold">Overall Interpretation:</p>
                        <p className="text-foreground/80 text-xs mt-1">Positive dream indicating emotional clarity, personal growth, and readiness for new challenges.</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </Card>
          </main>
        )}

        {/* AI Companion Section */}
        {currentSection === 'companion' && (
          <main className="p-4 md:p-6 space-y-6">
            <AICompanion userId={userId} />
          </main>
        )}

        {/* Settings Section */}
        {currentSection === 'settings' && (
          <main className="p-4 md:p-6 space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* BCI Configuration */}
              <Card className="glass-card p-6 rounded-xl hover-glow">
                <h3 className="text-lg font-futuristic font-semibold mb-6">BCI Configuration</h3>
                <div className="space-y-6">
                  <div>
                    <Label className="text-sm font-medium text-foreground/80 mb-2">Electrode Count</Label>
                    <Select defaultValue="64">
                      <SelectTrigger className="w-full bg-card/50 border border-primary/30">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="32">32 Channels</SelectItem>
                        <SelectItem value="64">64 Channels</SelectItem>
                        <SelectItem value="128">128 Channels</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  
                  <div>
                    <Label className="text-sm font-medium text-foreground/80 mb-2">Sampling Rate</Label>
                    <Select defaultValue="500">
                      <SelectTrigger className="w-full bg-card/50 border border-primary/30">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="250">250 Hz</SelectItem>
                        <SelectItem value="500">500 Hz</SelectItem>
                        <SelectItem value="1000">1000 Hz</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <Label className="text-sm font-medium text-foreground/80 mb-4">Alert Thresholds</Label>
                    <div className="space-y-3">
                      <div>
                        <Label className="text-xs text-foreground/60">Stress Level Alert</Label>
                        <Slider defaultValue={[75]} max={100} step={1} className="w-full mt-2" />
                        <div className="flex justify-between text-xs text-foreground/50 mt-1">
                          <span>0%</span>
                          <span>75%</span>
                          <span>100%</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </Card>

              {/* Interface Settings */}
              <Card className="glass-card p-6 rounded-xl hover-glow">
                <h3 className="text-lg font-futuristic font-semibold mb-6">Interface Settings</h3>
                <div className="space-y-6">
                  <div>
                    <Label className="text-sm font-medium text-foreground/80 mb-2">Theme</Label>
                    <div className="flex space-x-3">
                      <Button
                        variant={theme === 'dark' ? 'default' : 'outline'}
                        className={`flex-1 ${theme === 'dark' ? 'bg-primary/20 border-primary/30 text-primary' : ''}`}
                        onClick={() => setTheme('dark')}
                        data-testid="button-theme-dark"
                      >
                        Dark Mode
                      </Button>
                      <Button
                        variant={theme === 'light' ? 'default' : 'outline'}
                        className={`flex-1 ${theme === 'light' ? 'bg-primary/20 border-primary/30 text-primary' : ''}`}
                        onClick={() => setTheme('light')}
                        data-testid="button-theme-light"
                      >
                        Light Mode
                      </Button>
                    </div>
                  </div>

                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <Label className="text-sm">Chart Animations</Label>
                      <Switch defaultChecked data-testid="switch-chart-animations" />
                    </div>
                    <div className="flex items-center justify-between">
                      <Label className="text-sm">Neural Flow Effects</Label>
                      <Switch defaultChecked data-testid="switch-neural-effects" />
                    </div>
                    <div className="flex items-center justify-between">
                      <Label className="text-sm">Health Alerts</Label>
                      <Switch defaultChecked data-testid="switch-health-alerts" />
                    </div>
                  </div>
                </div>
              </Card>
            </div>

            {/* Data Export & Privacy */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card className="glass-card p-6 rounded-xl hover-glow">
                <h3 className="text-lg font-futuristic font-semibold mb-6">Data Export</h3>
                <div className="space-y-4">
                  <Button 
                    onClick={handleDataExport}
                    className="w-full bg-success/10 border border-success/30 text-success hover:bg-success/20"
                    data-testid="button-export-health-data"
                  >
                    <Download className="mr-2 h-4 w-4" />
                    Export Health Data (CSV)
                  </Button>
                  <Button 
                    variant="outline"
                    className="w-full bg-secondary/10 border border-secondary/30 text-secondary hover:bg-secondary/20"
                    data-testid="button-export-dream-analysis"
                  >
                    <Download className="mr-2 h-4 w-4" />
                    Export Dream Analysis
                  </Button>
                </div>
                <div className="mt-6 text-xs text-foreground/50">
                  <p>Last export: {new Date().toLocaleDateString()}</p>
                  <p>Data retention: 90 days</p>
                </div>
              </Card>

              <Card className="glass-card p-6 rounded-xl hover-glow">
                <h3 className="text-lg font-futuristic font-semibold mb-6">Privacy & Security</h3>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <Label className="text-sm">Local Data Processing</Label>
                    <Switch defaultChecked data-testid="switch-local-processing" />
                  </div>
                  <div className="flex items-center justify-between">
                    <Label className="text-sm">Data Encryption</Label>
                    <Switch defaultChecked data-testid="switch-data-encryption" />
                  </div>
                  <div className="flex items-center justify-between">
                    <Label className="text-sm">Anonymous Analytics</Label>
                    <Switch data-testid="switch-anonymous-analytics" />
                  </div>
                  <Button 
                    variant="destructive"
                    className="w-full mt-6 bg-destructive/10 border border-destructive/30 text-destructive hover:bg-destructive/20"
                    data-testid="button-clear-data"
                  >
                    <AlertTriangle className="mr-2 h-4 w-4" />
                    Clear All Data
                  </Button>
                </div>
              </Card>
            </div>
          </main>
        )}
      </div>
    </div>
  );
}
