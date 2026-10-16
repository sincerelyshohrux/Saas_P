import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useLocation } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { useLogin } from "@/features/auth/hooks";
import { parseApiError } from "@/shared/api/client";
import { Button } from "@/shared/ui/Button";
import { Input } from "@/shared/ui/Input";
const schema = z.object({ username: z.string().min(1, "required"), password: z.string().min(1, "required") });
type FormValues = z.infer<typeof schema>;
export function LoginPage() {
  const { t } = useTranslation(); const location = useLocation(); const mutation = useLogin(); const [serverError, setServerError] = useState("");
  const { register, handleSubmit, formState: { errors } } = useForm<FormValues>({ resolver: zodResolver(schema), defaultValues: { username: "", password: "" } });
  useEffect(() => { if (location.state && "customerDenied" in location.state && location.state.customerDenied) setServerError(t("auth.customerNotAllowed")); }, [location.state, t]);
  const onSubmit = handleSubmit(async (values) => { setServerError(""); try { await mutation.mutateAsync(values); } catch (error: unknown) { const parsed = parseApiError(error); if (parsed.code === "invalid_credentials") setServerError(t("auth.invalidCredentials")); else if (parsed.code === "account_locked") setServerError(t("auth.accountLocked")); else if (parsed.status === 429 || parsed.code === "throttled") setServerError(t("auth.tooManyRequests")); else setServerError(parsed.detail || t("common.error")); } });
  return <main className="grid min-h-screen place-items-center bg-slate-50 px-4 py-10 dark:bg-slate-950"><div className="w-full max-w-md"><div className="mb-8 text-center"><div className="mx-auto mb-4 grid h-12 w-12 place-items-center rounded-2xl bg-indigo-600 text-xl font-bold text-white">S</div><h1 className="text-2xl font-bold tracking-tight">{t("auth.loginTitle")}</h1><p className="mt-2 text-sm text-slate-500">{t("auth.loginSubtitle")}</p></div><form onSubmit={(event) => void onSubmit(event)} className="space-y-5 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-slate-900 sm:p-8"><Input label={t("auth.username")} autoComplete="username" {...register("username")} error={errors.username ? t(`auth.${errors.username.message ?? "required"}`) : undefined} /><Input label={t("auth.password")} type="password" autoComplete="current-password" {...register("password")} error={errors.password ? t(`auth.${errors.password.message ?? "required"}`) : undefined} />{serverError && <p role="alert" className="rounded-lg bg-red-50 p-3 text-sm text-red-700 dark:bg-red-950 dark:text-red-300">{serverError}</p>}<Button type="submit" loading={mutation.isPending} className="w-full">{mutation.isPending ? t("auth.loggingIn") : t("auth.login")}</Button></form><p className="mt-6 text-center text-xs text-slate-400">SaaS Sales Platform</p></div></main>;
}
