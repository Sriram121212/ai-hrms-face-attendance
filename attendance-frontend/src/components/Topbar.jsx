import LiveClock from "./LiveClock";

export default function Topbar({ title }) {
  return (
    <header className="flex items-center justify-between bg-surface border-b border-line px-8 py-4 sticky top-0 z-10">
      <h1 className="font-serif text-xl text-ink">{title}</h1>
      <LiveClock />
    </header>
  );
}
