import { useEffect, useState } from "react";
import { fetchMyOrders } from "../api/orders";
import type { Order } from "../api/orders";
import { Alert, Card, CardContent, Stack, Typography } from "@mui/material";

export function MyOrdersPage() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchMyOrders()
      .then(setOrders)
      .catch((e) => setError(e?.message ?? "Not authorized?"));
  }, []);

  return (
    <Stack spacing={2}>
      <Typography variant="h4">Мои заказы</Typography>
      {error && <Alert severity="error">{error}</Alert>}

      {orders.map((o) => (
        <Card key={o.id}>
          <CardContent>
            <Typography variant="h6">Order #{o.id}</Typography>
            <Typography variant="body2">status: {o.status}</Typography>
            <Typography variant="body2">
              total: {o.total_amount} {o.currency}
            </Typography>
            <Typography variant="body2">tickets: {o.tickets.length}</Typography>
          </CardContent>
        </Card>
      ))}
    </Stack>
  );
}