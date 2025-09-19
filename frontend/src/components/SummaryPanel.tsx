import React, { useState, useEffect, useCallback } from 'react';
import { motion } from 'framer-motion';
import { FileText, RefreshCw, Clock, Loader2, AlertCircle } from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { ScrollArea } from './ui/scroll-area';
import { apiService } from '../services/api';

interface SummaryPanelProps {
  sessionId: string;
}

const SummaryPanel: React.FC<SummaryPanelProps> = ({ sessionId }) => {
  const [summary, setSummary] = useState<string>('');
  const [lastUpdated, setLastUpdated] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [hasLoadedOnce, setHasLoadedOnce] = useState(false);

  const fetchSummary = useCallback(async () => {
    if (!sessionId) return;
    
    setIsLoading(true);
    setError('');

    try {
      const response = await apiService.getSummary(sessionId);
      setSummary(response.summary);
      setLastUpdated(new Date().toISOString());
      setHasLoadedOnce(true);
    } catch (error: any) {
      console.error('Error fetching summary:', error);
      setError(error.message || 'Failed to load summary');
      
      // If it's the first load and there's no summary yet, show a helpful message
      if (!hasLoadedOnce) {
        setSummary('No conversation summary available yet. Start chatting to generate a summary.');
        setError('');
      }
    } finally {
      setIsLoading(false);
    }
  }, [sessionId, hasLoadedOnce]);

  // Auto-fetch summary when component mounts or sessionId changes
  useEffect(() => {
    fetchSummary();
  }, [sessionId, fetchSummary]);

  // Auto-refresh summary every 30 seconds when there's an active session
  useEffect(() => {
    if (!sessionId || !hasLoadedOnce) return;

    const interval = setInterval(() => {
      fetchSummary();
    }, 30000); // 30 seconds

    return () => clearInterval(interval);
  }, [sessionId, hasLoadedOnce, fetchSummary]);

  const formatLastUpdated = (timestamp: string) => {
    if (!timestamp) return '';
    
    try {
      const date = new Date(timestamp);
      const now = new Date();
      const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000);
      
      if (diffInSeconds < 60) {
        return 'Just now';
      } else if (diffInSeconds < 3600) {
        const minutes = Math.floor(diffInSeconds / 60);
        return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
      } else if (diffInSeconds < 86400) {
        const hours = Math.floor(diffInSeconds / 3600);
        return `${hours} hour${hours > 1 ? 's' : ''} ago`;
      } else {
        return date.toLocaleDateString();
      }
    } catch (error) {
      return timestamp;
    }
  };

  const handleRefresh = () => {
    fetchSummary();
  };

  return (
    <Card className="h-full flex flex-col">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-xl font-semibold flex items-center gap-2">
            <FileText className="w-6 h-6 text-primary" />
            Conversation Summary
          </CardTitle>
          <Button
            onClick={handleRefresh}
            disabled={isLoading}
            variant="ghost"
            size="icon"
            className="h-8 w-8"
          >
            <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
          </Button>
        </div>
        
        {lastUpdated && (
          <div className="flex items-center gap-1 text-xs text-muted-foreground">
            <Clock className="w-3 h-3" />
            Last updated: {formatLastUpdated(lastUpdated)}
          </div>
        )}
      </CardHeader>
      
      <CardContent className="flex-1 p-4 pt-0">
        <ScrollArea className="h-full">
          <div className="space-y-4">
            {isLoading && !summary ? (
              <div className="flex items-center justify-center py-8">
                <div className="flex items-center gap-2 text-muted-foreground">
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span className="text-sm">Loading summary...</span>
                </div>
              </div>
            ) : error ? (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="p-4 rounded-md bg-destructive/10 border border-destructive/20 text-destructive"
              >
                <div className="flex items-center gap-2">
                  <AlertCircle className="w-4 h-4" />
                  <p className="text-sm font-medium">Unable to load summary</p>
                </div>
                <p className="text-xs mt-1 opacity-80">{error}</p>
                <Button
                  onClick={handleRefresh}
                  variant="outline"
                  size="sm"
                  className="mt-2 text-destructive border-destructive/30 hover:bg-destructive/10"
                >
                  Try Again
                </Button>
              </motion.div>
            ) : summary ? (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="prose prose-sm dark:prose-invert max-w-none"
              >
                <div className="p-4 rounded-md bg-muted/50 border">
                  <p className="text-sm leading-relaxed whitespace-pre-wrap">
                    {summary}
                  </p>
                </div>
              </motion.div>
            ) : (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex items-center justify-center py-8"
              >
                <div className="text-center text-muted-foreground">
                  <FileText className="w-12 h-12 mx-auto mb-3 opacity-50" />
                  <p className="text-sm">No conversation summary available yet.</p>
                  <p className="text-xs mt-1">Start chatting to generate a summary.</p>
                </div>
              </motion.div>
            )}
            
            {/* Additional Info Section */}
            {summary && !error && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.3 }}
                className="mt-6 pt-4 border-t border-border"
              >
                <div className="text-xs text-muted-foreground space-y-1">
                  <p>• Summary updates automatically every 30 seconds</p>
                  <p>• Click the refresh button to update manually</p>
                  <p>• Summary reflects the current conversation context</p>
                </div>
              </motion.div>
            )}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
};

export default SummaryPanel;
