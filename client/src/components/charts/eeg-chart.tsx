import { useEffect, useRef } from "react";
import { Chart, ChartConfiguration, registerables } from "chart.js";

Chart.register(...registerables);

interface EEGChartProps {
  alphaWaves: number[];
  betaWaves: number[];
}

export function EEGChart({ alphaWaves, betaWaves }: EEGChartProps) {
  const chartRef = useRef<HTMLCanvasElement>(null);
  const chartInstance = useRef<Chart | null>(null);

  useEffect(() => {
    if (!chartRef.current) return;

    const ctx = chartRef.current.getContext('2d');
    if (!ctx) return;

    // Destroy existing chart
    if (chartInstance.current) {
      chartInstance.current.destroy();
    }

    const labels = Array.from({length: alphaWaves.length}, (_, i) => i);

    const config: ChartConfiguration = {
      type: 'line',
      data: {
        labels,
        datasets: [
          {
            label: 'Alpha Waves',
            data: alphaWaves,
            borderColor: 'hsl(195, 100%, 50%)',
            borderWidth: 2,
            pointRadius: 0,
            tension: 0.1
          },
          {
            label: 'Beta Waves',
            data: betaWaves,
            borderColor: 'hsl(270, 70%, 65%)',
            borderWidth: 2,
            pointRadius: 0,
            tension: 0.1
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: false,
        plugins: {
          legend: { 
            labels: { color: 'rgba(255, 255, 255, 0.7)' }
          }
        },
        scales: {
          y: { 
            min: -100,
            max: 100,
            grid: { color: 'rgba(255, 255, 255, 0.1)' },
            ticks: { color: 'rgba(255, 255, 255, 0.7)' }
          },
          x: {
            display: false
          }
        }
      }
    };

    chartInstance.current = new Chart(ctx, config);

    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }
    };
  }, [alphaWaves, betaWaves]);

  return (
    <div className="chart-container h-64">
      <canvas ref={chartRef} data-testid="chart-eeg" />
    </div>
  );
}
