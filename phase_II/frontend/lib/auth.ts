// Utility functions for JWT token handling

// Store JWT token
export const storeToken = (token: string, type: 'access' | 'refresh' = 'access'): void => {
  if (typeof window !== 'undefined') {
    localStorage.setItem(`${type}Token`, token);
  }
};

// Retrieve JWT token
export const getToken = (type: 'access' | 'refresh' = 'access'): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem(`${type}Token`);
  }
  return null;
};

// Remove JWT token
export const removeToken = (type: 'access' | 'refresh' = 'access'): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem(`${type}Token`);
  }
};

// Check if JWT token exists
export const hasToken = (type: 'access' | 'refresh' = 'access'): boolean => {
  return !!getToken(type);
};

// Decode JWT token payload
export const decodeToken = (token: string): any => {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );

    return JSON.parse(jsonPayload);
  } catch (error) {
    console.error('Error decoding token:', error);
    return null;
  }
};

// Check if JWT token is expired
export const isTokenExpired = (token: string): boolean => {
  try {
    const payload = decodeToken(token);
    if (!payload || !payload.exp) {
      return true;
    }

    const currentTime = Math.floor(Date.now() / 1000);
    return payload.exp < currentTime;
  } catch (error) {
    console.error('Error checking token expiration:', error);
    return true;
  }
};

// Get token expiration time
export const getTokenExpiration = (token: string): Date | null => {
  try {
    const payload = decodeToken(token);
    if (!payload || !payload.exp) {
      return null;
    }

    return new Date(payload.exp * 1000);
  } catch (error) {
    console.error('Error getting token expiration:', error);
    return null;
  }
};

// Set up automatic token refresh
export const setupTokenRefresh = (refreshCallback: () => Promise<boolean>): void => {
  // Check token validity periodically
  setInterval(async () => {
    const token = getToken('access');
    if (token && isTokenExpired(token)) {
      await refreshCallback();
    }
  }, 60000); // Check every minute
};

// Get current auth session
export const getAuthSession = async (): Promise<any> => {
  // In a real Next.js app with server components, you'd use cookies or headers
  // For this implementation, we'll simulate server-side session checking

  // Since this is a server component, we can't directly access localStorage
  // We'll need to pass the token from a client component or use a different approach
  // For now, returning a mock session to satisfy the layout
  const token = typeof window !== 'undefined' ? localStorage.getItem('accessToken') : null;

  if (!token || isTokenExpired(token)) {
    return null;
  }

  try {
    const payload = decodeToken(token);
    return {
      user: {
        id: payload.userId || 'unknown',
        email: payload.email || 'unknown@example.com',
        name: payload.name || 'Unknown User',
      },
      expiresAt: payload.exp ? new Date(payload.exp * 1000) : null,
    };
  } catch (error) {
    console.error('Error getting auth session:', error);
    return null;
  }
};