---
name: dashboard-theme-design
description: "Use when designing or installing Hermes Dashboard themes."
metadata:
  hermes:
    editorial_name: "Dashboard Theme Design"
    editorial_description: "Research, create, install, and verify professional Hermes Dashboard themes."
    requires_tools: [web_search, web_extract, terminal, write_file]
    requires_toolsets: []
    requires_plugins: []
---

# Dashboard Theme Design

Create or select themes for the Hermes **web Dashboard** with a design-led workflow. Treat a theme as a complete interface decision (type, contrast, spacing, surfaces, controls), not merely a palette swap.

## Standing design preference

Favor a quiet, contemporary Web-panel aesthetic: readable sans-serif typography, coherent spacing, modest radii, neutral surfaces, hairline borders, and one restrained action color. Avoid decorative cyberpunk effects, serif dashboard typography, forced uppercase, glow, textures, exaggerated gradients, and pure-black/pure-white high-contrast canvases unless the user explicitly requests them.

## Procedure

1. **Identify the surface.** Confirm the request is for `hermes dashboard`, not CLI/TUI skins or the native desktop app. Dashboard themes are YAML files under `$HERMES_HOME/dashboard-themes/` (fall back to `~/.hermes/dashboard-themes/`).
2. **Research before selecting.** Inspect the reference site with a browser when available; otherwise use page extraction and reliable design-system sources. If choosing a third-party pack, inspect screenshots or previews and its YAML shape before installing. Do not infer “professional” from its repository description.
3. **Decide whether a pack is suitable.** Use a pack only when its layout, typography, and visual hierarchy match the brief. If the user rejects several packs, stop cycling through palettes: author a purpose-built dashboard theme with `customCSS`.
4. **Build the theme incrementally.** Keep a known-good YAML revision before each visual experiment, then change one visual system at a time (for example: sidebar, typography, or buttons) and obtain a refreshed screenshot before moving to the next. Set these deliberately:
   - `palette`: neutral canvas plus readable foreground;
   - `typography`: system or reference-appropriate sans stack, practical base size and line height;
   - `layout`: modest radius and comfortable density;
   - `componentStyles` / `colorOverrides`: cards, sidebar, header, inputs, borders, focus ring;
   - `customCSS`: only the targeted corrections needed for a specific, verified DOM element.
5. **Inspect implementation before structural CSS.** When a complaint concerns a real Dashboard element, inspect the local Dashboard source or live DOM to find its exact selector and whether its style is inline. For example, the main menu rail is `#app-sidebar`; set its `componentStyles.sidebar.background` and add a narrowly scoped `#app-sidebar` correction only when required. When the user identifies a child control but wants its direct container changed, use a structural selector such as `:has(> button[role="radio"])` only after confirming that child’s stable attributes; this avoids changing each tab button’s own divider or state styling.
6. **Install and activate safely.** Write `<name>.yaml`, then use `hermes config set dashboard.theme <name>`; never hand-edit `config.yaml`.
7. **Verify.** Parse the YAML with Hermes’s venv Python, assert the expected `name` and palette values, assert `customCSS` stays below the 32 KiB runtime cap, then read back `hermes config get dashboard.theme`. Tell the user to refresh the dashboard (hard refresh if cached).

## Pitfalls

- Distinguish Dashboard theme YAML from Hermes skins before copying files — `dashboard-themes/` changes the web panel, while `skins/` targets CLI/TUI/Desktop and will not populate the normal Dashboard picker.
- Inspect a candidate visually before changing the active theme — repository labels such as “clean” or “professional” do not guarantee suitable typography, density, or panel hierarchy.
- Do not solve a layout-and-typography complaint by trying more palettes — a palette-only change leaves the original interface character intact.
- Use `customCSS` sparingly and keep it below 32 KiB — the Dashboard injects one scoped stylesheet and truncates larger blocks.
- Neutralize only the offending presentation rules with scoped CSS — broad overrides can damage terminal, code, accessibility, or plugin UI rendering.
- Do not apply `font-family`, color, radius, or fill rules to every `button`, `[role="button"]`, form control, or descendant of `#root` — Hermes uses a separate UI component system and an embedded terminal, so such rules override component variants, icon/Unicode fallbacks, and terminal-adjacent controls. Target a verified component selector instead.
- Keep Dashboard terminal colors and pet rendering outside a general UI CSS rewrite — they use dedicated terminal-theme fields and renderer settings, so diagnose them independently before changing either.
- When the user asks to correct one visible area, preserve the current working revision and modify that area only; do not bundle a typography, button, sidebar, and terminal redesign into the same iteration.
- Use `hermes config set dashboard.theme <name>` to activate a theme — it preserves valid config and persists the selected theme.
