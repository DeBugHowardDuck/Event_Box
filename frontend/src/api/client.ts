import axios from "axios";

function getCookie(name: string): string | null {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop()!.split(";").shift() ?? null;
  return null;
}

export const apiClient = axios.create({
  baseURL: "/api",
  withCredentials: true,
});

apiClient.interceptors.request.use((config) => {
  const method = (config.method ?? "get").toLowerCase();
  const needsCsrf = ["post", "put", "patch", "delete"].includes(method);

  if (needsCsrf) {
    const csrf = getCookie("csrftoken");
    if (csrf) {
      config.headers = config.headers ?? {};
      config.headers["X-CSRFToken"] = csrf;
    }
  }

  return config;
});