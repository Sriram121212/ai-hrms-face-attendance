import api from "./client";

// ---- Auth ----
export const login = (email, password) =>
  api.post("/auth/login", { email, password }).then((res) => res.data);

// ---- Employees (admin) ----
export const listEmployees = () => api.get("/admin/employees").then((res) => res.data);
export const registerEmployee = (payload) => api.post("/auth/register", payload).then((res) => res.data);
export const updateEmployee = (id, payload) => api.put(`/admin/employees/${id}`, payload).then((res) => res.data);
export const deactivateEmployee = (id) => api.delete(`/admin/employees/${id}`).then((res) => res.data);

// ---- Attendance ----
export const checkIn = () => api.post("/attendance/checkin").then((res) => res.data);
export const checkOut = () => api.post("/attendance/checkout").then((res) => res.data);
export const myAttendance = () => api.get("/attendance/my").then((res) => res.data);
export const allAttendance = (date) =>
  api.get("/admin/attendance", { params: date ? { date } : {} }).then((res) => res.data);

// ---- Leave ----
export const applyLeave = (payload) => api.post("/leave/apply", payload).then((res) => res.data);
export const myLeaves = () => api.get("/leave/my").then((res) => res.data);
export const allLeaves = (statusFilter) =>
  api.get("/admin/leaves", { params: statusFilter ? { status_filter: statusFilter } : {} }).then((res) => res.data);
export const approveLeave = (id) => api.put(`/admin/leaves/${id}/approve`).then((res) => res.data);
export const rejectLeave = (id) => api.put(`/admin/leaves/${id}/reject`).then((res) => res.data);

// ---- Salary ----
export const generateSalary = (payload) => api.post("/admin/salary/generate", payload).then((res) => res.data);
export const mySalarySlips = () => api.get("/salary/my").then((res) => res.data);
export const employeeSalarySlips = (id) => api.get(`/admin/salary/${id}`).then((res) => res.data);

// ---- HR Policy RAG ----
export const uploadHrPolicy = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return api
    .post("/admin/hr-policy/upload", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    })
    .then((res) => res.data);
};
export const listHrPolicyDocs = () => api.get("/admin/hr-policy/docs").then((res) => res.data);
export const deleteHrPolicyDoc = (id) => api.delete(`/admin/hr-policy/docs/${id}`).then((res) => res.data);
export const askHrPolicy = (question) =>
  api.post("/hr-policy/ask", { question }).then((res) => res.data);


export const askAdminAgent = (question) =>
  api.post("/admin/agent/ask", { question }).then((res) => res.data);



export const getCostSummary = () => api.get("/admin/cost-tracker/summary").then((res) => res.data);
export const getRecentChatLogs = (limit = 30) =>
  api.get("/admin/cost-tracker/logs", { params: { limit } }).then((res) => res.data);