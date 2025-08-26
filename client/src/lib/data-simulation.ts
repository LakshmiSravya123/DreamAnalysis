export function generateEEGData(length: number = 50) {
  return {
    alphaWaves: Array.from({length}, () => Math.sin(Math.random() * Math.PI * 2) * 50 + Math.random() * 20),
    betaWaves: Array.from({length}, () => Math.sin(Math.random() * Math.PI * 4) * 30 + Math.random() * 15),
    timestamp: Date.now()
  };
}

export function generateNeuralNetwork() {
  return {
    nodes: [
      { id: 'frontal', x: 150, y: 60, radius: 20, activity: 85, label: 'Frontal' },
      { id: 'temporal-l', x: 80, y: 140, radius: 18, activity: 72, label: 'Temporal' },
      { id: 'temporal-r', x: 220, y: 140, radius: 18, activity: 68, label: 'Parietal' },
      { id: 'occipital', x: 150, y: 220, radius: 16, activity: 91, label: 'Occipital' },
      { id: 'brainstem', x: 150, y: 280, radius: 14, activity: 77, label: 'Brainstem' }
    ],
    connections: [
      { from: 'frontal', to: 'temporal-l', strength: 0.8 },
      { from: 'frontal', to: 'temporal-r', strength: 0.7 },
      { from: 'temporal-l', to: 'occipital', strength: 0.6 },
      { from: 'temporal-r', to: 'occipital', strength: 0.65 },
      { from: 'occipital', to: 'brainstem', strength: 0.9 }
    ]
  };
}

export function generateDreamSymbols() {
  return [
    { symbol: 'Water/Ocean', frequency: 34, color: 'hsl(195, 100%, 50%)' },
    { symbol: 'Flying/Heights', frequency: 28, color: 'hsl(270, 70%, 65%)' },
    { symbol: 'People/Faces', frequency: 23, color: 'hsl(120, 100%, 55%)' },
    { symbol: 'Animals', frequency: 15, color: 'hsl(15, 100%, 60%)' }
  ];
}

export function generateEmotionData() {
  return {
    labels: ['Joy', 'Curiosity', 'Anxiety', 'Confusion'],
    datasets: [{
      data: [7.8, 6.2, 3.4, 2.1],
      backgroundColor: [
        'hsl(120, 100%, 55%)',
        'hsl(195, 100%, 50%)',
        'hsl(15, 100%, 60%)',
        'hsl(270, 70%, 65%)'
      ]
    }]
  };
}

export function generateHealthInsights() {
  return [
    {
      type: 'success',
      title: 'Excellent Sleep Pattern',
      description: 'Your sleep consistency has improved by 23% this week. Keep maintaining your 10:30 PM bedtime routine.',
      icon: 'check-circle'
    },
    {
      type: 'warning',
      title: 'Stress Spike Detected',
      description: 'Higher stress levels detected between 2-4 PM. Consider taking a 10-minute break during this period.',
      icon: 'exclamation-triangle'
    },
    {
      type: 'info',
      title: 'Activity Recommendation',
      description: 'Based on your neural patterns, you\'re most creative between 9-11 AM. Schedule important tasks during this window.',
      icon: 'lightbulb'
    },
    {
      type: 'secondary',
      title: 'Dream Frequency',
      description: 'Your REM sleep cycles suggest increased dream activity. This correlates with your enhanced creativity metrics.',
      icon: 'moon'
    }
  ];
}
