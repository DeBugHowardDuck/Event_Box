import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Alert, Button, Card, CardContent, Stack, TextField, Typography } from "@mui/material";
import { fetchEvent } from "../api/events";
import type { EventDetail } from "../api/events";
import { fetchTicketTypes, createTicketType } from "../api/ticketTypes";
import type { TicketType } from "../api/ticketTypes";
import { publishEvent } from "../api/organizer";

export function OrganizerEventDetailPage() {
  const { id } = useParams();
  const eventId = Number(id);

  const [event, setEvent] = useState<EventDetail | null>(null);
  const [types, setTypes] = useState<TicketType[]>([]);
  const [error, setError] = useState("");

  // форма
  const [name, setName] = useState("Standard");
  const [price, setPrice] = useState("10.00");
  const [currency, setCurrency] = useState("RUB");
  const [quota, setQuota] = useState(50);

  async function load() {
    setError("");
    try {
      const t = await fetchTicketTypes(eventId);
      setTypes(t);
    } catch (e: any) {
      setError(e?.response?.data?.detail ?? e?.message ?? "Failed");
    }
  }

  useEffect(() => {
    load();
  }, [eventId]);

  async function onCreateType() {
    setError("");
    try {
      await createTicketType({
        event: eventId,
        name,
        price,
        currency,
        quota,
        sales_start: null,
        sales_end: null,
        is_active: true,
      });
      await load();
    } catch (e: any) {
      setError(e?.response?.data?.detail ?? JSON.stringify(e?.response?.data) ?? e?.message ?? "Failed");
    }
  }

  return (
    <Stack spacing={2}>
      <Typography variant="h4">Событие #{eventId} — типы билетов</Typography>
      {error && <Alert severity="error">{error}</Alert>}

      <Card>
        <CardContent>
          <Typography variant="h6">Добавить билеты</Typography>
          <Stack spacing={2} sx={{ mt: 2, maxWidth: 480 }}>
            <TextField label="Название" value={name} onChange={(e) => setName(e.target.value)} />
            <TextField label="Цена" value={price} onChange={(e) => setPrice(e.target.value)} />
            <TextField label="Валюта" value={currency} onChange={(e) => setCurrency(e.target.value)} />
            <TextField
              label="Кол-во"
              type="number"
              value={quota}
              onChange={(e) => setQuota(Number(e.target.value))}
              inputProps={{ min: 0 }}
            />
            <Button variant="contained" onClick={onCreateType}>
              Создать Билет
            </Button>
          </Stack>
        </CardContent>
      </Card>

      <Typography variant="h6">Существующие типы</Typography>
      <Stack spacing={1}>
        {types.map((tt) => (
          <Card key={tt.id} variant="outlined">
            <CardContent>
              <Typography variant="subtitle1">{tt.name}</Typography>
              <Typography variant="body2">
                {tt.price} {tt.currency} • quota: {tt.quota} • active: {String(tt.is_active)}
              </Typography>
            </CardContent>
          </Card>
        ))}
      </Stack>
    </Stack>
  );
}