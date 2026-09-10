editorial Shapes
================

The ``editorial`` library provides flowchart and diagram primitives designed for
high-clarity publication graphics. Shapes convey semantic role (terminals, actions,
decisions, merges, data stores, actors), and atomic tangerine is reserved for focal
emphasis (``editorial-focal``, ``editorial-decision-accent``).

Flowchart Primitives
--------------------

Terminals (start/end), steps, decisions, and joins:

.. d2::
   :library: editorial
   :alt: editorial flowchart primitives
   :align: center

   shapes: {
     grid-columns: 4
     grid-gap: 32
     start: editorial-start { class: editorial-start }
     step: editorial-step { class: editorial-step }
     decision: editorial-decision { class: editorial-decision }
     join: editorial-merge { class: editorial-merge }
   }

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Class
     - Use
   * - ``editorial-start``, ``editorial-end``, ``editorial-terminal``
     - Flowchart entry or termination points (oval).
   * - ``editorial-step``, ``editorial-action``, ``editorial-process``
     - Action or processing step (rounded rectangle).
   * - ``editorial-decision``, ``editorial-condition``
     - Branching decision diamond.
   * - ``editorial-merge``, ``editorial-join``
     - Convergence / join point (circle).

Semantic States & Emphasis
--------------------------

Focal nodes carry the atomic-tangerine accent. State variants provide clear
success, warning, danger, and muted indications without visual clutter.

.. d2::
   :library: editorial
   :alt: editorial semantic states and emphasis
   :align: center

   shapes: {
     grid-columns: 3
     grid-gap: 32
     focal: editorial-focal { class: editorial-focal }
     d_accent: editorial-decision-accent { class: editorial-decision-accent }
     success: editorial-success { class: editorial-success }
     warn: editorial-warning { class: editorial-warning }
     danger: editorial-danger { class: editorial-danger }
     muted: editorial-muted { class: editorial-muted }
   }

Data & Infrastructure
---------------------

IO data, documents, databases, queues, gateways, and external systems:

.. d2::
   :library: editorial
   :alt: editorial data and infrastructure shapes
   :align: center

   shapes: {
     grid-columns: 3
     grid-gap: 32
     io: editorial-io { class: editorial-io }
     doc: editorial-document { class: editorial-document }
     db: editorial-database { class: editorial-database }
     queue: editorial-queue { class: editorial-queue }
     gw: editorial-gateway { class: editorial-gateway }
     ext: editorial-external { class: editorial-external }
   }

Series Categorical Tints
------------------------

Five desaturated editorial tints from the diagram-design style guide (sage, dusty blue, mustard, rust, slate) for multi-category diagrams:

.. d2::
   :library: editorial
   :alt: editorial series palette tints
   :align: center

   shapes: {
     grid-columns: 5
     grid-gap: 24
     s1: sage { class: editorial-series-sage }
     s2: blue { class: editorial-series-blue }
     s3: mustard { class: editorial-series-mustard }
     s4: rust { class: editorial-series-rust }
     s5: slate { class: editorial-series-slate }
   }

Containers & Boundaries
-----------------------

Grouping containers, panels, swimlanes, and boundaries:

.. d2::
   :library: editorial
   :alt: editorial containers and boundaries
   :align: center

   container: Container Area {
     class: editorial-container

     lane: Swimlane {
       class: editorial-swimlane
       a: Step A { class: editorial-step }
       b: Step B { class: editorial-primary }
       a -> b: { class: editorial-flow-primary }
     }

     zone: External Zone {
       class: editorial-boundary
       ext: API { class: editorial-external }
     }
   }

Flow Edge Styles
----------------

.. d2::
   :library: editorial
   :alt: editorial flow connector styles
   :align: center

   direction: right
   a: Source { class: editorial-step }
   b: Target { class: editorial-step }

   a -> b: default { class: editorial-flow }
   a -> b: primary / focal { class: editorial-flow-primary }
   a -> b: success { class: editorial-flow-success }
   a -> b: danger { class: editorial-flow-danger }
   a -> b: dashed / async { class: editorial-flow-dashed }
   a -> b: link / api { class: editorial-flow-link }
   a -> b: muted { class: editorial-flow-muted }
