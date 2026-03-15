import axios from "axios";

export async function ensureCsrfCookie() {
  await axios.get("/api/events/", { withCredentials: true });
}