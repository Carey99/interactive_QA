/**
 * QAInterface Component
 * 
 * This is the main chat interface for the Interactive Q&A System.
 * It provides a modern chat UI where users can ask questions and receive AI-generated responses.
 * 
 * Features:
 * - Real-time chat interface with message history
 * - Connection status monitoring (online/offline)
 * - Loading states and error handling
 * - Responsive design with dark mode support
 * - TypeScript for type safety
 */

'use client';

import { useState, useEffect } from 'react';
import { Send, Bot, User, Loader2, Wifi, WifiOff } from 'lucide-react';
import { Message } from '@/types/qa';
import { QAService } from '@/services/qa';

export default function QAInterface() {
  // State management for the chat interface
  const [messages, setMessages] = useState<Message[]>([]); // Array to store all chat messages
  const [input, setInput] = useState(''); // Current user input in the text field
  const [isLoading, setIsLoading] = useState(false); // Loading state while waiting for AI response
  const [isOnline, setIsOnline] = useState(true); // Backend connection status

  /**
   * Health Check Effect
   * Runs once when component mounts to check if the backend API is available
   * Also sets up periodic health checks every 30 seconds
   */
  useEffect(() => {
    const checkHealth = async () => {
      const health = await QAService.getHealth();
      setIsOnline(health);
    };
    
    // Initial health check
    checkHealth();
    
    // Set up periodic health checks every 30 seconds
    const healthInterval = setInterval(checkHealth, 30000);
    
    // Cleanup interval on component unmount
    return () => clearInterval(healthInterval);
  }, []);

  /**
   * Handle Form Submission
   * Processes user questions and manages the conversation flow
   * 
   * @param e - Form submission event
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Prevent submission if input is empty or we're already loading
    if (!input.trim() || isLoading) return;

    // Create user message object
    const userMessage: Message = {
      id: Date.now().toString(), // Simple ID generation using timestamp
      text: input,
      isUser: true,
      timestamp: new Date(),
    };

    // Add user message to chat immediately for better UX
    setMessages(prev => [...prev, userMessage]);
    
    // Store input value and clear the input field
    const currentInput = input;
    setInput('');
    setIsLoading(true); // Show loading indicator

    try {
      // Send question to backend AI service
      const response = await QAService.askQuestion(currentInput);
      
      // If we got a response with confidence > 0, backend is working
      if (response.confidence && response.confidence > 0) {
        setIsOnline(true);
      }
      
      // Create AI response message
      const botMessage: Message = {
        id: (Date.now() + 1).toString(), // Ensure unique ID
        text: response.answer,
        isUser: false,
        timestamp: new Date(),
      };
      
      // Add AI response to chat
      setMessages(prev => [...prev, botMessage]);
    } catch {
      // If we get an error, mark as offline
      setIsOnline(false);
      
      // Handle any errors that occur during question processing
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: "I'm sorry, I encountered an error while processing your question. Please try again.",
        isUser: false,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      // Always stop loading indicator, whether success or error
      setIsLoading(false);
    }
  };

  return (
    /* Main Chat Container - Matrix-themed design */
    <div className="max-w-4xl mx-auto matrix-card rounded-lg overflow-hidden font-mono">
      
      {/* Chat Header - Matrix command line style */}
      <div className="bg-black border-b border-green-500 px-6 py-4">
        <div className="flex items-center justify-between">
          {/* AI Assistant Title with Matrix styling */}
          <h2 className="text-xl font-bold text-green-400 flex items-center gap-2 matrix-glow">
            <Bot size={24} className="text-green-400" />
            <span className="font-mono tracking-wide">job startup AI</span>
          </h2>
          
          {/* Connection Status Indicator - Matrix style */}
          <div className="flex items-center gap-2">
            {isOnline ? (
              <div className="flex items-center gap-1 text-green-400 matrix-glow">
                <Wifi size={16} />
                <span className="text-sm font-mono tracking-wide">CONNECTED</span>
              </div>
            ) : (
              <div className="flex items-center gap-1 text-red-400 animate-pulse">
                <WifiOff size={16} />
                <span className="text-sm font-mono tracking-wide">DISCONNECTED</span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Messages Container - Matrix terminal style */}
      <div className="h-96 overflow-y-auto p-6 space-y-4 bg-black bg-opacity-90">
        {messages.length === 0 ? (
          /* Welcome Message - Matrix boot sequence style */
          <div className="text-center text-green-400 mt-12 font-mono">
            <Bot size={48} className="mx-auto mb-4 text-green-400 matrix-glow animate-pulse" />
            <div className="space-y-2">
              <p className="text-lg matrix-glow">{'> NEURAL INTERFACE INITIALIZED'}</p>
              <p className="text-sm text-green-300">{'> AWAITING USER INPUT...'}</p>
              <p className="text-xs text-green-500 opacity-70">{'> TYPE YOUR QUERY TO ACCESS THE MATRIX'}</p>
            </div>
          </div>
        ) : (
          /* Message List - Terminal-style chat messages */
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex items-start gap-3 ${
                // User messages align to the right, AI messages to the left
                message.isUser ? 'flex-row-reverse' : ''
              }`}
            >
              {/* Avatar - Matrix-themed with glow effect */}
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center border ${
                  message.isUser
                    ? 'bg-green-900 border-green-400 text-green-400'
                    : 'bg-black border-green-500 text-green-400'
                } matrix-glow`}
              >
                {message.isUser ? <User size={16} /> : <Bot size={16} />}
              </div>
              
              {/* Message Bubble - Terminal window style */}
              <div
                className={`max-w-xs lg:max-w-md px-4 py-2 rounded border font-mono text-sm ${
                  message.isUser
                    ? 'matrix-user-bubble ml-auto' // User messages: green theme
                    : 'matrix-ai-bubble' // AI messages: darker green theme
                }`}
              >
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs text-green-300 opacity-70">
                    {message.isUser ? '> USER:' : '> ORACLE:'}
                  </span>
                </div>
                <p className="text-green-300 leading-relaxed">{message.text}</p>
                <p className="text-xs text-green-500 opacity-60 mt-2 font-mono">
                  {'['}{message.timestamp.toLocaleTimeString()}{']'}
                </p>
              </div>
            </div>
          ))
        )}
        
        {/* Loading Indicator - Matrix processing style */}
        {isLoading && (
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-full flex items-center justify-center bg-black border border-green-500 text-green-400 matrix-glow">
              <Bot size={16} />
            </div>
            <div className="matrix-ai-bubble px-4 py-2 rounded border">
              <div className="flex items-center gap-2">
                <Loader2 size={16} className="animate-spin text-green-400" />
                <span className="text-sm text-green-300 font-mono animate-pulse">
                  {'> PROCESSING QUERY...'}
                </span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Input Form - Matrix command line interface */}
      <div className="border-t border-green-500 bg-black bg-opacity-95 p-4">
        <form onSubmit={handleSubmit} className="flex gap-2">
          {/* Command Line Prompt */}
          <div className="flex items-center text-green-400 font-mono">
            <span className="text-green-300 mr-2">{'>'}</span>
          </div>
          
          {/* Text Input Field - Matrix terminal style */}
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Enter command or query..."
            disabled={isLoading} // Disable input while processing
            className="flex-1 px-4 py-2 bg-black border border-green-500 rounded text-green-400 font-mono placeholder-green-600 focus:outline-none focus:border-green-400 focus:shadow-lg focus:shadow-green-500/50 disabled:opacity-50 matrix-input"
          />
          
          {/* Send Button - Matrix style */}
          <button
            type="submit"
            disabled={!input.trim() || isLoading} // Disable if empty input or loading
            className="px-6 py-2 bg-black border border-green-500 text-green-400 font-mono rounded hover:bg-green-900 hover:border-green-400 hover:shadow-lg hover:shadow-green-500/50 focus:outline-none focus:border-green-400 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 matrix-button transition-all duration-300"
          >
            <Send size={16} />
            <span className="font-mono tracking-wide">EXECUTE</span>
          </button>
        </form>
        
        {/* Matrix-style status line */}
        <div className="mt-2 text-xs text-green-600 font-mono opacity-70">
          {'> READY_FOR_INPUT'}
        </div>
      </div>
    </div>
  );
}
