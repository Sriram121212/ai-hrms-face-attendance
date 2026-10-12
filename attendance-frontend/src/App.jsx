import { Routes, Route, Navigate } from "react-router-dom";
import { useAuth } from "./context/AuthContext";

import Login from "./pages/Login";
import ProtectedRoute from "./components/ProtectedRoute";

import AdminLayout from "./layouts/AdminLayout";
import AdminDashboard from "./pages/admin/AdminDashboard";
import Employees from "./pages/admin/Employees";
import AttendanceView from "./pages/admin/AttendanceView";
import LeaveApprovals from "./pages/admin/LeaveApprovals";
import AdminChatbot from "./pages/admin/AdminChatbot";
import HrPolicyManagement from "./pages/admin/HrPolicyManagement";

import EmployeeLayout from "./layouts/EmployeeLayout";
import EmployeeDashboard from "./pages/employee/EmployeeDashboard";
import ApplyLeave from "./pages/employee/ApplyLeave";
import MySalary from "./pages/employee/MySalary";
import Profile from "./pages/employee/Profile";
import HRPolicyChat from "./pages/employee/HRPolicyChat";
import CostTracker from "./pages/admin/CostTracker";
export default function App() {
  const { user } = useAuth();

  return (
    <Routes>
      <Route
        path="/login"
        element={user ? <Navigate to={user.role === "admin" ? "/admin" : "/employee"} replace /> : <Login />}
      />

      {/* Admin routes */}
      <Route
        path="/admin"
        element={
          <ProtectedRoute allowedRole="admin">
            <AdminLayout title="Admin Dashboard" />
          </ProtectedRoute>
        }
      >
        <Route index element={<AdminDashboard />} />
        <Route path="employees" element={<Employees />} />
        <Route path="attendance" element={<AttendanceView />} />
        <Route path="leaves" element={<LeaveApprovals />} />
        <Route path="chatbot" element={<AdminChatbot />} />
        <Route path="hr-policy" element={<HrPolicyManagement />} />
        <Route path="cost-tracker" element={<CostTracker />} />
      </Route>

      {/* Employee routes */}
      <Route
        path="/employee"
        element={
          <ProtectedRoute allowedRole="employee">
            <EmployeeLayout title="My Dashboard" />
          </ProtectedRoute>
        }
      >
        <Route index element={<EmployeeDashboard />} />
        <Route path="leave" element={<ApplyLeave />} />
        <Route path="salary" element={<MySalary />} />
        <Route path="profile" element={<Profile />} />
        <Route path="chatbot" element={<HRPolicyChat />} />
      </Route>

      <Route path="*" element={<Navigate to="/login" replace />} />
      

    </Routes>
    
  );
}
