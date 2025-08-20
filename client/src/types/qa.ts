/**
 * Type Definitions for Q&A System
 * 
 * This file contains TypeScript type definitions used throughout the Q&A application.
 * These types ensure type safety and provide clear contracts between components.
 */

/**
 * Message interface representing a single chat message
 * Used for both user questions and AI responses in the chat interface
 */
export interface Message {
  id: string;           // Unique identifier for the message
  text: string;         // The actual message content
  isUser: boolean;      // True if message is from user, false if from AI
  timestamp: Date;      // When the message was created
}

/**
 * QAResponse interface representing the AI's response to a question
 * Contains the answer and optional metadata about the response quality
 */
export interface QAResponse {
  answer: string;           // The AI's answer to the user's question
  confidence?: number;      // Optional: AI's confidence level (0-1)
  sources?: string[];       // Optional: Sources used to generate the answer
  processingTime?: number;  // Optional: Time taken to process the question (in ms)
}
