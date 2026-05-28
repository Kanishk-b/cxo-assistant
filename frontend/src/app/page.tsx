"use client"; // This tells Next.js to enable interactive React state

import { useState, useEffect } from "react";

export default function Home() {
  // 1. React State to hold our data and track user interactions
  const [briefing, setBriefing] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [completedTasks, setCompletedTasks] = useState<string[]>([]);

  // 2. Fetch the data when the component loads
  useEffect(() => {
    const fetchBriefing = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/v1/morning-briefing");
        const result = await response.json();
        setBriefing(result.data);
      } catch (error) {
        console.error("Failed to fetch briefing:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchBriefing();
  }, []);

  // 3. The function that runs when you click a checkbox
  const handleCheck = (taskName: string) => {
    if (completedTasks.includes(taskName)) {
      setCompletedTasks(completedTasks.filter((t) => t !== taskName)); // Uncheck
    } else {
      setCompletedTasks([...completedTasks, taskName]); // Check
    }
  };

  const today = new Date().toLocaleDateString("en-US", { weekday: 'long', month: 'long', day: 'numeric' });

  // 4. Show a loading state while the AI is drafting
  if (isLoading) {
    return (
      <main className="min-h-screen flex flex-col items-center justify-center font-sans bg-gray-50">
        <div className="text-4xl mb-4 animate-bounce">🧠</div>
        <h2 className="text-xl font-semibold text-gray-700 animate-pulse">Claude is drafting your briefing...</h2>
        <p className="text-gray-500 mt-2">Reading live inbox and filtering confidential data</p>
      </main>
    );
  }

  // Fallback if the backend is down
  if (!briefing) {
    return (
      <main className="min-h-screen flex items-center justify-center font-sans">
        <div className="text-red-500 font-semibold p-4 bg-red-50 rounded-lg border border-red-200">
          ❌ Failed to connect to LangGraph Backend. Check terminal.
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen p-8 max-w-4xl mx-auto font-sans">
      <header className="mb-8 border-b pb-4">
        <h1 className="text-3xl font-bold tracking-tight text-gray-900">Morning Briefing</h1>
        <p className="text-gray-500 mt-1">{today}</p>
      </header>

      <div className="space-y-6">
        
        {/* Dynamic Shape of the Day */}
        <section className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h2 className="text-lg font-semibold text-gray-800 mb-3 flex items-center gap-2">
            🌅 Shape of the Day
          </h2>
          <p className="text-gray-600 leading-relaxed">
            {briefing.shape_of_the_day}
          </p>
        </section>

        {/* Dynamic Critical Attention Items */}
        <section className="bg-red-50 p-6 rounded-xl shadow-sm border border-red-100">
          <h2 className="text-lg font-semibold text-red-800 mb-3 flex items-center gap-2">
            🔥 Critical Attention Items
          </h2>
          <ul className="space-y-2">
            {briefing.critical_attention_items.map((item: string, index: number) => (
              <li key={index} className="flex items-start gap-2 text-red-900 bg-white p-3 rounded-lg border border-red-200 shadow-sm">
                <span className="mt-1 flex-shrink-0">⚠️</span>
                {item}
              </li>
            ))}
          </ul>
        </section>

        {/* Dynamic Open Commitments with Checkboxes */}
        <section className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h2 className="text-lg font-semibold text-gray-800 mb-3 flex items-center gap-2">
            📝 Open Commitments
          </h2>
          <ul className="space-y-3">
            {briefing.open_commitments.map((commitment: any, index: number) => {
              // Check if this specific item is in our completed state array
              const isCompleted = completedTasks.includes(commitment.task);

              return (
                <li 
                  key={index} 
                  // Tailwind magic: smoothly animate opacity and background color when checked
                  className={`flex items-center justify-between p-3 rounded-lg border transition-all duration-300 ${
                    isCompleted ? "opacity-40 bg-gray-100 border-gray-100" : "bg-gray-50 border-gray-200"
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <input 
                      type="checkbox" 
                      checked={isCompleted}
                      onChange={() => handleCheck(commitment.task)}
                      className="w-5 h-5 rounded border-gray-300 text-blue-600 cursor-pointer" 
                    />
                    <span className={`text-gray-700 transition-all ${isCompleted ? "line-through" : ""}`}>
                      {commitment.task}
                    </span>
                  </div>
                  <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                    isCompleted ? "bg-gray-200 text-gray-500" : "bg-orange-100 text-orange-800"
                  }`}>
                    {commitment.urgency} Urgency
                  </span>
                </li>
              );
            })}
          </ul>
        </section>

      </div>
    </main>
  );
}