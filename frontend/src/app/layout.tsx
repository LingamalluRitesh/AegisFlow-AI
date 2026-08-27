import type { Metadata } from 'next';
import './globals.css';
import { Navbar } from '@/components/layout/Navbar';
import { Sidebar } from '@/components/layout/Sidebar';

export const metadata: Metadata = {
  title: 'AegisFlow AI | Streaming ML & Fraud Sentinel',
  description: 'Enterprise Real-Time Streaming ML, Fraud Detection & Recommendation Platform',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="bg-background text-slate-100 min-h-screen flex flex-col">
        <Navbar />
        <div className="flex-1 flex overflow-hidden">
          <Sidebar />
          <main className="flex-1 overflow-y-auto p-6 bg-background/50">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
