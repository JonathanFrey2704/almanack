'use client';

import { useState } from "react";
import YouTubeSearch from "../youtube/YouTubeSearch";
import YouTubeChannelList from "../youtube/YouTubeChannelList";

export default function Home() {
  const [refresh, setRefresh] = useState(0);

  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-8">
      <YouTubeSearch onChannelAdded={() => setRefresh((r) => r + 1)} />
      <YouTubeChannelList key={refresh} />
    </main>
  );
}
