import { useTranslation } from "react-i18next";
import { useAuthStore } from "@/features/auth/store";
import { Shell } from "@/layouts/AdminLayout";
export function ShopLayout() {
  const { t } = useTranslation(); const user = useAuthStore((s) => s.user);
  const adminItems = [{ to: "/shop", key: "nav.dashboard" }, { to: "/shop/products", key: "nav.products" }, { to: "/shop/orders", key: "nav.orders" }, { to: "/shop/crm", key: "nav.crm" }, { to: "/shop/agents", key: "nav.agents" }, { to: "/shop/bonuses", key: "nav.bonuses" }, { to: "/shop/analytics", key: "nav.analytics" }, { to: "/shop/map", key: "nav.map" }, { to: "/shop/invite", key: "nav.customerLink" }, { to: "/shop/ai", key: "nav.ai" }, { to: "/shop/settings", key: "nav.settings" }];
  const agentItems = [{ to: "/shop/orders", key: "nav.orders" }, { to: "/shop/crm", key: "nav.crm" }];
  return <Shell title={user?.shop_name || t("common.shopPanel")} items={user?.role === "AGENT" ? agentItems : adminItems} />;
}
