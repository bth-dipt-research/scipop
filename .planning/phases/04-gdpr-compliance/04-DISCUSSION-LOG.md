# Phase 4: GDPR Compliance - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md - this log preserves the alternatives considered.

**Date:** 2026-04-09
**Phase:** 04-gdpr-compliance
**Areas discussed:** Consent UX surface, Consent choice model, Settings re-open path, Tracking disclosure content

---

## Consent UX surface

| Option | Description | Selected |
|--------|-------------|----------|
| Bottom banner | Low-friction consent prompt pattern for public site | ✓ |
| Centered modal | High-visibility prompt with stronger interruption | |
| Full-page gate | Strict pre-content gate with highest friction | |

**User's choice:** Bottom banner; no GA before explicit choice; dismissal treated as reject; persist state via cookie + localStorage.
**Notes:** User accepted recommended strict-consent defaults for all four UX behavior questions.

---

## Consent choice model

| Option | Description | Selected |
|--------|-------------|----------|
| Accept all / Reject all | Binary explicit choice model | ✓ |
| Granular categories | Additional category toggles/customization flow | |
| No reject path | Accept-only pattern | |

**User's choice:** Keep binary accept/reject; no customize in Phase 04; reject changes apply immediately; no consent versioning in this phase.
**Notes:** User intentionally kept scope lean and avoided additional policy version mechanics.

---

## Settings re-open path

| Option | Description | Selected |
|--------|-------------|----------|
| Footer link on all pages | Persistent low-clutter access point to privacy settings | ✓ |
| Header nav link | High-visibility but competes with core nav | |
| Both header and footer | Maximum visibility with extra UI noise | |

**User's choice:** Footer link on all pages; opens existing banner/panel; updates apply immediately; inline success confirmation shown.
**Notes:** Reuse-over-new-pattern was preferred to keep implementation straightforward.

---

## Tracking disclosure content

| Option | Description | Selected |
|--------|-------------|----------|
| Dedicated privacy page + banner summary | Short prompt text plus full disclosure destination | ✓ |
| Banner only | Minimal disclosure depth | |
| Methodology-only disclosure | Reuse existing page but weaker discoverability | |

**User's choice:** Dedicated privacy page plus banner summary; include provider/purpose/data points/controls; plain-language tone; include contact details.
**Notes:** User prioritized transparency for general audience readability.

---

## the agent's Discretion

- Consent library selection and implementation details.
- Exact state key naming and internal consent utility shape.
- Final UI styling/microcopy details within locked behavior.

## Deferred Ideas

- Granular category-based consent customization.
- Consent versioning and policy-change re-prompt behavior.
