'use client';

import * as React from 'react';
import { ThemeProvider as NextThemesProvider } from 'next-themes';
import { ErrorProvider } from '../../components/providers/error-provider';

export function ThemeProvider({ children, ...props }: { children: React.ReactNode; [key: string]: any }) {
  return (
    <NextThemesProvider {...props}>
      {children}
    </NextThemesProvider>
  );
}