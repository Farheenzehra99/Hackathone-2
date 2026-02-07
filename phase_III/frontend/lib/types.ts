// User-related types
export interface User {
  id: string;
  email: string;
  name?: string;
  createdAt: Date;
  updatedAt: Date;
}

// Task-related types
export interface Task {
  id: string;
  userId: string;
  title: string;
  description?: string;
  priority: 'low' | 'medium' | 'high';
  completed: boolean;
  created_at: Date;
  updated_at: Date;
}

// Session-related types
export interface Session {
  userId: string;
  accessToken: string;
  refreshToken: string;
  expiresAt: Date;
  isAuthenticated: boolean;
}

// Form data types
export interface TaskFormData {
  title: string;
  description?: string;
  priority: 'low' | 'medium' | 'high';
}

// Error types
export interface FormErrors {
  title?: string[];
  description?: string[];
  priority?: string[];
  general?: string[];
}

// Toast notification types
export interface ToastNotification {
  id: string;
  title: string;
  description?: string;
  type: 'success' | 'error' | 'warning' | 'info';
  duration?: number;
}

// API response types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}