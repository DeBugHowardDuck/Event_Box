import { apiClient } from "./client";

export type Ticket = {
  id: number;
  ticket_type: number;
  code: string;
  qr_payload: string;
  status: string;
  used_at: string | null;
  created_at: string;
};

export type Order = {
  id: number;
  status: string;
  event: number;
  total_amount: string;
  currency: string;
  provider: string;
  created_at: string;
  tickets: Ticket[];
};

export async function createOrder(ticket_type_id: number, qty: number) {
  const res = await apiClient.post<Order>("/orders/", { ticket_type_id, qty });
  return res.data;
}

export type Paginated<T> = {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
};

export async function fetchMyOrders() {
  const res = await apiClient.get<Paginated<Order>>("/orders/my/");
  return res.data.results;
}

export async function fetchMyTickets() {
  const res = await apiClient.get<Paginated<Ticket>>("/tickets/my/");
  return res.data.results;
}