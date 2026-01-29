'use client';

import { createContext, useContext, useEffect, useState } from 'react';
import { useToast } from '../../hooks/use-toast';

interface ErrorContextType {
  addError: (error: Error) => void;
  clearErrors: () => void;
  errors: Error[];
}

const ErrorContext = createContext<ErrorContextType | undefined>(undefined);

export function ErrorProvider({ children }: { children: React.ReactNode }) {
  const [errors, setErrors] = useState<Error[]>([]);
  const { toast } = useToast();

  const addError = (error: Error) => {
    setErrors(prev => [...prev, error]);

    // Show toast notification for the error
    toast({
      title: 'Error',
      description: error.message || 'An unexpected error occurred',
      variant: 'destructive',
    });
  };

  const clearErrors = () => {
    setErrors([]);
  };

  // Log errors to console in development
  useEffect(() => {
    if (process.env.NODE_ENV === 'development') {
      errors.forEach(error => {
        console.error('Global error caught:', error);
      });
    }
  }, [errors]);

  return (
    <ErrorContext.Provider value={{ addError, clearErrors, errors }}>
      {children}
    </ErrorContext.Provider>
  );
}

export function useError() {
  const context = useContext(ErrorContext);
  if (context === undefined) {
    throw new Error('useError must be used within an ErrorProvider');
  }
  return context;
}