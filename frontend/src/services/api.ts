import axios, { AxiosResponse } from 'axios';

// Types for API responses
export interface ChatMessage {
  id: string;
  content: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

// Import types from your form components
export interface ChildData {
  firstName: string;
  lastName?: string;
  gender?: 'Male' | 'Female' | 'Other' | 'Unknown';
  age?: string[];
  streetAddress?: string;
  parish?: string;
  phone1?: string;
  phone2?: string;
  nationality?: string;
  schoolName?: string;
  gradeLevel?: string;
  livingSituation?: string[];
  vulnerableGroups?: string[];
  region?: string;
}

export interface CategoryData {
  missing_children?: string[];
  violence?: string[];
  trafficking?: string[];
  mental_health?: string[];
  physical_health?: string[];
  accessibility?: string[];
  discrimination_and_exclusion?: string[];
  family_relationships?: string[];
  peer_relationships?: string[];
  education_and_occupation?: string[];
  sexuality?: string[];
  disability?: string[];
  non_counselling_contacts?: string[];
}

export interface SummaryData {
  callSummary: string;
  keepConfidential: boolean;
  locationOfIssue?: string;
  actionTaken?: string[];
  outcomeOfContact?: string;
  repeatCaller?: boolean | null;
  okForCaseWorkerToCall?: boolean | null;
  didTheChildFeelWeSolvedTheirProblem?: boolean | null;
  wouldTheChildRecommendUsToAFriend?: boolean | null;
  didYouDiscussRightsWithTheChild?: boolean | null;
}

export interface FormSubmissionData {
  child: ChildData;
  category: CategoryData;
  summary: SummaryData;
  metadata?: Record<string, any>;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

export interface ChatResponse {
  response: string;
}

export interface AutoFillResponse {
  child?: Record<string, any>;
  category?: Record<string, any>;
  summary?: Record<string, any>;
  metadata?: Record<string, any>;
}

export interface SummaryResponse {
  summary: string;
}

// Configure axios instance
const api = axios.create({
  baseURL: 'http://localhost:8001', // Hardcoded for testing
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  withCredentials: false, // Disable credentials for CORS
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    console.log('Request payload:', config.data);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.data);
    return response;
  },
  (error) => {
    console.error('API Error:', {
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data,
      message: error.message
    });
    return Promise.reject(error);
  }
);

// API Service Class
class ApiService {
  /**
   * Send a message to the chatbot
   * @param sessionId - Current session ID
   * @param message - User message
   * @returns Bot response
   */
  async sendMessage(sessionId: string, message: string): Promise<ChatResponse> {
    try {
      console.log('Sending message:', { sessionId, message });
      
      const payload = {
        sessionId: sessionId,
        message: message
      };

      const response: AxiosResponse<ApiResponse<ChatResponse>> = await api.post('/api/chat', payload);
      
      console.log('Raw response:', response.data);
      
      if (response.data.success && response.data.data) {
        return response.data.data;
      } else {
        throw new Error(response.data.error || response.data.message || 'Failed to send message');
      }
    } catch (err: any) {
      console.error('Error sending message:', {
        status: err.response?.status,
        statusText: err.response?.statusText,
        data: err.response?.data,
        message: err.message
      });
      
      // More specific error handling
      if (err.response?.status === 422) {
        throw new Error('Invalid request format. Please check the message format.');
      } else if (err.response?.status === 404) {
        throw new Error('Chat endpoint not found. Please check if the backend is running.');
      } else if (err.response?.status >= 500) {
        throw new Error('Server error. Please try again later.');
      } else if (err.code === 'ECONNREFUSED' || err.code === 'NETWORK_ERROR') {
        throw new Error('Unable to connect to server. Please check if the backend is running on port 8001.');
      }
      
      throw new Error(err.response?.data?.error || err.response?.data?.message || err.message || 'Failed to send message');
    }
  }

