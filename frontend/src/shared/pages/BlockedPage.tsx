import { Link, useSearchParams } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { useAuthStore } from "@/features/auth/store";

/** Ochiq sahifa: bloklangan foydalanuvchida token/profil bo'lmasligi mumkin. */
export function BlockedPage() {
  const { t } = useTranslation();
  const [params] = useSearchParams();
  const clearAuth = useAuthStore((s) => s.clearAuth);
  const message = params.get("reason") === "subscription" ? t("errors.subscription") : t("errors.blocked");
  return (
    <main className="grid min-h-screen place-items-center p-6">
      <section className="max-w-lg rounded-2xl border border-amber-200 bg-white p-8 text-center shadow-sm dark:border-amber-900 dark:bg-slate-900">
        <div className="mx-auto grid h-12 w-12 place-items-center rounded-full bg-amber-100 font-bold text-amber-700">!</div>
        <h1 className="mt-4 text-2xl font-bold">{t("errors.blockedTitle")}</h1>
        <p className="mt-3 text-slate-600 dark:text-slate-300">{message}</p>
        <Link to="/login" onClick={clearAuth} className="mt-6 inline-block text-sm font-semibold text-indigo-600 hover:underline">
          {t("common.backToLogin")}
        </Link>
      </section>
    </main>
  );
}
