export type ConsentState = 'accepted' | 'rejected' | 'unset';

export const CONSENT_STORAGE_KEY = 'scipop_analytics_consent';

function parseConsentValue(value: string | null | undefined): ConsentState {
  const stored = String(value ?? '').trim().toLowerCase();
  if (stored === 'accepted' || stored === 'rejected') {
    return stored;
  }
  return 'unset';
}

function readCookieValue(key: string): string | null {
  if (typeof document === 'undefined') {
    return null;
  }

  const prefix = `${key}=`;
  const parts = document.cookie.split(';').map((part) => part.trim());
  const match = parts.find((part) => part.startsWith(prefix));

  if (!match) {
    return null;
  }

  return match.slice(prefix.length);
}

export function readConsentState(): ConsentState {
  if (typeof window === 'undefined') {
    return 'unset';
  }

  const localStorageValue = parseConsentValue(window.localStorage.getItem(CONSENT_STORAGE_KEY));
  if (localStorageValue !== 'unset') {
    return localStorageValue;
  }

  const cookieValue = parseConsentValue(readCookieValue(CONSENT_STORAGE_KEY));
  if (cookieValue !== 'unset') {
    return cookieValue;
  }

  return 'unset';
}

export function writeConsentState(next: Exclude<ConsentState, 'unset'>): void {
  if (typeof window === 'undefined' || typeof document === 'undefined') {
    return;
  }

  if (!(next === 'accepted' || next === 'rejected')) {
    return;
  }

  window.localStorage.setItem(CONSENT_STORAGE_KEY, next);
  document.cookie = `${CONSENT_STORAGE_KEY}=${next}; Path=/; Max-Age=31536000; SameSite=Lax`;
}

export function clearConsentState(): void {
  if (typeof window !== 'undefined') {
    window.localStorage.removeItem(CONSENT_STORAGE_KEY);
  }

  if (typeof document !== 'undefined') {
    document.cookie = `${CONSENT_STORAGE_KEY}=; Path=/; Max-Age=0; SameSite=Lax`;
  }
}
