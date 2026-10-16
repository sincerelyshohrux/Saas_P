import { useTranslation } from "react-i18next";
export function PlaceholderPage({ titleKey }: { titleKey: string }) {
  const { t } = useTranslation();
  return <section className="mx-auto max-w-5xl"><div className="mb-6"><h1 className="text-2xl font-bold tracking-tight">{t(titleKey)}</h1><p className="mt-2 text-sm text-slate-500">{t("common.comingSoon")}</p></div><div className="rounded-2xl border border-dashed border-slate-300 bg-white px-6 py-16 text-center dark:border-slate-700 dark:bg-slate-900"><div className="mx-auto mb-3 grid h-12 w-12 place-items-center rounded-xl bg-indigo-50 text-lg font-bold text-indigo-600 dark:bg-indigo-950">{t(titleKey).slice(0, 1)}</div><h2 className="font-semibold">{t(titleKey)}</h2><p className="mt-1 text-sm text-slate-500">{t("common.comingSoon")}</p></div></section>;
}
