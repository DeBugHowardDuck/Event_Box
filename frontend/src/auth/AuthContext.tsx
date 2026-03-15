import React, { createContext, useContext, useEffect, useMemo, useState } from "react";
import type { Me } from "../api/auth";
import { me as apiMe, logout as apiLogout } from "../api/auth";
import { ensureCsrfCookie } from "../api/csrf";

type AuthState = {
  user: Me | null;
  isLoading: boolean;
  refresh: () => Promise<void>;
  logout: () => Promise<void>;
};

const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<Me | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  async function refresh() {
    setIsLoading(true);
    try {
      const u = await apiMe();
      setUser(u);
    } catch {
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  }

  async function logout() {
    await ensureCsrfCookie();
    await apiLogout();
    setUser(null);
  }

  useEffect(() => {
    refresh();
  }, []);

  const value = useMemo(() => ({ user, isLoading, refresh, logout }), [user, isLoading]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
  return ctx;
}