/** Format a decimal string without converting money to floating-point. */
export function formatMoney(decimalString: string): string {
  const normalized = decimalString.trim().replace(/\s/g, "");
  const match = /^([+-]?)(\d+)(?:[.,](\d+))?$/.exec(normalized);
  if (!match) return `${decimalString} so'm`;
  const sign = match[1] === "-" ? "-" : "";
  const integer = match[2].replace(/^0+(?=\d)/, "");
  const grouped = integer.replace(/\B(?=(\d{3})+(?!\d))/g, " ");
  const fraction = match[3]?.replace(/0+$/, "");
  return `${sign}${grouped}${fraction ? `,${fraction}` : ""} so'm`;
}
