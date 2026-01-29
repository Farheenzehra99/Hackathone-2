import { NextRequest, NextResponse } from 'next/server';

// Middleware to protect API routes that require authentication
export function middleware(request: NextRequest) {
  const pathname = request.nextUrl.pathname;

  // Check if the current path matches protected API routes
  if (pathname.startsWith('/api/tasks')) {
    // For API routes, check Authorization header
    const authHeader = request.headers.get('authorization');
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return NextResponse.json(
        { success: false, message: 'Authentication required' },
        { status: 401 }
      );
    }
    // Continue with the request if token exists
    return NextResponse.next();
  }

  // Allow the request to continue for other routes
  // Client-side auth protection will be handled in the components
  return NextResponse.next();
}

// Define which paths the middleware should run on
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes except auth)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.svg (favicon file)
     * - auth pages (login, register, etc.)
     */
    '/((?!api/auth|_next/static|_next/image|favicon\\.svg|.*auth.*).*)',
  ],
};