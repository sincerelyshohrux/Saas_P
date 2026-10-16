import axios from "axios";
import { getMe } from "@/features/auth/api";
import { useAuthStore } from "@/features/auth/store";

export async function bootstrapAuth(): Promise<void> {
  const store = useAuthStore.getState(); const refresh = localStorage.getItem("refresh_token");
  if (!refresh) { store.clearAuth(); store.setBootstrapping(false); return; }
  try {
    const { data } = await axios.post<{ access: string }>(`${import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1"}/auth/refresh/`, { refresh }, { headers: { "Content-Type": "application/json" }, timeout: 20000 });
    useAuthStore.getState().setAccessToken(data.access);
    const user = await getMe(); useAuthStore.getState().setUser(user);
    if (user.role === "CUSTOMER") { useAuthStore.getState().clearAuth(); }
  } catch { useAuthStore.getState().clearAuth(); }
  finally { useAuthStore.getState().setBootstrapping(false); }
}
