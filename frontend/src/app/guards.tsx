import { Navigate, Outlet, useLocation } from "react-router-dom";
import type { ReactNode } from "react";
import { useAuthStore } from "@/features/auth/store";
import type { UserRole } from "@/features/auth/types";
import { Spinner } from "@/shared/ui/Spinner";

export function RequireAuth() {
  const user = useAuthStore((s) => s.user);
  const location = useLocation();
  if (!user) return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  if (user.must_change_password && location.pathname !== "/change-password") return <Navigate to="/change-password" replace />;
  return <Outlet />;
}

export function RequireRole({ roles, children }: { roles: UserRole[]; children?: ReactNode }) {
  const user = useAuthStore((s) => s.user);
  if (!user) return <Navigate to="/login" replace />;
  if (user.must_change_password) return <Navigate to="/change-password" replace />;
  if (!roles.includes(user.role)) return <Navigate to="/403" replace />;
  return children ?? <Outlet />;
}

export function PublicOnly() {
  const user = useAuthStore((s) => s.user);
  if (!user) return <Outlet />;
  if (user.must_change_password) return <Navigate to="/change-password" replace />;
  return <Navigate to={user.role === "SUPER_ADMIN" ? "/admin" : "/shop"} replace />;
}

export function AuthLoading({ children }: { children: ReactNode }) {
  const loading = useAuthStore((s) => s.bootstrapping);
  return loading ? <div className="grid min-h-screen place-items-center"><Spinner label="Yuklanmoqda" /></div> : children;
}
