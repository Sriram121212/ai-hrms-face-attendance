import { Outlet } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";

const links = [
  { to: "/admin", label: "Dashboard", icon: "dashboard", end: true },
  { to: "/admin/employees", label: "Employees", icon: "employees" },
  { to: "/admin/attendance", label: "Attendance", icon: "attendance" },
  { to: "/admin/leaves", label: "Leave Approvals", icon: "leave" },
  { to: "/admin/hr-policy", label: "HR Policy Docs", icon: "chat" },
  { to: "/admin/chatbot", label: "AI Admin Chat", icon: "chat" },
  { to: "/admin/cost-tracker", label: "Cost Tracker", icon: "salary" },
];

export default function AdminLayout({ title }) {
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
