import { Suspense, lazy, type ReactNode } from "react";
import { createBrowserRouter, Navigate } from "react-router-dom";
import { RequireAuth, RequireRole, PublicOnly } from "@/app/guards";
import { AdminLayout } from "@/layouts/AdminLayout";
import { ShopLayout } from "@/layouts/ShopLayout";
import { Spinner } from "@/shared/ui/Spinner";

const LoginPage = lazy(() => import("@/features/auth/pages/LoginPage").then((m) => ({ default: m.LoginPage })));
const ChangePasswordPage = lazy(() => import("@/features/auth/pages/ChangePasswordPage").then((m) => ({ default: m.ChangePasswordPage })));
const DashboardPage = lazy(() => import("@/features/admin/pages/DashboardPage").then((m) => ({ default: m.DashboardPage })));
const ProductsPage = lazy(() => import("@/features/products/pages/ProductsPage").then((m) => ({ default: m.ProductsPage })));
const PlaceholderPage = lazy(() => import("@/shared/ui/PlaceholderPage").then((m) => ({ default: m.PlaceholderPage })));
const ForbiddenPage = lazy(() => import("@/shared/pages/ForbiddenPage").then((m) => ({ default: m.ForbiddenPage })));
const NotFoundPage = lazy(() => import("@/shared/pages/NotFoundPage").then((m) => ({ default: m.NotFoundPage })));
const BlockedPage = lazy(() => import("@/shared/pages/BlockedPage").then((m) => ({ default: m.BlockedPage })));
const wait = (element: ReactNode) => <Suspense fallback={<div className="grid min-h-64 place-items-center"><Spinner label="Sahifa yuklanmoqda" /></div>}>{element}</Suspense>;
const placeholder = (key: string) => wait(<PlaceholderPage titleKey={key} />);

export const router = createBrowserRouter([
  { path: "/blocked", element: wait(<BlockedPage />) },
  { element: <PublicOnly />, children: [{ path: "/login", element: wait(<LoginPage />) }] },
  { element: <RequireAuth />, children: [
    { path: "/change-password", element: wait(<ChangePasswordPage />) },
    { path: "/403", element: wait(<ForbiddenPage />) },
    { path: "/", element: <RoleHome /> },
    { path: "/admin", element: <RequireRole roles={["SUPER_ADMIN"]}><AdminLayout /></RequireRole>, children: [
      { index: true, element: wait(<DashboardPage />) },
      { path: "shops", element: placeholder("nav.shops") }, { path: "map", element: placeholder("nav.map") },
      { path: "subscriptions", element: placeholder("nav.subscriptions") }, { path: "audit-logs", element: placeholder("nav.auditLogs") },
    ] },
    { path: "/shop", element: <RequireRole roles={["SHOP_ADMIN", "AGENT"]}><ShopLayout /></RequireRole>, children: [
      { index: true, element: placeholder("nav.dashboard") }, { path: "products", element: wait(<ProductsPage />) },
      { path: "orders", element: placeholder("nav.orders") }, { path: "crm", element: placeholder("nav.crm") },
      { path: "agents", element: placeholder("nav.agents") }, { path: "bonuses", element: placeholder("nav.bonuses") },
      { path: "analytics", element: placeholder("nav.analytics") }, { path: "map", element: placeholder("nav.map") },
      { path: "invite", element: placeholder("nav.customerLink") }, { path: "ai", element: placeholder("nav.ai") },
      { path: "settings", element: placeholder("nav.settings") },
    ] },
    { path: "*", element: wait(<NotFoundPage />) },
  ] },
  { path: "*", element: wait(<NotFoundPage />) },
]);

function RoleHome() {
  const user = useAuthStoreSafe();
  if (!user) return <Navigate to="/login" replace />;
  if (user.must_change_password) return <Navigate to="/change-password" replace />;
  return <Navigate to={user.role === "SUPER_ADMIN" ? "/admin" : user.role === "SHOP_ADMIN" || user.role === "AGENT" ? "/shop" : "/403"} replace />;
}
function useAuthStoreSafe() {
  // Kept as a hook so role redirects react to auth state updates.
  return useAuthStore((state) => state.user);
}
import { useAuthStore } from "@/features/auth/store";
