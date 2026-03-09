import './globals.css';

export const metadata = {
  title: 'AutoVuln - Advanced Automated Vulnerability Assessment',
  description: 'Enterprise-grade automated vulnerability assessment platform giving you real-time security insights powered by next-generation engines.',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
