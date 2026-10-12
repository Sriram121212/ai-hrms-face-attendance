import { useEffect, useRef, useState } from "react";
import { askAdminAgent } from "../../api/endpoints";

const EXAMPLE_PROMPTS = [
  "Who was absent today?",
  "Show me pending leave requests",
  "What's the attendance summary for today?",
];

export default function AdminChatbot() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Ask me about attendance, leave requests, or salary — I'll pull real data from the database to answer.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, loading]);

  const send = async (question) => {
    if (!question.trim() || loading) return;

    setMessages((prev) => [...prev, { role: "user", content: question }]);
    setInput("");
    setLoading(true);

    try {
      const data = await askAdminAgent(question);
      setMessages((prev) => [...prev, { role: "assistant", content: data.answer }]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: err.response?.data?.detail || "Something went wrong. Try again in a moment.",
          isError: true,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    send(input);
  };

  return (
    <div className="bg-surface rounded-card shadow-card flex flex-col h-[calc(100vh-160px)]">
      <div className="px-6 py-4 border-b border-line">
        <h2 className="font-serif text-lg text-ink">AI Admin Chat</h2>
        <p className="text-xs text-ink-muted mt-0.5">
          Natural-language questions about attendance, leave, and salary — backed by live database queries.
        </p>
      </div>

      <div ref={scrollRef} className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
            <div
              className={`max-w-[75%] px-4 py-2.5 rounded-card text-sm whitespace-pre-wrap ${
                msg.role === "user"
                  ? "bg-ink text-white"
                  : msg.isError
                  ? "bg-clay-soft text-clay"
                  : "bg-canvas text-ink"
              }`}
            >
              {msg.content}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="bg-canvas text-ink-muted px-4 py-2.5 rounded-card text-sm flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-ink-muted animate-pulse-dot" />
              <span className="w-1.5 h-1.5 rounded-full bg-ink-muted animate-pulse-dot [animation-delay:0.2s]" />
              <span className="w-1.5 h-1.5 rounded-full bg-ink-muted animate-pulse-dot [animation-delay:0.4s]" />
            </div>
          </div>
        )}
      </div>

      {messages.length === 1 && (
        <div className="px-6 pb-3 flex gap-2 flex-wrap">
          {EXAMPLE_PROMPTS.map((p) => (
            <button
              key={p}
              onClick={() => send(p)}
              className="text-xs px-3 py-1.5 rounded-card border border-line text-ink-muted hover:border-ink hover:text-ink transition-colors"
            >
              {p}
            </button>
          ))}
        </div>
      )}

      <form onSubmit={handleSubmit} className="px-6 py-4 border-t border-line flex gap-3">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="e.g. What's Kumar's salary for July 2026?"
          disabled={loading}
          className="flex-1 px-4 py-2.5 rounded-card border border-line bg-surface text-sm outline-none focus:border-ink transition-colors"
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="bg-signal text-white px-5 py-2.5 rounded-card text-sm font-medium hover:opacity-90 transition-opacity disabled:opacity-40"
        >
          Send
        </button>
      </form>
    </div>
  );
}
