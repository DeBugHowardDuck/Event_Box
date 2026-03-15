import { Outlet, Link as RouterLink } from "react-router-dom";
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Container,
  Stack,
  CircularProgress,
} from "@mui/material";

import { useAuth } from "../auth/AuthContext";

export function Layout() {
  const { user, isLoading, logout } = useAuth();

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Event Box
          </Typography>

          <Stack direction="row" spacing={1} alignItems="center">
            <Button color="inherit" component={RouterLink} to="/">Мероприятия</Button>
            <Button color="inherit" component={RouterLink} to="/me/orders">Мои заказы</Button>
            <Button color="inherit" component={RouterLink} to="/me/tickets">Мои билеты</Button>
            <Button color="inherit" component={RouterLink} to="/checker">Проверка QR</Button>

            {user && (user.role === "organizer" || user.role === "admin") && (
            <Button color="inherit" component={RouterLink} to="/organizer/events">
              Создать
            </Button>
            )}


            {isLoading ? (
              <CircularProgress size={18} color="inherit" />
            ) : user ? (
              <>
                <Typography variant="body2" sx={{ mx: 1 }}>
                  {user.email} ({user.role ?? "user"})
                </Typography>
                <Button color="inherit" onClick={logout}>Выйти</Button>
              </>
            ) : (
              <>
                <Button color="inherit" component={RouterLink} to="/login">Войти</Button>
                <Button color="inherit" component={RouterLink} to="/register">Регистрация</Button>
              </>
            )}
          </Stack>
        </Toolbar>
      </AppBar>

      <Container sx={{ py: 3 }}>
        <Outlet />
      </Container>
    </>
  );
}