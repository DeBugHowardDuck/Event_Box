import { useEffect, useState } from "react";
import { Alert, Button, Card, CardContent, Stack, Typography } from "@mui/material";
import { Link as RouterLink } from "react-router-dom";
import { apiClient } from "../api/client";
import type { EventListItem, Paginated } from "../api/events";
import { publishEvent } from "../api/organizer";
import { Link } from "@mui/material";

export function OrganizerEventsPage() {
  const [data, setData] = useState<Paginated<EventListItem> | null>(null);
  const [error, setError] = useState("");

  async function load() {
    setError("");
    try {
      const res = await apiClient.get<Paginated<EventListItem>>("/organizer/events/");
      setData(res.data);
    } catch (e: any) {
      setError(e?.response?.data?.detail ?? e?.message ?? "Failed");
    }
  }

  useEffect(() => {
    load();
  }, []);

  return (
    <Stack spacing={2}>
      <Typography variant="h4">Организатор — мои события</Typography>
      {error && <Alert severity="error">{error}</Alert>}

      <Button component={RouterLink} to="/organizer/events/new" variant="contained">
        Создать событие
      </Button>

      {data && (
        <Stack spacing={2}>
{data.results.map((ev) => (
  <Card key={ev.id}>
    <CardContent>
      <Link component={RouterLink} to={`/organizer/events/${ev.id}`} underline="hover">
        <Typography variant="h6">{ev.title}</Typography>
      </Link>

      <Typography variant="body2">
        {ev.venue_type} • {ev.starts_at} → {ev.ends_at}
      </Typography>
      <Typography variant="body2">
        status: {ev.status}
      </Typography>

      {ev.status === "draft" && (
        <Button
          sx={{ mt: 1 }}
          variant="outlined"
          onClick={async () => {
            await publishEvent(ev.id);
            await load();
          }}
        >
          Опубликовать
        </Button>
      )}
    </CardContent>
  </Card>
))}
        </Stack>
      )}
    </Stack>
  );
}