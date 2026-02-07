import { Task, User, ApiResponse } from './types';
import { logger } from './logger';

const API_BASE_URL = '/api';

// Helper function to get auth headers
const getAuthHeaders = (): HeadersInit => {
  const token = localStorage.getItem('accessToken');
  return {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` })
  };
};

// Helper function to handle API responses and extract error messages
const handleApiResponse = async (response: Response): Promise<any> => {
  try {
    const contentType = response.headers.get('content-type');
    let data;

    if (contentType && contentType.includes('application/json')) {
      data = await response.json();
    } else {
      // If response is not JSON, try to get text
      const text = await response.text();
      data = {
        success: response.ok,
        message: text || response.statusText,
        ...(response.ok ? { data: text } : {})
      };
    }

    // Handle different status codes
    if (!response.ok) {
      return {
        success: false,
        error: `HTTP ${response.status}`,
        message: data?.message || response.statusText || 'Request failed',
        status: response.status,
      };
    }

    return {
      success: true,
      data: data?.data || data,
      message: data?.message,
    };
  } catch (error) {
    return {
      success: false,
      error: 'Parse error',
      message: 'Invalid response format',
    };
  }
};

// Authentication API calls
export const authApi = {
  async register(userData: { email: string; password: string; name?: string }): Promise<ApiResponse<User>> {
    try {
      logger.info('Starting user registration', { email: userData.email });

      const response = await fetch(`${API_BASE_URL}/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      const result = await handleApiResponse(response);
      if (result.success) {
        logger.info('User registration successful', { email: userData.email });
      } else {
        logger.error('User registration failed', {
          email: userData.email,
          error: result.message
        });
      }

      return result;
    } catch (error: any) {
      logger.error('Network error during registration', {
        email: userData.email,
        errorMessage: error.message
      });

      return {
        success: false,
        error: 'Network error occurred',
        message: 'Could not connect to the server',
      };
    }
  },

  async login(credentials: { email: string; password: string }): Promise<ApiResponse<{ user: User; accessToken: string; refreshToken: string }>> {
    try {
      logger.info('Starting user login', { email: credentials.email });

      const response = await fetch(`${API_BASE_URL}/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });

      const result = await handleApiResponse(response);

      // Store tokens if login successful
      if (result.success && result.data?.accessToken) {
        localStorage.setItem('accessToken', result.data.accessToken);
        localStorage.setItem('refreshToken', result.data.refreshToken);
        logger.info('User login successful', { email: credentials.email });
      } else if (!result.success) {
        logger.error('User login failed', {
          email: credentials.email,
          error: result.message
        });
      }

      return result;
    } catch (error: any) {
      logger.error('Network error during login', {
        email: credentials.email,
        errorMessage: error.message
      });

      return {
        success: false,
        error: 'Network error occurred',
        message: 'Could not connect to the server',
      };
    }
  },

  async logout(): Promise<ApiResponse<void>> {
    try {
      logger.info('Starting user logout');

      const headers = getAuthHeaders();
      const response = await fetch(`${API_BASE_URL}/logout`, {
        method: 'POST',
        headers,
      });

      const result = await handleApiResponse(response);

      // Clear tokens on successful logout
      if (result.success) {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        logger.info('User logout successful');
      } else {
        logger.error('User logout failed', { error: result.message });
      }

      return result;
    } catch (error: any) {
      logger.error('Network error during logout', { errorMessage: error.message });

      return {
        success: false,
        error: 'Network error occurred',
        message: 'Could not connect to the server',
      };
    }
  },
};

// Task API calls
export const taskApi = {
  async getAllTasks(params?: { page?: number; limit?: number; status?: 'all' | 'completed' | 'pending'; priority?: 'low' | 'medium' | 'high' }): Promise<ApiResponse<Task[]>> {
    try {
      logger.info('Fetching all tasks', { params });

      const queryParams = new URLSearchParams();
      if (params?.page) queryParams.append('page', params.page.toString());
      if (params?.limit) queryParams.append('limit', params.limit.toString());
      if (params?.status) queryParams.append('status', params.status);
      if (params?.priority) queryParams.append('priority', params.priority);

      const queryString = queryParams.toString();
      const url = `${API_BASE_URL}/tasks${queryString ? `?${queryString}` : ''}`;

      const headers = getAuthHeaders();
      const response = await fetch(url, {
        method: 'GET',
        headers,
      });

      const result = await handleApiResponse(response);

      if (result.success) {
        logger.info('Successfully fetched tasks', { count: result.data?.length });
      } else {
        logger.error('Failed to fetch tasks', { error: result.message });
      }

      return result;
    } catch (error: any) {
      logger.error('Network error while fetching tasks', { errorMessage: error.message });

      return {
        success: false,
        error: 'Network error occurred',
        message: 'Could not fetch tasks',
      };
    }
  },

  async createTask(taskData: Omit<Task, 'id' | 'userId' | 'createdAt' | 'updatedAt'>): Promise<ApiResponse<Task>> {
    try {
      const headers = getAuthHeaders();
      const response = await fetch(`${API_BASE_URL}/tasks`, {
        method: 'POST',
        headers,
        body: JSON.stringify(taskData),
      });

      return await handleApiResponse(response);
    } catch (error) {
      return {
        success: false,
        error: 'Network error occurred',
        message: 'Could not create task',
      };
    }
  },

  async updateTask(id: string, taskData: Partial<Task>): Promise<ApiResponse<Task>> {
    try {
      const headers = getAuthHeaders();
      const response = await fetch(`${API_BASE_URL}/tasks/${id}`, {
        method: 'PUT',
        headers,
        body: JSON.stringify(taskData),
      });

      return await handleApiResponse(response);
    } catch (error) {
      return {
        success: false,
        error: 'Network error occurred',
        message: 'Could not update task',
      };
    }
  },

  async deleteTask(id: string): Promise<ApiResponse<void>> {
    try {
      const headers = getAuthHeaders();
      const response = await fetch(`${API_BASE_URL}/tasks/${id}`, {
        method: 'DELETE',
        headers,
      });

      return await handleApiResponse(response);
    } catch (error) {
      return {
        success: false,
        error: 'Network error occurred',
        message: 'Could not delete task',
      };
    }
  },

  async toggleTaskCompletion(id: string, completed: boolean): Promise<ApiResponse<{ id: string; completed: boolean; updatedAt: Date }>> {
    try {
      const headers = getAuthHeaders();
      const response = await fetch(`${API_BASE_URL}/tasks/${id}/complete`, {
        method: 'PATCH',
        headers,
        body: JSON.stringify({ completed }),
      });

      return await handleApiResponse(response);
    } catch (error) {
      return {
        success: false,
        error: 'Network error occurred',
        message: 'Could not update task status',
      };
    }
  },
};

// Utility function to check if user is authenticated
export const isAuthenticated = (): boolean => {
  const token = localStorage.getItem('accessToken');
  return !!token;
};

// Utility function to refresh token if expired
export const refreshToken = async (): Promise<boolean> => {
  const refreshToken = localStorage.getItem('refreshToken');
  if (!refreshToken) {
    return false;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${refreshToken}`
      }
    });

    const result = await handleApiResponse(response);

    if (result.success && result.data?.accessToken) {
      localStorage.setItem('accessToken', result.data.accessToken);
      if (result.data.refreshToken) {
        localStorage.setItem('refreshToken', result.data.refreshToken);
      }
      return true;
    } else {
      // If refresh fails, clear stored tokens
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      return false;
    }
  } catch (error) {
    // If refresh fails, clear stored tokens
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    return false;
  }
};
