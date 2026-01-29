'use client';

import { useEffect } from 'react';
import { Button } from '@/components/ui/button';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error('Error occurred:', error);
  }, [error]);

  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] p-8 bg-red-50 rounded-lg border border-red-200">
      <h2 className="text-2xl font-bold text-red-800 mb-4">Something went wrong!</h2>
      <p className="text-red-600 mb-6">{error.message}</p>
      <div className="flex gap-4">
        <Button
          onClick={() => reset()}
          variant="default"
        >
          Try Again
        </Button>
        <Button
          onClick={() => window.location.href = '/'}
          variant="outline"
        >
          Go Home
        </Button>
      </div>
    </div>
  );
}