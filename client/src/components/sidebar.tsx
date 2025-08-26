import { useState } from "react";
import { Link, useLocation } from "wouter";
import { Brain, ChartLine, Activity, BarChart3, Moon, Bot, Settings, Menu } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useIsMobile } from "@/hooks/use-mobile";

interface SidebarProps {
  currentSection: string;
  onSectionChange: (section: string) => void;
}

export function Sidebar({ currentSection, onSectionChange }: SidebarProps) {
  const [isOpen, setIsOpen] = useState(false);
  const isMobile = useIsMobile();
  const [location] = useLocation();

  const navigationItems = [
    { id: 'dashboard', label: 'Dashboard', icon: ChartLine },
    { id: 'monitoring', label: 'Real-Time Monitor', icon: Activity },
    { id: 'analytics', label: 'Health Analytics', icon: BarChart3 },
    { id: 'dreams', label: 'Dream Analysis', icon: Moon },
    { id: 'companion', label: 'AI Companion', icon: Bot },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  const handleSectionClick = (sectionId: string) => {
    onSectionChange(sectionId);
    if (isMobile) {
      setIsOpen(false);
    }
  };

  return (
    <>
      {/* Mobile Menu Toggle */}
      {isMobile && (
        <Button
          variant="outline"
          size="icon"
          className="fixed top-4 left-4 z-50 glass-card border-primary/20 hover-glow"
          onClick={() => setIsOpen(!isOpen)}
          data-testid="button-mobile-menu"
        >
          <Menu className="h-5 w-5 text-primary" />
        </Button>
      )}

      {/* Sidebar */}
      <div 
        className={`fixed left-0 top-0 w-64 h-screen glass-card border-r border-primary/20 z-40 transition-transform duration-300 ${
          isMobile ? (isOpen ? 'translate-x-0' : '-translate-x-full') : 'translate-x-0'
        }`}
        data-testid="sidebar-navigation"
      >
        <div className="p-6">
          {/* Logo */}
          <div className="flex items-center mb-8">
            <div className="w-10 h-10 bg-gradient-to-br from-primary to-secondary rounded-lg flex items-center justify-center mr-3">
              <Brain className="text-white text-lg" />
            </div>
            <div>
              <h1 className="font-futuristic text-lg font-bold text-gradient">Neural Dream</h1>
              <p className="text-xs text-secondary">Weaver v2.1</p>
            </div>
          </div>
          
          {/* Navigation */}
          <nav className="space-y-2">
            {navigationItems.map((item) => {
              const Icon = item.icon;
              const isActive = currentSection === item.id;
              
              return (
                <button
                  key={item.id}
                  onClick={() => handleSectionClick(item.id)}
                  className={`w-full flex items-center px-4 py-3 rounded-lg transition-all ${
                    isActive 
                      ? 'bg-primary/10 text-primary border border-primary/30 hover-glow' 
                      : 'text-foreground/70 hover:bg-card hover:text-foreground'
                  }`}
                  data-testid={`nav-${item.id}`}
                >
                  <Icon className="mr-3 h-5 w-5" />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>
          
          {/* BCI Status */}
          <div className="mt-8 pt-6 border-t border-border">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-foreground/70">BCI Status</span>
              <div className="status-indicator" data-testid="status-indicator"></div>
            </div>
            <p className="text-xs text-success font-mono">CONNECTED</p>
          </div>
        </div>
      </div>

      {/* Mobile Overlay */}
      {isMobile && isOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-30"
          onClick={() => setIsOpen(false)}
          data-testid="sidebar-overlay"
        />
      )}
    </>
  );
}
