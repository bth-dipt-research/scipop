export function withBase(path: string): string {
  const base = import.meta.env.BASE_URL.replace(/\/+$/, '');
  const normalizedPath = path.replace(/^\/+/, '');

  if (!normalizedPath) {
    return `${base || '/'}/`;
  }

  return `${base}/${normalizedPath}`;
}
