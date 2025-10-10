import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { MessageSquare, FileText, Menu, X } from 'lucide-react';
import Chatbot from './Chatbot';
import FormSection from './forms/FormSection';
import { Button } from './ui/button';
import { apiService } from '../services/api';

const Layout: React.FC = () => {
  const [sessionId, setSessionId] = useState<string>('');
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  // Initialize session on component mount
  useEffect(() => {
    const newSessionId = apiService.generateSessionId();
    setSessionId(newSessionId);
  }, []);

  const handleSessionUpdate = (newSessionId: string) => {
    setSessionId(newSessionId);
  };

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <div className="flex flex-col min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-primary rounded-lg">
                <MessageSquare className="w-6 h-6 text-primary-foreground" />
              </div>
              <div>
                <h1 className="text-2xl font-bold">Aselo Support</h1>
                <p className="text-sm text-muted-foreground">
                  Chat with our assistant and submit your information
                </p>
              </div>
            </div>

            {/* Mobile Menu Button */}
            <Button
              variant="ghost"
              size="icon"
              className="lg:hidden"
              onClick={toggleMobileMenu}
            >
              {isMobileMenuOpen ? (
                <X className="w-5 h-5" />
              ) : (
                <Menu className="w-5 h-5" />
              )}
            </Button>

            {/* Session Info */}
            <div className="hidden lg:flex items-center gap-2 text-xs text-muted-foreground">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              Session: {sessionId.slice(-8)}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-6 flex-1 overflow-auto">
        {/* Desktop Layout */}
        <div className="hidden lg:grid lg:grid-cols-12 gap-6">
          {/* Left Side - Chatbot */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
            className="col-span-5"
          >
            <Chatbot 
              sessionId={sessionId} 
              onSessionUpdate={handleSessionUpdate}
            />
          </motion.div>

          {/* Right Side - Form */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="col-span-7 flex flex-col gap-6"
          >
            {/* Form Section */}
            <div className="flex-1">
              <FormSection sessionId={sessionId} />
            </div>
          </motion.div>
        </div>

        {/* Mobile Layout */}
        <div className="lg:hidden">
          {/* Mobile Navigation */}
          <div className="mb-4 bg-card rounded-lg border border-border overflow-hidden">
            <div className="grid grid-cols-3">
              <button
                onClick={() => setIsMobileMenuOpen(false)}
                className={`p-3 text-center transition-colors ${
                  !isMobileMenuOpen
                    ? 'bg-primary text-primary-foreground'
                    : 'text-muted-foreground hover:bg-muted'
                }`}
              >
                <MessageSquare className="w-5 h-5 mx-auto mb-1" />
                <span className="text-xs">Chat</span>
              </button>
              <button
                onClick={() => setIsMobileMenuOpen(true)}
                className={`p-3 text-center transition-colors ${
                  isMobileMenuOpen
                    ? 'bg-primary text-primary-foreground'
                    : 'text-muted-foreground hover:bg-muted'
                }`}
              >
                <FileText className="w-5 h-5 mx-auto mb-1" />
                <span className="text-xs">Form</span>
              </button>
              <div className="p-3 text-center text-muted-foreground">
                <div className="w-5 h-5 mx-auto mb-1 flex items-center justify-center">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                </div>
                <span className="text-xs">Active</span>
              </div>
            </div>
          </div>

          {/* Mobile Content */}
          <motion.div
            key={isMobileMenuOpen ? 'form' : 'chat'}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className="min-h-[calc(100vh-220px)]"
          >
            {!isMobileMenuOpen ? (
              <Chatbot 
                sessionId={sessionId} 
                onSessionUpdate={handleSessionUpdate}
              />
            ) : (
              <div className="flex flex-col gap-4">
                <div className="flex-1">
                  <FormSection sessionId={sessionId} />
                </div>
              </div>
            )}
          </motion.div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-border bg-card/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="text-sm text-muted-foreground">
              © 2024 Aselo Support Platform. All rights reserved.
            </div>
            <div className="flex items-center gap-4 text-xs text-muted-foreground">
              <span>Session ID: {sessionId.slice(-12)}</span>
              <div className="flex items-center gap-1">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span>Online</span>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout;