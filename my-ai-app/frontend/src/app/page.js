"use client";
import { useState } from 'react';

export default function Home() {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");

  const handleSend = async () => {
    // IMPORTANT: Replace this URL with your Railway URL after deployment
    const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";
    
    const res = await fetch(`${BACKEND_URL}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: input }),
    });
    const data = await res.json();
    setResponse(data.response);
  };

  return (
    <div className="p-10">
      <h1 className="text-2xl font-bold">AI Project Live</h1>
      <input 
        className="border p-2 mr-2 text-black"
        value={input} 
        onChange={(e) => setInput(e.target.value)} 
        placeholder="Ask something..."
      />
      <button onClick={handleSend} className="bg-blue-500 text-white p-2">Send</button>
      <p className="mt-4">Reply: {response}</p>
    </div>
  );
}