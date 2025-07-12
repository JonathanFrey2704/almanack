import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Almanack",
  description: "A Next.js website",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
