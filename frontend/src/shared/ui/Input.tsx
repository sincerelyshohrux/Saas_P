import { forwardRef, useId, type InputHTMLAttributes } from "react";

type Props = InputHTMLAttributes<HTMLInputElement> & { label: string; error?: string };

/**
 * react-hook-form `register()` ref beradi, shuning uchun forwardRef SHART.
 * Aks holda maydon qiymati o'qilmaydi va forma doim "bo'sh" hisoblanadi.
 */
export const Input = forwardRef<HTMLInputElement, Props>(function Input(
  { label, error, id, className = "", ...props },
  ref,
) {
  const generatedId = useId();
  const inputId = id ?? generatedId;
  const errorId = `${inputId}-error`;
  return (
    <div className="space-y-1.5">
      <label htmlFor={inputId} className="block text-sm font-medium text-slate-700 dark:text-slate-200">
        {label}
      </label>
      <input
        {...props}
        ref={ref}
        id={inputId}
        aria-invalid={Boolean(error)}
        aria-describedby={error ? errorId : undefined}
        className={`block w-full rounded-lg border bg-white px-3.5 py-2.5 text-sm text-slate-900 shadow-sm outline-none transition placeholder:text-slate-400 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 dark:bg-slate-950 dark:text-white dark:focus:ring-indigo-950 ${
          error ? "border-red-500" : "border-slate-300 dark:border-slate-700"
        } ${className}`}
      />
      {error && (
        <p id={errorId} role="alert" className="text-sm text-red-600">
          {error}
        </p>
      )}
    </div>
  );
});
