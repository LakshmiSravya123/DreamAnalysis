import { useState, useEffect, useRef } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { Bot, Send, Mic, Wind, Heart, Leaf } from "lucide-react";
import { apiRequest } from "@/lib/queryClient";
import { useToast } from "@/hooks/use-toast";

interface ChatMessage {
  id: string;
  message: string;
  isUser: boolean;
  timestamp: Date;
}

interface AICompanionProps {
  userId: string;
}

export function AICompanion({ userId }: AICompanionProps) {
  const [message, setMessage] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const queryClient = useQueryClient();
  const { toast } = useToast();

  // Fetch chat history
  const { data: chatHistory = [], isLoading } = useQuery({
    queryKey: ["/api/ai-chat", userId],
    queryFn: async () => {
      const response = await fetch(`/api/ai-chat/${userId}`);
      if (!response.ok) throw new Error('Failed to fetch chat history');
      return response.json();
    }
  });

  // Send message mutation
  const sendMessageMutation = useMutation({
    mutationFn: async (messageText: string) => {
      const response = await apiRequest("POST", "/api/ai-chat", {
        message: messageText,
        userId
      });
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["/api/ai-chat", userId] });
      setMessage("");
    },
    onError: () => {
      toast({
        title: "Message Failed",
        description: "Failed to send message. Please try again.",
        variant: "destructive",
      });
    }
  });

  const handleSendMessage = () => {
    if (!message.trim()) return;
    sendMessageMutation.mutate(message);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatHistory]);

  const quickActions = [
    { icon: Wind, label: "Breathing Exercise", color: "success" },
    { icon: Bot, label: "Guided Meditation", color: "secondary" },
    { icon: Heart, label: "Mood Check-In", color: "primary" },
    { icon: Leaf, label: "Stress Relief", color: "warning" }
  ];

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Chat Interface */}
      <div className="lg:col-span-2 glass-card p-6 rounded-xl hover-glow">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-futuristic font-semibold">AI Companion Chat</h3>
          <div className="flex items-center space-x-2">
            <div className="status-indicator w-2 h-2"></div>
            <span className="text-sm font-mono text-success">ONLINE</span>
          </div>
        </div>

        {/* Chat Messages */}
        <div className="h-96 overflow-y-auto mb-4 space-y-4 bg-card/20 rounded-lg p-4 border border-primary/20" data-testid="chat-messages">
          {isLoading ? (
            <div className="flex items-center justify-center h-full">
              <div className="text-foreground/50">Loading chat history...</div>
            </div>
          ) : chatHistory.length === 0 ? (
            <div className="flex items-start space-x-3">
              <div className="w-8 h-8 bg-gradient-to-br from-primary to-secondary rounded-full flex items-center justify-center flex-shrink-0">
                <Bot className="text-white text-sm" />
              </div>
              <div className="bg-card/50 rounded-lg p-3 max-w-sm">
                <p className="text-sm">Hello! I'm your AI companion. I can help analyze your mood, provide wellness insights, and guide you through relaxation exercises. How are you feeling today?</p>
                <span className="text-xs text-foreground/50">{new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
              </div>
            </div>
          ) : (
            chatHistory.map((chat: ChatMessage) => (
              <div key={chat.id} className={`flex items-start space-x-3 ${chat.isUser ? 'justify-end' : ''}`}>
                {!chat.isUser && (
                  <div className="w-8 h-8 bg-gradient-to-br from-primary to-secondary rounded-full flex items-center justify-center flex-shrink-0">
                    <Bot className="text-white text-sm" />
                  </div>
                )}
                <div className={`rounded-lg p-3 max-w-sm ${chat.isUser ? 'bg-primary/20' : 'bg-card/50'}`}>
                  <p className="text-sm">{chat.message}</p>
                  <span className="text-xs text-foreground/50">
                    {new Date(chat.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </span>
                </div>
                {chat.isUser && (
                  <div className="w-8 h-8 bg-gradient-to-br from-success to-primary rounded-full flex items-center justify-center flex-shrink-0">
                    <div className="w-4 h-4 bg-white rounded-full"></div>
                  </div>
                )}
              </div>
            ))
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Chat Input */}
        <div className="flex items-center space-x-3">
          <Input
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message here..."
            className="flex-1 bg-card/50 border border-primary/30 rounded-lg text-foreground placeholder-foreground/50 focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/20"
            disabled={sendMessageMutation.isPending}
            data-testid="input-chat-message"
          />
          <Button
            onClick={handleSendMessage}
            disabled={sendMessageMutation.isPending || !message.trim()}
            className="bg-gradient-to-r from-primary to-secondary text-primary-foreground hover-glow"
            data-testid="button-send-message"
          >
            <Send className="h-4 w-4" />
          </Button>
          <Button
            variant="outline"
            className="bg-card/50 border border-secondary/30 text-secondary hover:bg-secondary/10"
            data-testid="button-voice-input"
          >
            <Mic className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* Quick Actions & Emotion Analysis */}
      <div className="space-y-6">
        {/* Quick Actions */}
        <Card className="glass-card p-6 rounded-xl hover-glow">
          <h3 className="text-lg font-futuristic font-semibold mb-6">Quick Actions</h3>
          <div className="space-y-4">
            {quickActions.map((action, index) => {
              const Icon = action.icon;
              const colorClasses = {
                success: 'bg-success/10 border-success/30 text-success hover:bg-success/20',
                secondary: 'bg-secondary/10 border-secondary/30 text-secondary hover:bg-secondary/20',
                primary: 'bg-primary/10 border-primary/30 text-primary hover:bg-primary/20',
                warning: 'bg-warning/10 border-warning/30 text-warning hover:bg-warning/20'
              };

              return (
                <Button
                  key={index}
                  variant="outline"
                  className={`w-full py-3 px-4 rounded-lg transition-all flex items-center justify-between ${colorClasses[action.color as keyof typeof colorClasses]}`}
                  data-testid={`button-${action.label.toLowerCase().replace(/\s+/g, '-')}`}
                >
                  <span>{action.label}</span>
                  <Icon className="h-4 w-4" />
                </Button>
              );
            })}
          </div>
        </Card>

        {/* Current Emotion Analysis */}
        <Card className="glass-card p-6 rounded-xl hover-glow">
          <h3 className="text-lg font-futuristic font-semibold mb-6">Emotion Analysis</h3>
          <div className="space-y-4">
            {[
              { label: 'Stress Level', value: 35, color: 'warning' },
              { label: 'Happiness', value: 78, color: 'success' },
              { label: 'Focus', value: 62, color: 'primary' },
              { label: 'Energy', value: 84, color: 'secondary' }
            ].map((metric, index) => (
              <div key={index} className="flex items-center justify-between">
                <span className="text-sm">{metric.label}</span>
                <div className="flex items-center space-x-2">
                  <div className="w-16 h-2 bg-card rounded-full overflow-hidden">
                    <div 
                      className={`h-full rounded-full ${
                        metric.color === 'warning' ? 'bg-warning' :
                        metric.color === 'success' ? 'bg-success' :
                        metric.color === 'primary' ? 'bg-primary' : 'bg-secondary'
                      }`}
                      style={{ width: `${metric.value}%` }}
                    ></div>
                  </div>
                  <span className={`text-xs font-mono ${
                    metric.color === 'warning' ? 'text-warning' :
                    metric.color === 'success' ? 'text-success' :
                    metric.color === 'primary' ? 'text-primary' : 'text-secondary'
                  }`} data-testid={`emotion-${metric.label.toLowerCase().replace(/\s+/g, '-')}`}>
                    {metric.value}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
}
