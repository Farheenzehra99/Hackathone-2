// Centralized logging utility for the application
interface LogEntry {
  timestamp: Date;
  level: 'info' | 'warn' | 'error' | 'debug';
  message: string;
  context?: Record<string, any>;
}

class Logger {
  private logs: LogEntry[] = [];
  private maxLogs = 1000; // Keep only the last 1000 logs

  log(level: 'info' | 'warn' | 'error' | 'debug', message: string, context?: Record<string, any>) {
    const logEntry: LogEntry = {
      timestamp: new Date(),
      level,
      message,
      context,
    };

    this.logs.push(logEntry);

    // Keep only the last maxLogs entries
    if (this.logs.length > this.maxLogs) {
      this.logs = this.logs.slice(-this.maxLogs);
    }

    // Log to console in development
    if (process.env.NODE_ENV === 'development') {
      const logMessage = context ? `${message} - Context: ${JSON.stringify(context)}` : message;

      switch (level) {
        case 'info':
          console.info(`[INFO] ${logMessage}`);
          break;
        case 'warn':
          console.warn(`[WARN] ${logMessage}`);
          break;
        case 'error':
          console.error(`[ERROR] ${logMessage}`);
          break;
        case 'debug':
          console.debug(`[DEBUG] ${logMessage}`);
          break;
      }
    }
  }

  info(message: string, context?: Record<string, any>) {
    this.log('info', message, context);
  }

  warn(message: string, context?: Record<string, any>) {
    this.log('warn', message, context);
  }

  error(message: string, context?: Record<string, any>) {
    this.log('error', message, context);
  }

  debug(message: string, context?: Record<string, any>) {
    this.log('debug', message, context);
  }

  getLogs(): LogEntry[] {
    return [...this.logs]; // Return a copy to prevent external mutations
  }

  clearLogs() {
    this.logs = [];
  }

  // Method to export logs (could be sent to external service in production)
  exportLogs(): string {
    return JSON.stringify(this.logs, (key, value) =>
      value instanceof Date ? value.toISOString() : value, 2
    );
  }
}

export const logger = new Logger();

// Error boundary logging integration
export const logError = (error: Error, errorInfo?: React.ErrorInfo) => {
  logger.error(error.message, {
    stack: error.stack,
    componentStack: errorInfo?.componentStack,
  });
};

// API error logging
export const logApiError = (url: string, error: any) => {
  logger.error(`API call failed: ${url}`, {
    error: error.message || error,
    timestamp: new Date().toISOString(),
  });
};

// Unhandled promise rejection logging
if (typeof window !== 'undefined') {
  window.addEventListener('unhandledrejection', (event) => {
    logger.error('Unhandled promise rejection', {
      reason: event.reason,
      promise: event.promise,
    });
  });

  window.addEventListener('error', (event) => {
    logger.error('Unhandled script error', {
      message: event.message,
      filename: event.filename,
      lineno: event.lineno,
      colno: event.colno,
      error: event.error,
    });
  });
}