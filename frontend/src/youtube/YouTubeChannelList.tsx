"use client";

import { useEffect, useState } from "react";

export default function YouTubeChannelList() {
  const [channels, setChannels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("http://localhost:8000/api/youtube-channels/")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch channels");
        return res.json();
      })
      .then((data) => setChannels(data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading channels...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h2 className="text-xl font-bold mb-2">Saved YouTube Channels</h2>
      <ul className="list-disc pl-5">
        {channels.length === 0 ? (
          <li>No channels saved.</li>
        ) : (
          channels.map((ch: any) => (
            <li key={ch.id}>
              {ch.name} ({ch.youtube_channel_id})
            </li>
          ))
        )}
      </ul>
    </div>
  );
} 