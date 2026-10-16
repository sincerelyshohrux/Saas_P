import axios, { AxiosError, type InternalAxiosRequestConfig } from "axios";
import type { ApiError, ApiErrorBody } from "@/shared/api/types";
import { useAuthStore } from "@/features/auth/store";

const baseURL = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";
export const api = axios.create({ baseURL, headers: { "Content-Type": "application/json" }, timeout: 20000 });
let refreshPromise: Promise<string> | null = null;
let redirecting = false;

function isAuthEndpoint(url?: string) { return Boolean(url && ["/auth/login/", "/auth/refresh/"].some((path) => url.includes(path))); }
function clearSessionAndRedirect() {
  localStorage.removeItem("refresh_token"); useAuthStore.getState().clearAuth();
  if (!redirecting && window.location.pathname !== "/login") { redirecting = true; window.location.assign("/login"); }
}
async function refreshAccess(): Promise<string> {
  if (!refreshPromise) {
    const refresh = localStorage.getItem("refresh_token");
    if (!refresh) throw new Error("No refresh token");
    refreshPromise = axios.post<{ access: string }>(`${baseURL}/auth/refresh/`, { refresh }, { headers: { "Content-Type": "application/json" }, timeout: 20000 })
      .then(({ data }) => { useAuthStore.getState().setAccessToken(data.access); return data.access; })
      .catch((error: unknown) => { clearSessionAndRedirect(); throw error; })
      .finally(() => { refreshPromise = null; });
  }
  return refreshPromise;
}
api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const access = useAuthStore.getState().accessToken;
  if (access) config.headers.set("Authorization", `Bearer ${access}`);
  return config;
});
api.interceptors.response.use((response) => response, async (error: unknown) => {
  if (!axios.isAxiosError(error)) return Promise.reject(error);
  const original = error.config as (InternalAxiosRequestConfig & { _retried?: boolean }) | undefined;
  const status = error.response?.status; const body = error.response?.data as ApiErrorBody | undefined;
  if (status === 401 && original && !original._retried && !isAuthEndpoint(original.url)) {
    original._retried = true;
    try { const token = await refreshAccess(); original.headers.set("Authorization", `Bearer ${token}`); return await api(original); }
    catch (refreshError: unknown) { return Promise.reject(refreshError); }
  }
  if (status === 403 && body?.code === "password_change_required" && window.location.pathname !== "/change-password") window.location.assign("/change-password");
  if (status === 403 && (body?.code === "subscription_expired" || body?.code === "shop_blocked")) {
    const reason = body.code === "subscription_expired" ? "subscription" : "blocked";
    if (window.location.pathname !== "/blocked") window.location.assign(`/blocked?reason=${reason}`);
  }
  return Promise.reject(error);
});

export function parseApiError(err: unknown): ApiError {
  if (axios.isAxiosError(err)) {
    const body = (err as AxiosError<ApiErrorBody>).response?.data;
    return { status: err.response?.status ?? 0, code: body?.code ?? "network_error", detail: body?.detail ?? err.message ?? "Tarmoq xatosi", ...(body?.fields ? { fields: body.fields } : {}) };
  }
  return { status: 0, code: "unknown_error", detail: err instanceof Error ? err.message : "Kutilmagan xatolik" };
}
