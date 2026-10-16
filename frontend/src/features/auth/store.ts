import { create } from "zustand";
import type { AuthUser, LoginResponse } from "@/features/auth/types";
interface AuthState { accessToken: string | null; user: AuthUser | null; bootstrapping: boolean; setAccessToken: (token: string | null) => void; setSession: (data: LoginResponse) => void; setUser: (user: AuthUser) => void; clearAuth: () => void; setBootstrapping: (value: boolean) => void }
export const useAuthStore = create<AuthState>((set) => ({ accessToken: null, user: null, bootstrapping: true,
  setAccessToken: (accessToken) => set({ accessToken }),
  setSession: (data) => { localStorage.setItem("refresh_token", data.refresh); set({ accessToken: data.access, user: data.user }); },
  setUser: (user) => set({ user }),
  clearAuth: () => { localStorage.removeItem("refresh_token"); set({ accessToken: null, user: null }); },
  setBootstrapping: (bootstrapping) => set({ bootstrapping }),
}));
