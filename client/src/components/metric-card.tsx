import { LucideIcon } from "lucide-react";

interface MetricCardProps {
  title: string;
  value: string | number;
  unit?: string;
  change?: string;
  icon: LucideIcon;
  color: "success" | "warning" | "primary" | "secondary";
  animated?: boolean;
  children?: React.ReactNode;
}

export function MetricCard({ 
  title, 
  value, 
  unit, 
  change, 
  icon: Icon, 
  color, 
  animated = false,
  children 
}: MetricCardProps) {
  const colorClasses = {
    success: 'text-success bg-success/20',
    warning: 'text-warning bg-warning/20',
    primary: 'text-primary bg-primary/20',
    secondary: 'text-secondary bg-secondary/20'
  };

  const changeColorClasses = {
    success: 'text-success/70',
    warning: 'text-warning/70',
    primary: 'text-primary/70',
    secondary: 'text-secondary/70'
  };

  return (
    <div className={`glass-card p-6 rounded-xl hover-glow ${animated ? 'animate-pulse-glow' : ''}`}>
      <div className="flex items-center justify-between mb-4">
        <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${colorClasses[color]}`}>
          <Icon className={`${colorClasses[color].split(' ')[0]} text-xl`} />
        </div>
        {unit && <span className="text-xs text-foreground/70 font-mono">{unit}</span>}
      </div>
      <div className="flex items-end space-x-2">
        <span className={`text-3xl font-bold font-mono ${colorClasses[color].split(' ')[0]}`} data-testid={`metric-${title.toLowerCase().replace(/\s+/g, '-')}`}>
          {value}
        </span>
        {change && (
          <span className={`text-sm mb-1 ${changeColorClasses[color]}`}>
            {change}
          </span>
        )}
      </div>
      {children && (
        <div className="mt-4">
          {children}
        </div>
      )}
    </div>
  );
}
