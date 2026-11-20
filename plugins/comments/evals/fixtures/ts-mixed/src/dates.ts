export function parseIsoDate(s: string): Date {
  // Safari before 16.4 parses a bare "YYYY-MM-DD" as local time instead of UTC,
  // so append "T00:00:00Z". https://bugs.webkit.org/show_bug.cgi?id=231285
  return new Date(/^\d{4}-\d{2}-\d{2}$/.test(s) ? s + "T00:00:00Z" : s);
}

export function daysBetween(a: Date, b: Date): number {
  // Node's Intl date math skips DST changes in some time zones, so count in UTC milliseconds.
  return Math.round((b.getTime() - a.getTime()) / 86_400_000);
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function toDate(x: any): Date {
  // TODO(#142): accept Unix timestamps in seconds as well
  return x instanceof Date ? x : parseIsoDate(String(x));
}
