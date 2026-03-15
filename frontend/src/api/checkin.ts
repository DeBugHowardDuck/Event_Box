import { apiClient } from "./client";

export type CheckInResponse =
  | { result: "ok"; ticket_id: number; order_id: number; used_at: string }
  | { result: "invalid" | "already_used" | "not_active" };

export async function checkinByQr(qr_payload: string) {
  const res = await apiClient.post<CheckInResponse>("/checkin/qr/", { qr_payload });
  return res.data;
}