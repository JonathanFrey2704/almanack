'use client';

import { useState, useEffect } from 'react';

export default function Home() {
  const [message, setMessage] = useState<string>('Loading...');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHello = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/hello');
        const data = await response.json();
        setMessage(data.message);
      } catch (error) {
        console.error('Error fetching from API:', error);
        setMessage('Error connecting to backend');
      } finally {
        setLoading(false);
      }
    };

    fetchHello();
  }, []);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <p className="text-2xl font-semibold">
        {loading ? 'Loading...' : message}
      </p>
    </div>
  );
}
