import { api } from "@/shared/api/client";
import type { AuthUser, ChangePasswordPayload, LoginPayload, LoginResponse } from "@/features/auth/types";
export async function loginRequest(payload: LoginPayload) { const { data } = await api.post<LoginResponse>("/auth/login/", payload); return data; }
export async function getMe() { const { data } = await api.get<AuthUser>("/auth/me/"); return data; }
export async function changePasswordRequest(payload: ChangePasswordPayload) { await api.post("/auth/change-password/", payload); }
export async function logout() { const refresh = localStorage.getItem("refresh_token"); if (refresh) await api.post("/auth/logout/", { refresh }); localStorage.removeItem("refresh_token"); }
