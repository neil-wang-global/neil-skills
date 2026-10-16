---
name: v0-ui-style
description: Use when designing or refining a v0.app-style UI, Vercel-inspired neutral workspace, or Hermes V0 Panel interface, including interactive HTML demos and component previews.
---

# Hermes v0 UI Style

Apply the user's local Hermes visual sources to the requested interface. This is a portable packaging of Hermes's **V0 Panel theme and Vercel design reference**, not an official v0.app skill or a claim that Hermes shipped a standalone skill named v0.

## Read the source

For workspace/dashboard UI, read [references/v0-panel.yaml](references/v0-panel.yaml) first: its tokens and component styles are the primary source. Read [references/vercel.md](references/vercel.md) for typography, shadows, component detail, and responsive behavior; it describes Vercel's marketing site, so do not impose its hero typography or generous landing-page spacing on dense product screens.

When editing an existing app or a Hermes Dashboard theme, also read [references/dashboard-theme-design.md](references/dashboard-theme-design.md), especially its selector scoping and terminal preservation guidance. The bundled source files are unmodified originals; their Hermes-specific tool names are context, not requirements to install tools or publish a tunnel.

## Translate to the target UI

- Start from the theme's quiet neutral surfaces: `#fafafa` canvas, white cards/sidebar, `#18181b` text, `#e4e4e7` hairlines, 8px card radius, 6px controls, and restrained blue focus. Dark primary actions and muted secondary actions create hierarchy. Reserve semantic colors for actual status.
- Use Geist/Inter with system and appropriate language fallbacks; Geist Mono for identifiers. Keep body text readable. Do not transfer compressed Latin display tracking to Chinese body text.
- Resolve source differences by surface: V0 Panel's flat bordered cards for workspace UI; Vercel's layered shadow-border treatment for a requested marketing page. Use restrained elevation for overlays.
- Translate tokens into the existing stack and scope styles to the new surface or verified component. The original YAML's global `!important` resets are dashboard-specific historical source, **not a stylesheet to paste wholesale**. Preserve focus states, component variants, maps, code, and terminals.

## Deliver and verify

Match the requested component inventory with working controls. For component demos, implement selection, change, dismissal, validation, and visible state feedback as applicable; prose descriptions are supporting material. Respect explicit custom/non-native control requirements. Date, range, and datetime controls should share the surface's typography, border, spacing, focus, and popover treatment.

Preview the actual rendered artifact at the requested widths and exercise its controls, including keyboard focus and overlay dismissal. Report the artifact path, implemented interactions, and any unverified visual or runtime behavior accurately.

## Provenance

Copied from the local Hermes installation on 2026-10-16:

- `~/.hermes/dashboard-themes/v0-panel.yaml` -> `references/v0-panel.yaml` (V0 Panel theme).
- `~/.hermes/skills/creative/popular-web-designs/templates/vercel.md` -> `references/vercel.md` (Vercel reference). Its parent skill credits Hermes Agent + Teknium, sourced from VoltAgent/awesome-design-md, MIT.
- `~/.hermes/skills/creative/dashboard-theme-design/SKILL.md` -> `references/dashboard-theme-design.md` (scoped theme implementation guidance).

The entrypoint adapts source routing for portable skill use; originals retain their content and attribution.
