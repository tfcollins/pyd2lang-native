clean Shapes
============

The clean library provides 21 flat technical-diagramming shapes. Each shape is a
D2 class applied with ``class: <name>``. Differentiation is carried by **tint**
(paper for compute, actors, AI, and logic; slate for data; muted + dashed for
external systems) and by **shape**, with the single clay accent reserved for
emphasis (``clean-primary``).

Every diagram below renders in both light and dark to match the documentation
theme.

Usage
-----

.. code-block:: python

   import d2

   code = """
   client: Client { class: clean-client }
   gw: API Gateway { class: clean-gateway }
   api: Orders API { class: clean-primary }
   db: Postgres { class: clean-database }

   client -> gw { class: clean-flow }
   gw -> api { class: clean-flow-primary }
   api -> db { class: clean-flow }
   """

   svg = d2.compile(code, library="clean")

Compute
-------

Paper-tinted boxes for services and endpoints. ``clean-primary`` carries the
clay accent for the emphasized node; ``clean-gateway`` is a hexagon and
``clean-cloud`` a cloud outline.

.. d2::
   :library: clean
   :alt: clean compute shapes
   :align: center

   shapes: {
     grid-columns: 3
     grid-gap: 36
     svc: clean-service { class: clean-service }
     prm: clean-primary { class: clean-primary }
     api: clean-api { class: clean-api }
     gw: clean-gateway { class: clean-gateway }
     fn: clean-function { class: clean-function }
     cloud: clean-cloud { class: clean-cloud }
   }

.. list-table::
   :header-rows: 1
   :widths: 28 72

   * - Class
     - Use
   * - ``clean-service``
     - Generic service or component box.
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

Data
----

Slate-tinted shapes for the data plane. ``clean-database`` and ``clean-storage``
are cylinders; ``clean-cache`` and ``clean-queue`` are slate rectangles.

.. d2::
   :library: clean
   :alt: clean data shapes
   :align: center

   shapes: {
     grid-columns: 4
     grid-gap: 36
     db: clean-database { class: clean-database }
     cache: clean-cache { class: clean-cache }
     store: clean-storage { class: clean-storage }
     queue: clean-queue { class: clean-queue }
   }

.. list-table::
   :header-rows: 1
   :widths: 28 72

   * - Class
     - Use
   * - ``clean-database``
     - Relational or primary datastore (cylinder).
   * - ``clean-cache``
     - Cache layer such as Redis or a CDN.
   * - ``clean-storage``
     - Object or blob storage (cylinder).
   * - ``clean-queue``
     - Message queue or stream.

Actors
------

Clients and people. ``clean-user`` is a person silhouette; ``clean-external`` is
a muted, dashed box for third-party systems outside your control.

.. d2::
   :library: clean
   :alt: clean actor shapes
   :align: center

   shapes: {
     grid-columns: 3
     grid-gap: 36
     client: clean-client { class: clean-client }
     browser: clean-browser { class: clean-browser }
     mobile: clean-mobile { class: clean-mobile }
     user: clean-user { class: clean-user }
     ext: clean-external { class: clean-external }
   }

.. list-table::
   :header-rows: 1
   :widths: 28 72

   * - Class
     - Use
   * - ``clean-client``
     - Generic client or consumer.
   * - ``clean-browser``
     - Web client.
   * - ``clean-mobile``
     - Mobile client.
   * - ``clean-user``
     - End user (person shape).
   * - ``clean-external``
     - Third-party or external system (muted fill, dashed border).

AI
--

Paper-tinted shapes for model-centric flows. ``clean-document`` is a page shape
for artifacts and inputs.

.. d2::
   :library: clean
   :alt: clean AI shapes
   :align: center

   shapes: {
     grid-columns: 3
     grid-gap: 36
     model: clean-model { class: clean-model }
     agent: clean-agent { class: clean-agent }
     doc: clean-document { class: clean-document }
   }

.. list-table::
   :header-rows: 1
   :widths: 28 72

   * - Class
     - Use
   * - ``clean-model``
     - Model or inference endpoint.
   * - ``clean-agent``
     - Agent.
   * - ``clean-document``
     - Document or artifact (page shape).

Logic & Structure
-----------------

Control-flow and grouping shapes. ``clean-decision`` is a diamond; ``clean-group``
is a transparent container with a hairline boundary for grouping related nodes.

.. d2::
   :library: clean
   :alt: clean logic and structure shapes
   :align: center

   shapes: {
     grid-columns: 3
     grid-gap: 36
     dec: clean-decision { class: clean-decision }
     proc: clean-process { class: clean-process }
     grp: clean-group { class: clean-group }
   }

.. list-table::
   :header-rows: 1
   :widths: 28 72

   * - Class
     - Use
   * - ``clean-decision``
     - Branch or decision point (diamond).
   * - ``clean-process``
     - Process or step.
   * - ``clean-group``
     - Transparent grouping container with a hairline boundary.

Flow Edges
----------

Four edge classes set the emphasis of a connection. ``clean-flow-primary`` uses
the clay accent for the main path; ``clean-flow-muted`` and ``clean-flow-dashed``
de-emphasize secondary, optional, or asynchronous links.

.. d2::
   :library: clean
   :alt: clean flow edge classes
   :align: center

   direction: right
   a: Source { class: clean-service }
   b: Target { class: clean-service }
   a -> b: clean-flow { class: clean-flow }
   a -> b: clean-flow-primary { class: clean-flow-primary }
   a -> b: clean-flow-muted { class: clean-flow-muted }
   a -> b: clean-flow-dashed { class: clean-flow-dashed }

.. list-table::
   :header-rows: 1
   :widths: 32 68

   * - Class
     - Use
   * - ``clean-flow``
     - Standard connection.
   * - ``clean-flow-primary``
     - Clay-accented primary path.
   * - ``clean-flow-muted``
     - Low-emphasis or secondary link.
   * - ``clean-flow-dashed``
     - Optional, asynchronous, or external link.

Panels and Typography
---------------------

Use ``clean-panel`` for the outer grouped surface and ``clean-band`` for a
slate-tinted sub-grouping such as a data plane. For text-only labels use
``clean-title``, ``clean-subtitle``, ``clean-label``, ``clean-section-label``,
and ``clean-note``.

.. d2::
   :library: clean
   :alt: clean panel, band, and typography example
   :align: center

   direction: down
   title: Service Topology { class: clean-title }
   panel: Platform {
     class: clean-panel
     gw: Gateway { class: clean-gateway }
     data: Data Plane {
       class: clean-band
       api: Orders API { class: clean-primary }
       db: Postgres { class: clean-database }
       api -> db { class: clean-flow }
     }
     gw -> data.api { class: clean-flow-primary }
   }
