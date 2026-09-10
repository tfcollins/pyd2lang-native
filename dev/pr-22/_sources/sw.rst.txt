SW Component Library
====================

The built-in software/AI component library provides 32 shapes for software
architecture and AI agent pipeline diagrams, themed with ADI brand colors.
Enable it by passing ``library="sw"`` to :func:`d2.compile`.

.. code-block:: python

   import d2

   svg = d2.compile(code, library="sw")

Use the SW library to create:

- **AI agent pipelines** — agents, models, tools, evaluators, documents
- **Software architecture** — servers, databases, APIs, queues, caches
- **Workflow diagrams** — steps, branches, loops, pipelines
- **Communication flows** — messages, webhooks, logs, metrics

.. toctree::
   :maxdepth: 2

   sw-shapes
   sw-theme
