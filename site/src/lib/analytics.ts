export const SITE_ENV_PRODUCTION = 'production';

export function getSiteEnv(): string {
  return String(import.meta.env.PUBLIC_SITE_ENV ?? '').trim().toLowerCase();
}

export function getPublicMeasurementId(): string {
  return String(import.meta.env.PUBLIC_GA_MEASUREMENT_ID ?? '').trim();
}

export function isProductionTelemetryEnabled(): boolean {
  return getSiteEnv() === SITE_ENV_PRODUCTION;
}

export function assertProductionTelemetryConfig(): void {
  if (isProductionTelemetryEnabled() && !getPublicMeasurementId()) {
    throw new Error('PUBLIC_GA_MEASUREMENT_ID is required when PUBLIC_SITE_ENV=production');
  }
}
