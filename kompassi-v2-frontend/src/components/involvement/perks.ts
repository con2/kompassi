/**
 * Manual perk overrides. Mirrors kompassi/involvement/perks.py on the backend.
 *
 * Which perks are manually overridden is tracked by the values of the technical
 * `manual-perks-override` Involvement dimension:
 *
 * - a dimension perk `ticket-type` -> `d-ticket-type`
 * - an annotation perk `tracon:mealVouchers` -> `a-tracon-meal-vouchers`
 *   (colon -> `-`, camelCase -> kebab-case, lowercased)
 */

export const manualPerksOverrideSlug = "manual-perks-override";

export function dimensionOverrideValue(dimensionSlug: string): string {
  return `d-${dimensionSlug}`;
}

export function annotationOverrideValue(annotationSlug: string): string {
  const kebab = annotationSlug
    .replace(/:/g, "-")
    .replace(/(?<!^)(?=[A-Z])/g, "-")
    .toLowerCase();
  return `a-${kebab}`;
}

export interface PerksOverridePayload {
  /** Override keys (`d-…` / `a-…`) that are manually overridden. */
  overrides: string[];
  /** Manually set values for overridden dimension perks, keyed by dimension slug. */
  dimensions: Record<string, string[]>;
  /** Manually set values for overridden annotation perks, keyed by annotation slug. */
  annotations: Record<string, string | number | boolean>;
}
