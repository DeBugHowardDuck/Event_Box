import { apiClient } from "./client";

export type CreatePaymentResponse = {
  order_id: number;
  provider_payment_id: string;
  status: string;
  confirmation_url: string;
};

export async function createYooKassaPayment(order_id: number) {
  const res = await apiClient.post<CreatePaymentResponse>("/payments/yookassa/create/", { order_id });
  return res.data;
}