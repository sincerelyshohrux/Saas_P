import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";
import timezone from "dayjs/plugin/timezone";
import "dayjs/locale/uz";
dayjs.extend(utc); dayjs.extend(timezone); dayjs.locale("uz");
export function formatDate(value: string | Date | null | undefined, pattern = "DD.MM.YYYY HH:mm"): string {
  if (!value) return "—";
  const date = dayjs(value).tz("Asia/Tashkent");
  return date.isValid() ? date.format(pattern) : "—";
}
export { dayjs };
