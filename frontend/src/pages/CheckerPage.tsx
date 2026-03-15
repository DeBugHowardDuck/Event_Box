import { useState } from "react";
import { Alert, Button, Stack, TextField, Typography } from "@mui/material";
import { checkinByQr } from "../api/checkin";

export function CheckerPage() {
  const [payload, setPayload] = useState("");
  const [result, setResult] = useState<string>("");
  const [severity, setSeverity] = useState<"success" | "info" | "warning" | "error">("info");

  async function check() {
    setResult("");
    try {
      const r = await checkinByQr(payload);
      if (r.result === "ok") {
        setSeverity("success");
        setResult(`OK: ticket_id=${r.ticket_id}, order_id=${r.order_id}`);
      } else if (r.result === "already_used") {
        setSeverity("warning");
        setResult("Уже использован");
      } else if (r.result === "not_active") {
        setSeverity("warning");
        setResult("Не активен (не оплачен/возврат)");
      } else {
        setSeverity("error");
        setResult("Неверный QR");
      }
    } catch (e: any) {
      setSeverity("error");
      setResult(e?.response?.data?.detail ?? e?.message ?? "Ошибка запроса");
    }
  }

  return (
    <Stack spacing={2}>
      <Typography variant="h4">Checker</Typography>
      <TextField
        label="QR payload"
        value={payload}
        onChange={(e) => setPayload(e.target.value)}
        placeholder="event_box:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
      />
      <Button variant="contained" onClick={check} disabled={!payload}>
        Проверить
      </Button>
      {result && <Alert severity={severity}>{result}</Alert>}
    </Stack>
  );
}