"use client";

import { useState } from "react";

export default function YouTubeSearch({ onChannelAdded }: { onChannelAdded?: () => void }) {
  const [channelId, setChannelId] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(null);
    try {
      // Fetch channel info from backend (which calls YouTube API)
      const res = await fetch(`http://localhost:8000/api/youtube-search/?q=${encodeURIComponent(channelId)}`);
      if (!res.ok) throw new Error("Channel not found");
      const data = await res.json();
      // Use the first result (handles and channel IDs should return unique results)
      if (!data || data.length === 0) throw new Error("Channel not found");
      const found = data[0];
      // Add to saved channels
      const addRes = await fetch("http://localhost:8000/api/youtube-channels/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: found.name, youtube_channel_id: found.youtube_channel_id }),
      });
      if (addRes.status === 409) {
        setError("Channel already saved.");
        return;
      }
      if (!addRes.ok) throw new Error("Failed to add channel");
      setSuccess(`Added channel: ${found.name}`);
      setChannelId("");
      if (onChannelAdded) onChannelAdded();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mb-6" style={{ maxWidth: 400 }}>
      <form onSubmit={handleSubmit} className="flex gap-2 mb-2">
        <input
          type="text"
          value={channelId}
          onChange={(e) => setChannelId(e.target.value)}
          placeholder="Enter YouTube channel ID or handle (@username)..."
          className="border px-2 py-1 rounded w-full"
          autoComplete="off"
          disabled={loading}
        />
        <button type="submit" className="bg-blue-600 text-white px-3 py-1 rounded" disabled={loading || !channelId.trim()}>
          {loading ? "Adding..." : "Add"}
        </button>
      </form>
      {error && <div className="text-red-600 mt-1">{error}</div>}
      {success && <div className="text-green-600 mt-1">{success}</div>}
    </div>
  );
} 