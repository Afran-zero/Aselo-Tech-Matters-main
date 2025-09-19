import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Bot, User, Loader2, AlertCircle } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { ScrollArea } from './ui/scroll-area';

import { apiService, ChatMessage } from '../services/api';

interface ChatbotProps {
  sessionId: string;
  onSessionUpdate?: (sessionId: string) => void;
}

const Chatbot: React.FC<ChatbotProps> = ({ sessionId, onSessionUpdate }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      content: 'Hello! I\'m here to help you with your inquiry. How can I assist you today?',
      sender: 'bot',
      timestamp: new Date(),
    },
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [connectionError, setConnectionError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Focus input on mount and test connection
  useEffect(() => {
    inputRef.current?.focus();
    testConnection();
  }, []);

  // Test backend connection
  const testConnection = async () => {
    try {
      await apiService.healthCheck();
      setConnectionError(null);
      console.log('Backend connection successful');
    } catch (error) {
      console.error('Backend connection failed:', error);
      setConnectionError('Cannot connect to backend server. Please ensure it\'s running on port 8001.');
    }
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      content: inputMessage.trim(),
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    const currentMessage = inputMessage.trim();
    setInputMessage('');
    setIsLoading(true);
    setConnectionError(null);

    try {
      console.log('Sending message with sessionId:', sessionId);
      console.log('Message content:', currentMessage);
      
      const response = await apiService.sendMessage(sessionId, currentMessage);
      console.log('Received response:', response);

      const botMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        content: response?.response || 'Sorry, I could not get a response.',
        sender: 'bot',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error: any) {
      console.error('Error sending message:', error);
      
      let errorContent = 'Sorry, I encountered an error. Please try again.';
      
      if (error.message.includes('connect to server') || error.message.includes('ECONNREFUSED')) {
        errorContent = 'Cannot connect to the server. Please check if the backend is running.';
        setConnectionError(errorContent);
      } else if (error.message.includes('Invalid request format')) {
        errorContent = 'Message format error. Please try a different message.';
      } else if (error.message.includes('Server error')) {
        errorContent = 'Server is experiencing issues. Please try again in a moment.';
      } else if (error.message) {
        errorContent = `Error: ${error.message}`;
      }

      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        content: errorContent,
        sender: 'bot',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      inputRef.current?.focus();
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const formatTime = (timestamp: Date) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const handleRetryConnection = () => {
    setConnectionError(null);
    testConnection();
  };

  return (
    <Card className="h-full flex flex-col">
      <CardHeader className="pb-3">
        <CardTitle className="text-xl font-semibold flex items-center gap-2">
          <Bot className="w-6 h-6 text-primary" />
          Chat Assistant
          {connectionError && (
            <AlertCircle className="w-5 h-5 text-red-500" />
          )}
        </CardTitle>
        {connectionError && (
          <div className="mt-2 p-3 bg-red-50 border border-red-200 rounded-md flex items-center justify-between">
            <div className="flex items-center gap-2">
              <AlertCircle className="h-4 w-4 text-red-500" />
              <span className="text-sm text-red-700">{connectionError}</span>
            </div>
            <Button 
              variant="outline" 
              size="sm" 
              onClick={handleRetryConnection}
              className="ml-2 text-red-600 border-red-200 hover:bg-red-50"
            >
              Retry
            </Button>
          </div>
        )}
      </CardHeader>
      
      <CardContent className="flex-1 flex flex-col p-4 pt-0">
        {/* Messages Area */}
        <ScrollArea className="flex-1 pr-4">
          <div className="space-y-4">
            <AnimatePresence>
              {messages.map((message) => (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3 }}
                  className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[80%] rounded-lg px-4 py-3 ${
                      message.sender === 'user'
                        ? 'bg-primary text-primary-foreground'
                        : 'bg-muted text-muted-foreground'
                    }`}
                  >
                    <div className="flex items-start gap-2">
                      {message.sender === 'bot' && (
                        <Bot className="w-4 h-4 mt-0.5 flex-shrink-0" />
                      )}
                      {message.sender === 'user' && (
                        <User className="w-4 h-4 mt-0.5 flex-shrink-0" />
                      )}
                      <div className="flex-1">
                        <p className="text-sm leading-relaxed whitespace-pre-wrap">
                          {message.content}
                        </p>
                        <p className={`text-xs mt-1 opacity-70`}>
                          {formatTime(message.timestamp)}
                        </p>
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
            
            {/* Loading Indicator */}
            {isLoading && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex justify-start"
              >
                <div className="bg-muted text-muted-foreground rounded-lg px-4 py-3">
                  <div className="flex items-center gap-2">
                    <Bot className="w-4 h-4" />
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span className="text-sm">Typing...</span>
                  </div>
                </div>
              </motion.div>
            )}
            
            <div ref={messagesEndRef} />
          </div>
        </ScrollArea>

        {/* Input Area */}
        <div className="mt-4 flex gap-2">
          <Input
            ref={inputRef}
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            disabled={isLoading}
            className="flex-1"
          />
          <Button
            onClick={handleSendMessage}
            disabled={!inputMessage.trim() || isLoading}
            size="icon"
          >
            {isLoading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </Button>
        </div>

        {/* Debug Info (remove in production) */}
        <div className="mt-2 text-xs text-gray-500">
          Session ID: {sessionId}
        </div>
      </CardContent>
    </Card>
  );
};

export default Chatbot;