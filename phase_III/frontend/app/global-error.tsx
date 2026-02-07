'use client';

import { useEffect } from 'react';

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error('Fatal error occurred:', error);
  }, [error]);

  return (
    <html>
      <body>
        <div className="flex flex-col items-center justify-center min-h-screen bg-red-50">
          <h2 className="text-2xl font-bold text-red-800 mb-4">Critical Error!</h2>
          <p className="text-red-600 mb-4">Something went critically wrong.</p>
          <p className="text-red-500 text-sm mb-6">{error.message}</p>
          <button
            onClick={() => reset()}
            className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
          >
            Try Again
          </button>
        </div>
      </body>
    </html>
  );
}