import { apiClient } from "./client";

export type OrganizerEvent = {
  id: number;
  title: string;
  starts_at: string;
  ends_at: string;
  venue_type: "online" | "offline";
  status: "draft" | "published" | "canceled";
  capacity: number;
  registration_ends_at: string | null;
};

export async function createEvent(payload: any) {
  const res = await apiClient.post("/events/", payload);
  return res.data;
}

export async function publishEvent(id: number) {
  const res = await apiClient.post(`/events/${id}/publish/`);
  return res.data;
}

export async function fetchMyEvents() {
  const res = await apiClient.get("/events/");
  return res.data;
}