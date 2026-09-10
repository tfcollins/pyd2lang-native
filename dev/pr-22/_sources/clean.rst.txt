clean Technical Diagramming Library
===================================

The built-in ``clean`` library provides a cohesive, flat diagramming aesthetic
inspired by the Anthropic and OpenAI design languages: a restrained
cool-neutral tint scale that groups components by tint and shape, a single clay
accent reserved for emphasis, hairline borders, and no drop shadows. Enable it
by passing ``library="clean"`` to :func:`d2.compile`.

.. code-block:: python

   import d2

   svg = d2.compile(code, library="clean")

Use the clean library for:

- **System and architecture diagrams** - services, gateways, APIs, and clients
- **Data planes** - databases, caches, queues, and object storage
- **AI/agent flows** - models, agents, and document artifacts
- **Control flow** - decisions, processes, and grouped boundaries

Differentiation is carried by tint (paper for compute/actors/AI/logic, slate for
data, muted-dashed for external systems) and shape, with the clay accent applied
only to emphasis nodes (``clean-primary``) and primary paths
(``clean-flow-primary``).

.. toctree::
   :maxdepth: 2

   clean-shapes

Example
-------

.. code-block:: text

   direction: right

   title: Request Flow { class: clean-title }

   system: Platform {
     class: clean-panel

     user: User { class: clean-user }
     web: Web App { class: clean-browser }
     gw: API Gateway { class: clean-gateway }

     data: Data Plane {
       class: clean-band
       api: Orders API { class: clean-primary }
       cache: Redis { class: clean-cache }
       db: Postgres { class: clean-database }
     }

     ext: Payments { class: clean-external }

     user -> web { class: clean-flow }
     web -> gw { class: clean-flow }
     gw -> data.api { class: clean-flow-primary }
     data.api -> data.cache { class: clean-flow-muted }
     data.api -> data.db { class: clean-flow }
     data.api -> ext: webhook { class: clean-flow-dashed }
   }

.. d2::
   :library: clean
   :alt: clean library request-flow architecture example
   :align: center

   direction: right

   title: Request Flow { class: clean-title }

   system: Platform {
     class: clean-panel

     user: User { class: clean-user }
     web: Web App { class: clean-browser }
     gw: API Gateway { class: clean-gateway }

     data: Data Plane {
       class: clean-band
       api: Orders API { class: clean-primary }
       cache: Redis { class: clean-cache }
       db: Postgres { class: clean-database }
     }

     ext: Payments { class: clean-external }

     user -> web { class: clean-flow }
     web -> gw { class: clean-flow }
     gw -> data.api { class: clean-flow-primary }
     data.api -> data.cache { class: clean-flow-muted }
     data.api -> data.db { class: clean-flow }
     data.api -> ext: webhook { class: clean-flow-dashed }
   }

Component Classes
-----------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Class
     - Use
   * - ``clean-service``
     - Generic service or component box (paper).
   * - ``clean-primary``
     - Emphasized or primary node, carrying the clay accent.
   * - ``clean-api``
     - API or endpoint.
   * - ``clean-gateway``
     - Gateway or ingress (hexagon).
   * - ``clean-function``
     - Function, lambda, or handler.
   * - ``clean-cloud``
     - Cloud or managed service (cloud shape).
   * - ``clean-database``
     - Relational or primary datastore (cylinder, slate tint).
   * - ``clean-cache``
     - Cache layer (slate tint).
   * - ``clean-storage``
     - Object or blob storage (cylinder, slate tint).
   * - ``clean-queue``
     - Message queue or stream (slate tint).
   * - ``clean-client``
     - Generic client.
   * - ``clean-browser``
     - Web client.
   * - ``clean-mobile``
     - Mobile client.
   * - ``clean-user``
     - End user (person shape).
   * - ``clean-external``
     - Third-party or external system (muted fill, dashed border).
   * - ``clean-model``
     - Model or inference endpoint.
   * - ``clean-agent``
     - Agent.
   * - ``clean-document``
     - Document or artifact (page shape).
   * - ``clean-decision``
     - Branch or decision point (diamond).
   * - ``clean-process``
     - Process or step.
   * - ``clean-group``
     - Transparent grouping container with a hairline boundary.

Panel, Typography, and Flow Classes
-----------------------------------

Use ``clean-panel`` for the outer grouped surface and ``clean-band`` for a
slate-tinted sub-grouping (for example a data plane or subsystem).

Use ``clean-title``, ``clean-subtitle``, ``clean-label``,
``clean-section-label``, and ``clean-note`` for text-only labels.

Use ``clean-flow`` for standard arrows, ``clean-flow-primary`` for the
clay-accented primary path, ``clean-flow-muted`` for low-emphasis links, and
``clean-flow-dashed`` for optional, asynchronous, or external links.

Dark Theme
----------

The clean library supports the same dark theme mode as the other libraries:

.. code-block:: python

   svg = d2.compile(code, library="clean", theme="dark")
