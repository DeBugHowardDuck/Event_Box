import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchEvent } from "../api/events";
import type { EventDetail, TicketType } from "../api/events";
import { createOrder } from "../api/orders";
import { createYooKassaPayment } from "../api/payments";
import {
  Alert,
  Button,
  Card,
  CardContent,
  Divider,
  Stack,
  TextField,
  Typography,
} from "@mui/material";

export function EventDetailPage() {
  const params = useParams();
  const eventId = Number(params.id);

  const [event, setEvent] = useState<EventDetail | null>(null);
  const [error, setError] = useState<string>("");
  const [qty, setQty] = useState<number>(1);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchEvent(eventId)
      .then(setEvent)
      .catch((e) => setError(e?.message ?? "Failed to load event"));
  }, [eventId]);

  async function buy(tt: TicketType) {
    setError("");
    setLoading(true);
    try {
      const order = await createOrder(tt.id, qty);
      const pay = await createYooKassaPayment(order.id);

      window.location.href = pay.confirmation_url;
    } catch (e: any) {
      setError(e?.response?.data?.detail ?? e?.message ?? "Purchase failed");
    } finally {
      setLoading(false);
    }
  }

  if (!event) return <Typography>Загрузка…</Typography>;

  return (
    <Stack spacing={2}>
      <Typography variant="h4">{event.title}</Typography>
      {error && <Alert severity="error">{error}</Alert>}

      <Typography>{event.description}</Typography>

      <Card>
        <CardContent>
          <Typography variant="h6">Билеты</Typography>
          <Typography variant="body2">
            Осталось: {event.tickets_left} • Регистрация закрыта: {String(event.is_registration_closed)}
          </Typography>

          <Divider sx={{ my: 2 }} />

          <Stack direction="row" spacing={2} sx={{ mb: 2 }}>
            <TextField
              label="Кол-во"
              type="number"
              value={qty}
              onChange={(e) => setQty(Number(e.target.value))}
              inputProps={{ min: 1, max: 10 }}
              size="small"
            />
          </Stack>

          <Stack spacing={1}>
            {event.ticket_types.map((tt) => (
              <Card key={tt.id} variant="outlined">
                <CardContent>
                  <Stack direction="row" justifyContent="space-between" alignItems="center">
                    <div>
                      <Typography variant="subtitle1">{tt.name}</Typography>
                      <Typography variant="body2">
                        {tt.price} {tt.currency} • active: {String(tt.is_active)}
                      </Typography>
                    </div>
                    <Button
                      variant="contained"
                      disabled={loading || !tt.is_active || event.is_registration_closed || event.is_sold_out}
                      onClick={() => buy(tt)}
                    >
                      Купить
                    </Button>
                  </Stack>
                </CardContent>
              </Card>
            ))}
          </Stack>
        </CardContent>
      </Card>

      <Typography variant="caption">
      </Typography>
    </Stack>
  );
}