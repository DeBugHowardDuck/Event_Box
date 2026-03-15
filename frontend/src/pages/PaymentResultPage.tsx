import { useParams, Link as RouterLink } from "react-router-dom";
import { Alert, Button, Stack, Typography } from "@mui/material";

export function PaymentResultPage() {
  const { status } = useParams();

  const isOk = status === "success";

  return (
    <Stack spacing={2}>
      <Typography variant="h4">Оплата</Typography>

      {isOk ? (
        <Alert severity="success">
          Оплата прошла. Статус заказа обновится после webhook YooKassa.
        </Alert>
      ) : (
        <Alert severity="error">
          Оплата не завершена или отменена.
        </Alert>
      )}

      <Button component={RouterLink} to="/me/orders" variant="contained">
        Перейти к моим заказам
      </Button>
    </Stack>
  );
}