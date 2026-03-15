import { apiClient } from "./client";

export type TicketType = {
  id: number;
  event: number;
  name: string;
  price: string;
  currency: string;
  quota: number;
  sales_start: string | null;
  sales_end: string | null;
  is_active: boolean;
};

export async function fetchTicketTypes(eventId: number) {
  const res = await apiClient.get("/ticket-types/", { params: { event: eventId } });
  const data: any = res.data;
  return (data.results ?? data) as TicketType[];
}

export async function createTicketType(payload: Omit<TicketType, "id">) {
  const res = await apiClient.post("/ticket-types/", payload);
  return res.data;
}