---
name: soft-technical-flowgraphs
description: Create modern, soft technical flowgraphs, architecture diagrams, system maps, workflow visuals, D2/SVG flowcharts, and AI-product-style technical graphics. Use when Codex needs to design or style diagrams with a polished, calm, technical aesthetic inspired by contemporary Anthropic/OpenAI product graphics without copying brand assets, logos, or proprietary visual identity.
---

# Soft Technical Flowgraphs

Use this skill to create clear, modern technical diagrams with a soft visual style. Favor legibility, structure, and restraint over decorative complexity.

## Design Direction

- Use calm neutral backgrounds, off-white surfaces, charcoal text, muted borders, and a few soft accent colors.
- Build diagrams from rounded cards or nodes, thin connector lines, subtle shadows, and generous negative space.
- Keep the graph technical: visible hierarchy, clear direction, concise labels, grouped subsystems, and consistent node sizing.
- Prefer left-to-right flow for pipelines and top-to-bottom flow for layered systems.
- Use restrained detail: short labels, small metadata chips, light grid texture, or faint grouping containers only when they clarify the system.
- Do not imitate Anthropic or OpenAI exactly. Avoid their logos, exact branded palettes, proprietary illustrations, or claims of brand affiliation.

## Default Style Tokens

Use these as defaults unless the target project already has a stronger design system:

```css
:root {
  --bg: #f7f3ea;
  --surface: #fffcf5;
  --ink: #1f1e1a;
  --muted: #5d6675;
  --border: #ded8cc;
  --accent-blue: #8fd7e6;
  --accent-green: #b7d7c2;
  --accent-amber: #e8c07d;
  --accent-coral: #d9a08a;
  --shadow: 0 18px 45px rgba(31, 30, 26, 0.08);
}
```

## Layout Rules

- Start with the information architecture before styling: identify inputs, processing steps, outputs, feedback loops, and external systems.
- Use 3-7 primary nodes per row or layer. Split dense systems into grouped regions instead of shrinking text.
- Make connectors secondary to nodes: thin strokes, low contrast, arrowheads only where direction is ambiguous.
- Use accent colors to encode meaning, not decoration. Keep one primary accent and one secondary accent for most diagrams.
- Add soft grouping containers for subsystems such as `Client`, `Control Plane`, `Model Runtime`, or `Data Layer`.

## D2 Guidance

- Prefer classes and reusable style blocks over one-off inline styling.
- Use rounded rectangles or container shapes for most nodes; reserve distinctive shapes for external systems or data stores.
- Keep labels short and use separate small nodes or annotations for secondary metadata.
- If generating a complete D2 file, include a small theme/style section near the top so future edits stay consistent.

## SVG, HTML, and CSS Guidance

- Use CSS variables for the palette and spacing.
- Use accessible text contrast for all labels and avoid relying on color alone for meaning.
- Use `viewBox` and responsive sizing for SVG outputs.
- Add subtle gradients, texture, or grid backgrounds only when they do not reduce readability.
- Avoid generic purple gradients and default SaaS dashboards unless the user explicitly asks for that direction.

## Quality Bar

A successful output should feel like a polished technical explainer graphic: calm, precise, spatially balanced, and easy to scan. If the first version looks like a generic flowchart, revise spacing, hierarchy, type scale, grouping, and color restraint before considering it complete.
