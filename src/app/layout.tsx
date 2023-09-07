import Navigation from './Navigation';
import './globals.scss';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Kompassi',
  description: 'Event Management System',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  // TODO lang=
  return (
    <html>
      <body>
        <Navigation />
        {children}
      </body>
    </html>
  );
}
