// import { useEffect, useRef, useState } from "react";
// import { askHrPolicy } from "../../api/endpoints";
// import { useAuth } from "../../context/AuthContext";
// import { askHrPolicy } from "../../api/endpoints";

// export default function HRPolicyChat() {
//   const [messages, setMessages] = useState([
//     {
//       role: "assistant",
//       content: "Ask me anything about HR policy — leave rules, working hours, benefits, and more.",
//     },
//   ]);
//   const [input, setInput] = useState("");
//   const [loading, setLoading] = useState(false);
//   const scrollRef = useRef(null);

//   useEffect(() => {
//     scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
//   }, [messages, loading]);

//   const handleSend = async (e) => {
//     e.preventDefault();
//     const question = input.trim();
//     if (!question || loading) return;

//     setMessages((prev) => [...prev, { role: "user", content: question }]);
//     setInput("");
//     setLoading(true);

//     try {
//       const data = await askHrPolicy(question);
//       setMessages((prev) => [...prev, { role: "assistant", content: data.answer }]);
//     } catch (err) {
//       setMessages((prev) => [
//         ...prev,
//         {
//           role: "assistant",
//           content:
//             err.response?.data?.detail ||
//             "Something went wrong reaching the HR policy assistant. Try again in a moment.",
//           isError: true,
//         },
//       ]);
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="bg-surface rounded-card shadow-card flex flex-col h-[calc(100vh-160px)]">
//       <div className="px-6 py-4 border-b border-line">
//         <h2 className="font-serif text-lg text-ink">HR Policy Chat</h2>
//         <p className="text-xs text-ink-muted mt-0.5">Answers are sourced from uploaded HR policy documents.</p>
//       </div>

//       <div ref={scrollRef} className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
//         {messages.map((msg, i) => (
//           <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
//             <div
//               className={`max-w-[75%] px-4 py-2.5 rounded-card text-sm whitespace-pre-wrap ${
//                 msg.role === "user"
//                   ? "bg-ink text-white"
//                   : msg.isError
//                   ? "bg-clay-soft text-clay"
//                   : "bg-canvas text-ink"
//               }`}
//             >
//               {msg.content}
//             </div>
//           </div>
//         ))}

//         {loading && (
//           <div className="flex justify-start">
//             <div className="bg-canvas text-ink-muted px-4 py-2.5 rounded-card text-sm flex items-center gap-2">
//               <span className="w-1.5 h-1.5 rounded-full bg-ink-muted animate-pulse-dot" />
//               <span className="w-1.5 h-1.5 rounded-full bg-ink-muted animate-pulse-dot [animation-delay:0.2s]" />
//               <span className="w-1.5 h-1.5 rounded-full bg-ink-muted animate-pulse-dot [animation-delay:0.4s]" />
//             </div>
//           </div>
//         )}
//       </div>

//       <form onSubmit={handleSend} className="px-6 py-4 border-t border-line flex gap-3">
//         <input
//           value={input}
//           onChange={(e) => setInput(e.target.value)}
//           placeholder="e.g. How many casual leaves am I entitled to?"
//           disabled={loading}
//           className="flex-1 px-4 py-2.5 rounded-card border border-line bg-surface text-sm outline-none focus:border-ink transition-colors"
//         />
//         <button
//           type="submit"
//           disabled={loading || !input.trim()}
//           className="bg-signal text-white px-5 py-2.5 rounded-card text-sm font-medium hover:opacity-90 transition-opacity disabled:opacity-40"
//         >
//           Send
//         </button>
//       </form>
//     </div>
//   );
// }



import { useEffect, useRef, useState } from "react";
import { askHrPolicy } from "../../api/endpoints";
import { useAuth } from "../../context/AuthContext";

export default function HRPolicyChat() {
  const { user } = useAuth();
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Ask me anything about HR policy — leave rules, working hours, benefits, and more.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, loading]);

  const handleSend = async (e) => {
    e.preventDefault();
    const question = input.trim();
    if (!question || loading) return;

    setMessages((prev) => [...prev, { role: "user", content: question }]);
    setInput("");
    setLoading(true);

    try {
      const data = await askHrPolicy(question);
      setMessages((prev) => [...prev, { role: "assistant", content: data.answer }]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            err.response?.data?.detail ||
            "Something went wrong reaching the HR policy assistant. Try again in a moment.",
          isError: true,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-surface rounded-card shadow-card flex flex-col h-[calc(100vh-160px)]">
      <div className="px-6 py-4 border-b border-line">
        <h2 className="font-serif text-lg text-ink">Welcome, {user?.name}</h2>
        <p className="text-xs text-ink-muted mt-0.5">HR Policy Chat — answers sourced from uploaded HR policy documents.</p>
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

      <form onSubmit={handleSend} className="px-6 py-4 border-t border-line flex gap-3">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="e.g. How many casual leaves am I entitled to?"
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