import { useEffect, useState } from "react";
import { Link as RouterLink } from "react-router-dom";
import { fetchEvents, type EventListItem, type Paginated } from "../api/events";
import {
  Container,
  Typography,
  Card,
  CardContent,
  Stack,
  Link,
  Button,
} from "@mui/material";

export function HomePage() {
  const [data, setData] = useState<Paginated<EventListItem> | null>(null);
  const [error, setError] = useState<string>("");
  const [page, setPage] = useState<number>(1);

  useEffect(() => {
    setError("");
    fetchEvents(page)
      .then(setData)
      .catch((e) => setError(e?.message ?? "Request failed"));
  }, [page]);

  return (
    <Container sx={{ py: 4 }}>
      <Typography variant="h4" sx={{ mb: 2 }}>
        Event Box — события
      </Typography>

      {error && <Typography color="error">{error}</Typography>}
      {!data && !error && <Typography>Загрузка…</Typography>}

      {data && (
        <>
          <Typography variant="body2" sx={{ mb: 2 }}>
            Всего: {data.count} • Страница: {page}
          </Typography>

          <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
            <Button
              variant="outlined"
              disabled={!data.previous}
              onClick={() => setPage((p) => Math.max(1, p - 1))}
            >
              Предыдущая
            </Button>
            <Button
              variant="outlined"
              disabled={!data.next}
              onClick={() => setPage((p) => p + 1)}
            >
              Следующая
            </Button>
          </Stack>

          <Stack spacing={2}>
            {data.results.map((ev) => (
              <Card key={ev.id}>
                <CardContent>
                  <Link component={RouterLink} to={`/events/${ev.id}`} underline="hover">
                    <Typography variant="h6">{ev.title}</Typography>
                  </Link>
                  <Typography variant="body2">
                    {ev.venue_type} • {ev.starts_at} → {ev.ends_at}
                  </Typography>
                  <Typography variant="body2">
                    Осталось: {ev.tickets_left} • Sold out: {String(ev.is_sold_out)} • Регистрация закрыта:{" "}
                    {String(ev.is_registration_closed)}
                  </Typography>
                </CardContent>
              </Card>
            ))}
          </Stack>
        </>
      )}
    </Container>
  );
}