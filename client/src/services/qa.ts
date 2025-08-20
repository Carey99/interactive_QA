/**
 * QA Service
 * 
 * This service handles all communication with the backend API for the Q&A system.
 * It provides methods for submitting questions and checking backend health.
 * 
 * Features:
 * - Question submission to backend AI/LLM
 * - Health checks for backend connectivity
 * - Error handling and fallback responses
 * - Environment-based API URL configuration
 */

import { QAResponse } from '@/types/qa';

// Get API URL from environment variables, fallback to localhost for development
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001';

export class QAService {
  /**
   * Submit a question to the backend AI service
   * 
   * @param question - The user's question to be processed
   * @returns Promise<QAResponse> - The AI's response with answer and metadata
   */
  static async askQuestion(question: string): Promise<QAResponse> {
    try {
      // Send POST request to backend with the user's question
      const response = await fetch(`${API_BASE_URL}/api/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      });

      // Check if the request was successful
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // Parse and return the JSON response
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error asking question:', error);
      
      // Return a fallback response when backend is unavailable
      // This ensures the frontend remains functional even without a backend
      return {
        answer: `I apologize, but I'm currently unable to process your question: "${question}". Server is not running.`,
        confidence: 0,
      };
    }
  }

  /**
   * Check if the backend API is available and responding
   * 
   * @returns Promise<boolean> - True if backend is healthy, false otherwise
   */
  static async getHealth(): Promise<boolean> {
    try {
      // Send a simple GET request to the health endpoint
      const response = await fetch(`${API_BASE_URL}/api/health`);
      return response.ok;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  }
}
