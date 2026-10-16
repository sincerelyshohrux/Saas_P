import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { loginRequest } from "@/features/auth/api";
import { useAuthStore } from "@/features/auth/store";
import type { LoginPayload } from "@/features/auth/types";
export function useLogin() {
  const setSession = useAuthStore((s) => s.setSession); const clearAuth = useAuthStore((s) => s.clearAuth); const navigate = useNavigate();
  return useMutation({ mutationFn: (payload: LoginPayload) => loginRequest(payload), onSuccess: (data) => {
    if (data.user.role === "CUSTOMER") { clearAuth(); navigate("/login", { replace: true, state: { customerDenied: true } }); return; }
    setSession(data); navigate(data.user.must_change_password ? "/change-password" : data.user.role === "SUPER_ADMIN" ? "/admin" : "/shop", { replace: true });
  } });
}
