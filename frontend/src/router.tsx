import { createBrowserRouter } from "react-router-dom";
import { Layout } from "./ui/Layout";
import { HomePage } from "./pages/HomePage";
import { EventDetailPage } from "./pages/EventDetailPage";
import { MyOrdersPage } from "./pages/MyOrdersPage";
import { MyTicketsPage } from "./pages/MyTicketsPage";
import { CheckerPage } from "./pages/CheckerPage";
import { PaymentResultPage } from "./pages/PaymentResultPage";
import { LoginPage } from "./pages/LoginPage";
import { RegisterPage } from "./pages/RegisterPage";
import { OrganizerEventsPage } from "./pages/OrganizerEventsPage";
import { OrganizerCreateEventPage } from "./pages/OrganizerCreateEventPage";
import { OrganizerEventDetailPage } from "./pages/OrganizerEventDetailPage";


export const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      { path: "/", element: <HomePage /> },
      { path: "/events/:id", element: <EventDetailPage /> },
      { path: "/me/orders", element: <MyOrdersPage /> },
      { path: "/me/tickets", element: <MyTicketsPage /> },
      { path: "/checker", element: <CheckerPage /> },
      { path: "/payment/:status", element: <PaymentResultPage /> },
      { path: "/login", element: <LoginPage /> },
      { path: "/register", element: <RegisterPage /> },
      { path: "/organizer/events", element: <OrganizerEventsPage /> },
      { path: "/organizer/events/new", element: <OrganizerCreateEventPage /> },
      { path: "/organizer/events/:id", element: <OrganizerEventDetailPage /> },
    ],
  },
]);