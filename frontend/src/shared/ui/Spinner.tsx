export function Spinner({ label = "Yuklanmoqda", size = "md" }: { label?: string; size?: "sm" | "md" | "lg" }) {
  const sizes = { sm: "h-4 w-4 border-2", md: "h-7 w-7 border-[3px]", lg: "h-10 w-10 border-4" };
  return <span className="inline-flex items-center gap-3" role="status"><span className={`inline-block animate-spin rounded-full border-indigo-600 border-t-transparent ${sizes[size]}`} />{label && <span className="text-sm text-slate-600 dark:text-slate-300">{label}</span>}</span>;
}
