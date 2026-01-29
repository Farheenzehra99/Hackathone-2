import { z } from 'zod';

// User validation schemas
export const userSchema = z.object({
  id: z.string().min(1, 'ID is required'),
  email: z.string().email('Must be a valid email'),
  name: z.string().min(1, 'Name is required').max(50, 'Name must be less than 50 characters').optional(),
});

export const signUpSchema = z.object({
  name: z.string().min(1, 'Name is required').max(50, 'Name must be less than 50 characters'),
  email: z.string().email('Must be a valid email'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

export const signInSchema = z.object({
  email: z.string().email('Must be a valid email'),
  password: z.string().min(1, 'Password is required'),
});

// Task validation schemas
export const taskSchema = z.object({
  id: z.string().min(1, 'Task ID is required'),
  userId: z.string().min(1, 'User ID is required'),
  title: z.string().min(1, 'Title is required').max(100, 'Title must be less than 100 characters'),
  description: z.string().max(500, 'Description must be less than 500 characters').optional(),
  priority: z.enum(['low', 'medium', 'high'], {
    required_error: 'Priority is required',
    invalid_type_error: 'Priority must be low, medium, or high',
  }),
  completed: z.boolean(),
  createdAt: z.date(),
  updatedAt: z.date(),
});

export const taskFormDataSchema = z.object({
  title: z.string().min(1, 'Title is required').max(100, 'Title must be less than 100 characters'),
  description: z.string().max(500, 'Description must be less than 500 characters').optional(),
  priority: z.enum(['low', 'medium', 'high'], {
    required_error: 'Priority is required',
    invalid_type_error: 'Priority must be low, medium, or high',
  }),
});

// Session validation schemas
export const sessionSchema = z.object({
  userId: z.string().min(1, 'User ID is required'),
  accessToken: z.string().min(1, 'Access token is required'),
  refreshToken: z.string().min(1, 'Refresh token is required'),
  expiresAt: z.date(),
  isAuthenticated: z.boolean(),
});