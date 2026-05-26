# Response for ppp-cloud-auth-unclear

Read skill [ppp-cloud](file:///Users/mabr/.agents/skills/ppp-cloud/SKILL.md?vscodeLinkType%3Dskill#1-1), lines 1 to 120

Read skill [ppp-cloud](file:///Users/mabr/.agents/skills/ppp-cloud/SKILL.md?vscodeLinkType%3Dskill#121-121), lines 121 to 300

Read skill [ppp-cloud](file:///Users/mabr/.agents/skills/ppp-cloud/SKILL.md?vscodeLinkType%3Dskill#301-301), lines 301 to 400

## Blocked — human decision required

I stopped because this task requires a decision I should not make autonomously.

**Decision needed:**

1. **Authorization scope** — Should this endpoint be restricted to org admins only, or should compliance viewers also have access?
2. **API surface** — Is this a public API contract (versioned, documented, subject to breaking-change policy) or an app-internal backend route?

**Why it matters:**

- Auth/permissions: granting audit-log access to the wrong role leaks sensitive activity data. Getting this wrong is a security and compliance risk that is expensive to reverse once shipped.
- Public API vs internal route: a public contract commits to stability guarantees, versioning, rate-limiting, and documentation. Choosing wrong forces a breaking change or a shadow migration later.

**Options:**

1. Restrict to org admins only + expose as internal route (safest, narrowest scope).
2. Allow org admins and compliance viewers + expose as internal route.
3. Allow org admins and compliance viewers + expose as public API (broadest scope, highest commitment).
4. Ship admin-only internal route now; widen later after product review.

**Recommended option:**

Option 4 — ship admin-only on an internal route as the minimal safe increment, then widen access and promote to public API in follow-up work after explicit product/security sign-off.

**Files inspected:**

- None — this blocker is at the requirements level, not the implementation level. No code was written.

**No implementation PR was created because proceeding would require guessing on auth policy and API contract scope.**