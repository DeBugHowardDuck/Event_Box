import { useState } from "react";
import { useNavigate, Link as RouterLink } from "react-router-dom";
import { Alert, Button, Stack, TextField, Typography, Link } from "@mui/material";
import { ensureCsrfCookie } from "../api/csrf";
import { register, login } from "../api/auth";
import { useAuth } from "../auth/AuthContext";

export function RegisterPage() {
  const nav = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState("");
  const { refresh } = useAuth();

  async function onSubmit() {
    setErr("");
    try {
      await ensureCsrfCookie();
      await register(email, password);
      await login(email, password);
      await refresh();
      nav("/");
    } catch (e: any) {
      setErr(e?.response?.data?.detail ?? e?.message ?? "Register failed");
    }
  }

  return (
    <Stack spacing={2} sx={{ maxWidth: 420 }}>
      <Typography variant="h4">Регистрация</Typography>
      {err && <Alert severity="error">{err}</Alert>}
      <TextField label="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
      <TextField label="Пароль" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <Button variant="contained" onClick={onSubmit}>Создать аккаунт</Button>
      <Link component={RouterLink} to="/login">Уже есть аккаунт? Войти</Link>
    </Stack>
  );
}