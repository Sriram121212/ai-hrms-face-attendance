import { useEffect, useState } from "react";

export default function LiveClock({ variant = "light" }) {
  const [now, setNow] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const time = now.toLocaleTimeString("en-IN", { hour12: true });
  const date = now.toLocaleDateString("en-IN", {
    weekday: "short",
    day: "2-digit",
    month: "short",
    year: "numeric",
  });

  const timeColor = variant === "dark" ? "text-white" : "text-ink";
  const dateColor = variant === "dark" ? "text-white/50" : "text-ink-muted";

  return (
    <div className="flex items-baseline gap-3 font-mono">
      <span className={`text-lg tracking-wide ${timeColor}`}>{time}</span>
      <span className={`text-xs uppercase tracking-wider ${dateColor}`}>{date}</span>
    </div>
  );
}
