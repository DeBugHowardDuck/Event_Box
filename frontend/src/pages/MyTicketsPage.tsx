import { useEffect, useState } from "react";
import { fetchMyTickets } from "../api/orders";
import type { Ticket } from "../api/orders";
import { Alert, Card, CardContent, Stack, Typography } from "@mui/material";
import { QRCodeCanvas } from "qrcode.react";

export function MyTicketsPage() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchMyTickets()
      .then(setTickets)
      .catch((e) => setError(e?.message ?? "Not authorized?"));
  }, []);

  return (
    <Stack spacing={2}>
      <Typography variant="h4">Мои билеты</Typography>
      {error && <Alert severity="error">{error}</Alert>}

      {tickets.map((t) => (
        <Card key={t.id}>
          <CardContent>
            <Typography variant="h6">Ticket #{t.id}</Typography>
            <Typography variant="body2">status: {t.status}</Typography>
            <Typography variant="body2">payload: {t.qr_payload}</Typography>
              <div style={{ marginTop: 12 }}>
    <QRCodeCanvas value={t.qr_payload} size={140} />
  </div>
          </CardContent>
        </Card>
      ))}
    </Stack>
  );
}