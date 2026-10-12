import { Outlet } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";

const links = [
  { to: "/employee", label: "Dashboard", icon: "dashboard", end: true },
  { to: "/employee/chatbot", label: "HR Policy Chat", icon: "chat" },
  { to: "/employee/salary", label: "My Salary", icon: "salary" },
  { to: "/employee/leave", label: "Apply Leave", icon: "leave" },
  { to: "/employee/profile", label: "My Profile", icon: "profile" },
];

export default function EmployeeLayout({ title }) {
  return (
    <div className="flex min-h-screen bg-canvas">
      <Sidebar links={links} />
      <div className="flex-1 min-w-0">
        <Topbar title={title} />
        <main className="p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
