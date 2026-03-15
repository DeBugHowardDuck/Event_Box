import { apiClient } from "./client";

export type Me = { id: number; email: string; role: string | null };

export async function register(email: string, password: string) {
  const res = await apiClient.post("/auth/register/", { email, password });
  return res.data;
}

export async function login(email: string, password: string) {
  const res = await apiClient.post("/auth/login/", { email, password });
  return res.data;
}

export async function logout() {
  const res = await apiClient.post("/auth/logout/");
  return res.data;
}

export async function me() {
  const res = await apiClient.get<Me>("/auth/me/");
  return res.data;
}