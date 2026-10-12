import { createContext, useContext, useState } from "react";
import { login as apiLogin } from "../api/endpoints";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const token = localStorage.getItem("access_token");
    if (!token) return null;
    return {
      token,
      role: localStorage.getItem("role"),
      name: localStorage.getItem("name"),
      employeeId: localStorage.getItem("employee_id"),
    };
  });

  const login = async (email, password) => {
    const data = await apiLogin(email, password);
    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("role", data.role);
    localStorage.setItem("name", data.name);
    localStorage.setItem("employee_id", data.employee_id);
    setUser({
      token: data.access_token,
      role: data.role,
      name: data.name,
      employeeId: data.employee_id,
    });
    return data;
  };

  const logout = () => {
    localStorage.clear();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
