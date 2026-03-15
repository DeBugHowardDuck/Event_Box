import { apiClient } from "./client";

export type EventListItem = {
  id: number;
  title: string;
  starts_at: string;
  ends_at: string;
  venue_type: string;
  tickets_left: number;
  is_sold_out: boolean;
  is_registration_closed: boolean;
};

export type TicketType = {
  id: number;
  name: string;
  price: string;
  currency: string;
  quota: number;
  sales_start: string | null;
  sales_end: string | null;
  is_active: boolean;
};

export type EventDetail = {
  id: number;
  title: string;
  description: string;
  cover_image: string | null;
  starts_at: string;
  ends_at: string;
  timezone: string;
  venue_type: string;
  venue_address: string;
  online_url: string;
  status: string;
  capacity: number;
  registration_ends_at: string | null;
  ticket_types: TicketType[];
  tickets_left: number;
  is_sold_out: boolean;
  is_registration_closed: boolean;
};

export type Paginated<T> = {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
};

export async function fetchEvents(page: number = 1) {
  const res = await apiClient.get<Paginated<EventListItem>>("/events/", {
    params: { page },
  });
  return res.data;
}

export async function fetchEvent(id: number) {
  const res = await apiClient.get<EventDetail>(`/events/${id}/`);
  return res.data;
}

export const __debug = "events.ts loaded";