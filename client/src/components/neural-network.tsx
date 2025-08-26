import { useEffect, useState } from "react";

interface NeuralNode {
  id: string;
  x: number;
  y: number;
  radius: number;
  activity: number;
  label: string;
}

interface NeuralConnection {
  from: string;
  to: string;
  strength: number;
}

interface NeuralNetworkProps {
  width?: number;
  height?: number;
}

export function NeuralNetwork({ width = 300, height = 320 }: NeuralNetworkProps) {
  const [nodes, setNodes] = useState<NeuralNode[]>([
    { id: 'frontal', x: 150, y: 60, radius: 20, activity: 85, label: 'Frontal' },
    { id: 'temporal-l', x: 80, y: 140, radius: 18, activity: 72, label: 'Temporal' },
    { id: 'temporal-r', x: 220, y: 140, radius: 18, activity: 68, label: 'Parietal' },
    { id: 'occipital', x: 150, y: 220, radius: 16, activity: 91, label: 'Occipital' },
    { id: 'brainstem', x: 150, y: 280, radius: 14, activity: 77, label: 'Brainstem' }
  ]);

  const connections: NeuralConnection[] = [
    { from: 'frontal', to: 'temporal-l', strength: 0.8 },
    { from: 'frontal', to: 'temporal-r', strength: 0.7 },
    { from: 'temporal-l', to: 'occipital', strength: 0.6 },
    { from: 'temporal-r', to: 'occipital', strength: 0.65 },
    { from: 'occipital', to: 'brainstem', strength: 0.9 }
  ];

  // Update node activities periodically
  useEffect(() => {
    const interval = setInterval(() => {
      setNodes(prevNodes => 
        prevNodes.map(node => ({
          ...node,
          activity: Math.max(20, Math.min(100, node.activity + Math.floor(Math.random() * 10) - 5))
        }))
      );
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  const getNodeColor = (activity: number) => {
    if (activity > 80) return 'var(--neural-cyan)';
    if (activity > 60) return 'var(--neural-purple)';
    if (activity > 40) return 'var(--neural-green)';
    return 'var(--warning)';
  };

  const getConnectionById = (nodeId: string) => {
    return nodes.find(node => node.id === nodeId);
  };

  return (
    <div className="relative h-80 bg-card/20 rounded-lg border border-accent/30 overflow-hidden" data-testid="neural-network">
      <svg className="w-full h-full" viewBox={`0 0 ${width} ${height}`}>
        {/* Connections */}
        {connections.map((connection, index) => {
          const fromNode = getConnectionById(connection.from);
          const toNode = getConnectionById(connection.to);
          
          if (!fromNode || !toNode) return null;

          return (
            <line
              key={`connection-${index}`}
              x1={fromNode.x}
              y1={fromNode.y}
              x2={toNode.x}
              y2={toNode.y}
              stroke="var(--neural-cyan)"
              strokeWidth={2}
              opacity={0.6}
              className="neural-connection"
              style={{ animationDelay: `${index * 0.5}s` }}
            />
          );
        })}

        {/* Nodes */}
        {nodes.map((node, index) => (
          <g key={node.id}>
            <circle
              cx={node.x}
              cy={node.y}
              r={node.radius}
              fill={getNodeColor(node.activity)}
              opacity={0.7}
              className="animate-pulse"
              style={{ animationDelay: `${index * 0.5}s` }}
            />
            <text
              x={node.x}
              y={node.y - node.radius - 5}
              textAnchor="middle"
              className="text-xs fill-current text-foreground"
              data-testid={`node-label-${node.id}`}
            >
              {node.label}
            </text>
          </g>
        ))}
      </svg>

      {/* Activity Legend */}
      <div className="absolute bottom-4 left-4 grid grid-cols-2 gap-2 text-xs">
        <div className="flex items-center space-x-2">
          <div className="w-3 h-3 rounded-full bg-primary"></div>
          <span>High Activity</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-3 h-3 rounded-full bg-secondary"></div>
          <span>Medium Activity</span>
        </div>
      </div>
    </div>
  );
}
