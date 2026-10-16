import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useState } from "react";
import { RouterProvider } from "react-router-dom";
import { router } from "@/app/router";
import "@/shared/i18n";

export function AppProviders() {
  const [client] = useState(() => new QueryClient({ defaultOptions: { queries: { retry: 1, refetchOnWindowFocus: false } } }));
  return <QueryClientProvider client={client}><RouterProvider router={router} /></QueryClientProvider>;
}
