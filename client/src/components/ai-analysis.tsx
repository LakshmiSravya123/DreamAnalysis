import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card } from "@/components/ui/card";
import { Brain, Loader2 } from "lucide-react";
import { apiRequest } from "@/lib/queryClient";
import { useToast } from "@/hooks/use-toast";

interface AnalysisResult {
  mood: string;
  stressLevel: number;
  emotions: string[];
  recommendations: string[];
}

interface AIAnalysisProps {
  userId: string;
}

export function AIAnalysis({ userId }: AIAnalysisProps) {
  const [inputText, setInputText] = useState("");
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const { toast } = useToast();

  const analysisMutation = useMutation({
    mutationFn: async (text: string) => {
      const response = await apiRequest("POST", "/api/analyze-mood", {
        text,
        userId
      });
      return response.json();
    },
    onSuccess: (data) => {
      setAnalysisResult(data);
      toast({
        title: "Analysis Complete",
        description: "Your mood and emotional state has been analyzed.",
      });
    },
    onError: () => {
      toast({
        title: "Analysis Failed",
        description: "Failed to analyze mood. Please try again.",
        variant: "destructive",
      });
    }
  });

  const handleAnalyze = () => {
    if (!inputText.trim()) {
      toast({
        title: "Input Required",
        description: "Please enter some text to analyze.",
        variant: "destructive",
      });
      return;
    }
    
    analysisMutation.mutate(inputText);
  };

  return (
    <Card className="glass-card p-6 rounded-xl hover-glow">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-futuristic font-semibold">AI Mood & Dream Analysis</h3>
        <Brain className="text-accent" />
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <Textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Describe your current mood, recent dreams, or any thoughts you'd like to analyze..."
            className="w-full h-32 bg-card/50 border border-primary/30 rounded-lg p-4 text-foreground placeholder-foreground/50 focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 resize-none"
            data-testid="input-mood-analysis"
          />
          <Button
            onClick={handleAnalyze}
            disabled={analysisMutation.isPending}
            className="mt-4 bg-gradient-to-r from-primary to-secondary text-primary-foreground hover-glow font-medium"
            data-testid="button-analyze-mood"
          >
            {analysisMutation.isPending ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <Brain className="mr-2 h-4 w-4" />
                Analyze with AI
              </>
            )}
          </Button>
        </div>
        
        <div className="bg-card/30 rounded-lg p-4 border border-secondary/20">
          <h4 className="font-semibold text-secondary mb-3">
            {analysisResult ? "Analysis Results" : "Recent Analysis"}
          </h4>
          
          {analysisResult ? (
            <div className="space-y-3 text-sm text-foreground/80">
              <div>
                <span className="font-medium text-primary">Mood:</span> {analysisResult.mood}
              </div>
              <div>
                <span className="font-medium text-warning">Stress Level:</span> {analysisResult.stressLevel}%
              </div>
              <div>
                <span className="font-medium text-secondary">Emotions:</span>
                <div className="flex flex-wrap gap-1 mt-1">
                  {analysisResult.emotions.map((emotion, index) => (
                    <span key={index} className="px-2 py-1 bg-accent/20 text-accent text-xs rounded-full">
                      {emotion}
                    </span>
                  ))}
                </div>
              </div>
              {analysisResult.recommendations.length > 0 && (
                <div>
                  <span className="font-medium text-success">Recommendations:</span>
                  <ul className="mt-1 space-y-1">
                    {analysisResult.recommendations.map((rec, index) => (
                      <li key={index} className="text-xs">• {rec}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ) : (
            <div className="space-y-2 text-sm text-foreground/80">
              <p><span className="text-success">●</span> Positive mood trend detected</p>
              <p><span className="text-warning">●</span> Elevated stress during evening</p>
              <p><span className="text-secondary">●</span> Dream symbols suggest creativity</p>
            </div>
          )}
        </div>
      </div>
    </Card>
  );
}