  /**
   * Auto-fill form fields based on conversation context
   * @param sessionId - Current session ID
   * @returns Partial form data to fill
   */
  async autoFill(sessionId: string): Promise<AutoFillResponse> {
    try {
      const response: AxiosResponse<ApiResponse<any>> = await api.post('/api/autofill', {
        sessionId,
      });

      console.log('🔍 AutoFill Response Structure:', {
        success: response.data.success,
        dataKeys: response.data.data ? Object.keys(response.data.data) : 'no data',
        fullData: response.data.data
      });

      if (response.data.success && response.data.data) {
        const rawData = response.data.data;
        if (rawData.summary && typeof rawData.summary === 'object') {
                    Object.assign(rawData, rawData.summary);
                        }
        // Transform flat structure to nested structure
        const transformed: AutoFillResponse = {
          child: {},
          category: {},
          summary: {},
          metadata: {}
        };

        // Define which fields belong to which section
        const childFields = [
          'firstName', 'lastName', 'gender', 'age', 'streetAddress', 
          'parish', 'phone1', 'phone2', 'nationality', 'schoolName', 
          'gradeLevel', 'livingSituation', 'vulnerableGroups', 'region'
        ];

        const summaryFields = [
          'callSummary', 'keepConfidential', 'locationOfIssue', 
          'actionTaken', 'outcomeOfContact', 'repeatCaller', 
          'okForCaseWorkerToCall', 'didTheChildFeelWeSolvedTheirProblem',
          'wouldTheChildRecommendUsToAFriend', 'didYouDiscussRightsWithTheChild'
        ];
        const multiSelectFields = ["locationOfIssue", "vulnerableGroups"];

        // Map flat data to nested structure
       Object.entries(rawData).forEach(([key, value]) => {
  if (childFields.includes(key)) {
    transformed.child![key] = value;
  } else if (summaryFields.includes(key)) {
    if (multiSelectFields.includes(key) && typeof value === "string") {
      transformed.summary![key] = value.split(",").map(v => v.trim());
    } else {
      transformed.summary![key] = value;
    }
  } else if (key === "suggested_categories") {
    transformed.category = value as Record<string, any>;
  } else if (key !== "success" && key !== "message") {
    transformed.metadata![key] = value;
  }
});

        console.log('✅ Transformed Data:', transformed);
        return transformed;
      } else {
        throw new Error(response.data.error || 'Failed to auto-fill form');
      }
    } catch (error: any) {
      console.error('Error auto-filling form:', error);
      throw new Error(error.response?.data?.error || 'Failed to auto-fill form');
    }
  }

  /**
   * Submit form data
   * @param sessionId - Current session ID
   * @param formData - Form data to submit
   * @returns Submission confirmation
   */
  async submitForm(sessionId: string, formData: FormSubmissionData): Promise<{ success: boolean; caseId?: string }> {
    try {
      const response: AxiosResponse<ApiResponse<{ success: boolean; message: string; submissionId: string }>> = await api.post('/api/submitForm', {
        sessionId,
        formData,
      });

      if (response.data.success && response.data.data) {
        return {
          success: response.data.data.success,
          caseId: response.data.data.submissionId,
        };
      } else {
        throw new Error(response.data.error || 'Failed to submit form');
      }
    } catch (error: any) {
      console.error('Error submitting form:', error);
      throw new Error(error.response?.data?.error || 'Failed to submit form');
    }
  }

  /**
   * Get conversation summary
   * @param sessionId - Current session ID
   * @returns Conversation summary
   */
  async getSummary(sessionId: string): Promise<SummaryResponse> {
    try {
      const response: AxiosResponse<ApiResponse<SummaryResponse>> = await api.post('/api/summarize', {
        sessionId,
      });

      if (response.data.success && response.data.data) {
        return response.data.data;
      } else {
        throw new Error(response.data.error || 'Failed to get summary');
      }
    } catch (error: any) {
      console.error('Error getting summary:', error);
      throw new Error(error.response?.data?.error || 'Failed to get summary');
    }
  }

  /**
   * Generate a new session ID
   * @returns New session ID
   */
  generateSessionId(): string {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * Health check to verify backend connection
   * @returns Health status
   */
  async healthCheck(): Promise<{ status: string }> {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      console.error('Health check failed:', error);
      throw new Error('Backend is not reachable');
    }
  }
}

// Export singleton instance
export const apiService = new ApiService();
export default apiService;