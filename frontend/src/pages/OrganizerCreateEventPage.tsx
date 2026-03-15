import { useState } from "react";
import { Alert, Button, Stack, TextField, Typography, MenuItem } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { createEvent } from "../api/organizer";

export function OrganizerCreateEventPage() {
  const nav = useNavigate();
  const [error, setError] = useState("");
  const [title, setTitle] = useState("");
  const [venueType, setVenueType] = useState<"online" | "offline">("online");
  const [onlineUrl, setOnlineUrl] = useState("");
  const [venueAddress, setVenueAddress] = useState("");
  const [startsAt, setStartsAt] = useState("");
  const [endsAt, setEndsAt] = useState("");

  async function submit() {
    setError("");
    try {
      const payload: any = {
        title,
        venue_type: venueType,
        starts_at: startsAt,
        ends_at: endsAt,
        timezone: "Europe/Moscow",
        status: "draft",
        capacity: 0,
        registration_ends_at: null,
        description: "",
        online_url: venueType === "online" ? onlineUrl : "",
        venue_address: venueType === "offline" ? venueAddress : "",
      };

      await createEvent(payload);
      nav("/organizer/events");
    } catch (e: any) {
      setError(e?.response?.data?.detail ?? JSON.stringify(e?.response?.data) ?? e?.message ?? "Failed");
    }
  }

  return (
    <Stack spacing={2} sx={{ maxWidth: 520 }}>
      <Typography variant="h4">Создать событие</Typography>
      {error && <Alert severity="error">{error}</Alert>}

      <TextField label="Название" value={title} onChange={(e) => setTitle(e.target.value)} />

      <TextField select label="Тип" value={venueType} onChange={(e) => setVenueType(e.target.value as any)}>

        <MenuItem value="online">online</MenuItem>
        <MenuItem value="offline">offline</MenuItem>
      </TextField>

      {venueType === "online" ? (
        <TextField label="Online URL" value={onlineUrl} onChange={(e) => setOnlineUrl(e.target.value)} placeholder="https://events.com" />
      ) : (
        <TextField label="Адрес" value={venueAddress} onChange={(e) => setVenueAddress(e.target.value)} />
      )}

      <TextField
        label="Начало регистрации"
        value={startsAt}
        onChange={(e) => setStartsAt(e.target.value)}
        placeholder="2026-03-10T19:00"
      />
      <TextField
        label="Окончание регистрации"
        value={endsAt}
        onChange={(e) => setEndsAt(e.target.value)}
        placeholder="2026-03-10T21:00"
      />

      <Button variant="contained" onClick={submit}>
        Создать
      </Button>
    </Stack>
  );
}