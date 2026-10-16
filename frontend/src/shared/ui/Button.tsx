import type { ButtonHTMLAttributes, ReactNode } from "react";
import { Spinner } from "@/shared/ui/Spinner";
type Props = ButtonHTMLAttributes<HTMLButtonElement> & { loading?: boolean; children: ReactNode; variant?: "primary" | "secondary" | "danger" };
export function Button({ loading = false, disabled, children, variant = "primary", className = "", ...props }: Props) {
  const styles = { primary: "bg-indigo-600 text-white hover:bg-indigo-700", secondary: "border border-slate-300 bg-white text-slate-700 hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100", danger: "bg-red-600 text-white hover:bg-red-700" };
  return <button {...props} disabled={disabled || loading} className={`inline-flex min-h-11 items-center justify-center gap-2 rounded-lg px-4 py-2 text-sm font-semibold transition disabled:cursor-not-allowed disabled:opacity-60 ${styles[variant]} ${className}`}>
    {loading && <Spinner size="sm" label="" />}{children}
  </button>;
}
