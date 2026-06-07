Agent Skills
============

This repository includes Codex skills under ``.agents/skills/``. Skills are
small, repo-local instruction bundles that help agents produce consistent work
without re-discovering project preferences each time.

Use these skills when creating diagrams, UI, examples, or documentation assets
for this project. Keep skill guidance concise and focused; if a workflow needs
large examples or reusable assets, add them as skill resources instead of
expanding ``SKILL.md``.

Available Skills
----------------

``soft-technical-flowgraphs``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use this skill for modern technical flowgraphs, architecture diagrams, system
maps, workflow visuals, D2/SVG flowcharts, and AI-product-style explainer
graphics. It defines a calm visual direction with off-white surfaces, muted
borders, charcoal text, soft accent colors, rounded nodes, subtle shadows, and
clear directional flow.

This skill is best for:

- AI agent pipelines and model/tool workflows
- Software architecture and data-flow diagrams
- Technical explainers that need a polished, soft visual style
- D2, SVG, HTML, or CSS diagram outputs

It treats Anthropic/OpenAI-style graphics as broad inspiration only. Do not copy
brand assets, logos, exact palettes, or proprietary visual identity.

``professional-ui-design``
~~~~~~~~~~~~~~~~~~~~~~~~~~

Use this skill for frontend UI design and implementation work. It emphasizes
production-ready interfaces, deliberate whitespace, strong hierarchy,
accessible semantic HTML, responsive layouts, and clear interaction states.

Maintaining Skills
------------------

Each skill must include a ``SKILL.md`` file with YAML frontmatter containing a
``name`` and ``description``. The description is the trigger text, so include the
main use cases there rather than only in the body.

Validate changed skills before opening a PR:

.. code-block:: bash

   python3 /home/tcollins/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/<skill-name>

When adding or changing a skill, also update this page so contributors know when
and how to use it.
