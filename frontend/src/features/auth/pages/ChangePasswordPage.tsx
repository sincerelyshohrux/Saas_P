import { useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { Link, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { changePasswordRequest, getMe } from "@/features/auth/api";
import { useAuthStore } from "@/features/auth/store";
import { parseApiError } from "@/shared/api/client";
import { Button } from "@/shared/ui/Button";
import { Input } from "@/shared/ui/Input";
const schema = z.object({ old_password: z.string().min(1, "required"), new_password: z.string().min(8, "passwordMin"), confirm_password: z.string().min(1, "required") }).refine((value) => value.new_password === value.confirm_password, { path: ["confirm_password"], message: "passwordMismatch" });
type FormValues = z.infer<typeof schema>;
export function ChangePasswordPage() {
  const { t } = useTranslation(); const user = useAuthStore((s) => s.user); const setUser = useAuthStore((s) => s.setUser); const navigate = useNavigate(); const [serverError, setServerError] = useState("");
  const { register, handleSubmit, setError, formState: { errors, isSubmitting } } = useForm<FormValues>({ resolver: zodResolver(schema) });
  const onSubmit = handleSubmit(async ({ old_password, new_password }) => {
    setServerError(""); try { await changePasswordRequest({ old_password, new_password }); const freshUser = await getMe(); setUser(freshUser); navigate(freshUser.role === "SUPER_ADMIN" ? "/admin" : "/shop", { replace: true }); }
    catch (error: unknown) { const parsed = parseApiError(error); if (parsed.fields) { for (const field of ["old_password", "new_password", "confirm_password"] as const) { const messages = parsed.fields[field]; if (messages?.[0]) setError(field, { type: "server", message: messages[0] }); } const nonField = parsed.fields.non_field_errors?.[0]; if (nonField) setServerError(nonField); } else setServerError(parsed.detail || t("common.error")); }
  });
  const forced = Boolean(user?.must_change_password);
  const fieldError = (key: keyof FormValues) => { const message = errors[key]?.message; if (!message) return undefined; return message in { required: 1, passwordMin: 1, passwordMismatch: 1 } ? t(`auth.${message}`) : message; };
  return <main className="grid min-h-screen place-items-center bg-slate-50 px-4 py-10 dark:bg-slate-950"><div className="w-full max-w-lg"><div className="mb-6"><h1 className="text-2xl font-bold">{t("auth.changePasswordTitle")}</h1><p className="mt-2 text-sm text-slate-500">{t("auth.changePasswordSubtitle")}</p></div><form onSubmit={(event) => void onSubmit(event)} className="space-y-5 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-slate-900">{forced && <div role="status" className="rounded-lg border border-amber-200 bg-amber-50 p-3 text-sm text-amber-800 dark:border-amber-900 dark:bg-amber-950 dark:text-amber-200">{t("auth.forcedPasswordBanner")}</div>}<Input label={t("auth.oldPassword")} type="password" autoComplete="current-password" {...register("old_password")} error={fieldError("old_password")} /><Input label={t("auth.newPassword")} type="password" autoComplete="new-password" {...register("new_password")} error={fieldError("new_password")} /><Input label={t("auth.confirmPassword")} type="password" autoComplete="new-password" {...register("confirm_password")} error={fieldError("confirm_password")} />{serverError && <p role="alert" className="rounded-lg bg-red-50 p-3 text-sm text-red-700 dark:bg-red-950 dark:text-red-300">{serverError}</p>}<div className="flex flex-col gap-3 sm:flex-row"><Button type="submit" loading={isSubmitting} className="flex-1">{t("auth.changePassword")}</Button>{!forced && <Link to={user?.role === "SUPER_ADMIN" ? "/admin" : "/shop"} className="inline-flex min-h-11 items-center justify-center rounded-lg px-4 text-sm font-medium text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800">{t("common.cancel")}</Link>}</div></form></div></main>;
}
