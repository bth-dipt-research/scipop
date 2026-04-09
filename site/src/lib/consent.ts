export const SCIPOP_ANALYTICS_CONSENT_KEY = 'scipop_analytics_consent';

export type AnalyticsConsentState = 'granted' | 'denied' | 'unset';

export function parseAnalyticsConsent(value: string | null): AnalyticsConsentState {
  if (value === 'granted') {
    return 'granted';
  }

  if (value === 'denied') {
    return 'denied';
  }

  return 'unset';
}
