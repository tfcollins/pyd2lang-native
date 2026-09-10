editorial Diagramming & Flowchart Library
=========================================

The built-in ``editorial`` library provides a publication-quality diagramming
and flowchart aesthetic inspired by `cathrynlavery/diagram-design <https://github.com/cathrynlavery/diagram-design>`_:
a crisp white-smoke and jet-black ink palette, subtle hairline borders,
a single atomic-tangerine focal accent reserved for the critical path or key decision,
and semantic flowchart primitives. Enable it by passing ``library="editorial"`` to :func:`d2.compile`.

.. code-block:: python

   import d2

   svg = d2.compile(code, library="editorial")

Use the editorial library for:

- **Flowcharts & Decision Logic** - branching algorithms, routing, and triage trees
- **Action & Process Pipelines** - multi-step sequential workflows with happy/fail paths
- **System Boundaries & Zones** - swimlanes, panels, boundaries, and containers
- **Editorial Categorization** - series color tints (sage, dusty blue, mustard, rust, slate)

Design Principles
-----------------

1. **Shape Carries Meaning**: Ovals denote terminals (start/end), rectangles denote actions/steps, diamonds denote decisions, and circles denote merge points.
2. **Restrained Focal Accent**: Atomic tangerine (``#EB6C36``) is reserved for 1–2 focal elements per diagram (such as the happy path or key decision).
3. **Dual Light/Dark Fidelity**: Diagrams render crisp in light mode (white-smoke surface with jet-black ink) and dark mode (slate-indigo base with bright white-smoke typography).

.. toctree::
   :maxdepth: 2

   editorial-shapes

Example: Flowchart Decision Tree
--------------------------------

.. code-block:: text

   direction: down

   title: User Onboarding Flow { class: editorial-title }

   start: Start Onboarding { class: editorial-start }
   check_email: Email Verified? { class: editorial-decision }
   setup_profile: Setup Profile { class: editorial-step }
   verify_identity: Verify Identity { class: [editorial-decision; editorial-decision-accent] }
   grant_access: Grant Full Access { class: [editorial-step; editorial-focal] }
   manual_review: Route to Review { class: [editorial-step; editorial-warning] }
   complete: Done { class: editorial-end }

   start -> check_email: { class: editorial-flow }
   check_email -> setup_profile: Yes { class: editorial-flow-success }
   check_email -> check_email: Resend link { class: editorial-flow-dashed }
   setup_profile -> verify_identity: { class: editorial-flow }
   verify_identity -> grant_access: Approved { class: editorial-flow-primary }
   verify_identity -> manual_review: Flagged { class: editorial-flow-danger }
   grant_access -> complete: { class: editorial-flow-primary }
   manual_review -> complete: Resolved { class: editorial-flow-muted }

.. d2::
   :library: editorial
   :alt: editorial flowchart decision tree example
   :align: center

   direction: down

   title: User Onboarding Flow { class: editorial-title }

   start: Start Onboarding { class: editorial-start }
   check_email: Email Verified? { class: editorial-decision }
   setup_profile: Setup Profile { class: editorial-step }
   verify_identity: Verify Identity { class: [editorial-decision; editorial-decision-accent] }
   grant_access: Grant Full Access { class: [editorial-step; editorial-focal] }
   manual_review: Route to Review { class: [editorial-step; editorial-warning] }
   complete: Done { class: editorial-end }

   start -> check_email: { class: editorial-flow }
   check_email -> setup_profile: Yes { class: editorial-flow-success }
   check_email -> check_email: Resend link { class: editorial-flow-dashed }
   setup_profile -> verify_identity: { class: editorial-flow }
   verify_identity -> grant_access: Approved { class: editorial-flow-primary }
   verify_identity -> manual_review: Flagged { class: editorial-flow-danger }
   grant_access -> complete: { class: editorial-flow-primary }
   manual_review -> complete: Resolved { class: editorial-flow-muted }

Component Classes
-----------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Class
     - Description
   * - ``editorial-start``, ``editorial-end``, ``editorial-terminal``
     - Terminal start/end oval node.
   * - ``editorial-step``, ``editorial-action``, ``editorial-process``
     - Standard action or process step (rounded rectangle).
   * - ``editorial-decision``, ``editorial-condition``
     - Decision / branching diamond.
   * - ``editorial-merge``, ``editorial-join``
     - Merge / join circle node.
   * - ``editorial-io``, ``editorial-data``
     - Input/output data node (parallelogram).
   * - ``editorial-document``, ``editorial-artifact``
     - Document or report page artifact.
   * - ``editorial-database``, ``editorial-store``
     - Database or storage cylinder.
   * - ``editorial-queue``
     - Queue buffer node.
   * - ``editorial-cloud``
     - Cloud / managed infrastructure node.
   * - ``editorial-actor``, ``editorial-user``
     - User / actor person shape.
   * - ``editorial-service``, ``editorial-api``
     - Service or endpoint block.
   * - ``editorial-gateway``
     - Gateway hexagon node.
   * - ``editorial-external``
     - External or third-party system (dashed border).
   * - ``editorial-focal``, ``editorial-primary``, ``editorial-accent``
     - Key emphasized step with atomic-tangerine tint and border.
   * - ``editorial-decision-accent``
     - Emphasized decision diamond with atomic-tangerine styling.
   * - ``editorial-success``, ``editorial-pass``
     - Approved or success state (green tint).
   * - ``editorial-warning``
     - Review or warning state (amber tint).
   * - ``editorial-danger``, ``editorial-fail``
     - Rejected or error state (coral/red tint).
   * - ``editorial-muted``
     - Secondary or muted node.
   * - ``editorial-series-sage`` .. ``editorial-series-slate``
     - Categorical series palette tints (sage, blue, mustard, rust, slate).

Theme & Flow Classes
--------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Class
     - Description
   * - ``editorial-container``
     - Structural container box with subtle fill and border.
   * - ``editorial-panel``
     - Card / panel container with solid border.
   * - ``editorial-swimlane``
     - Swimlane grouping container.
   * - ``editorial-boundary``
     - System / trust boundary (dashed border).
   * - ``editorial-card``
     - Clean card element.
   * - ``editorial-title``
     - Bold diagram title text (size 22).
   * - ``editorial-subtitle``
     - Diagram subtitle text (size 14).
   * - ``editorial-label``, ``editorial-section-label``
     - Section and node header labels.
   * - ``editorial-eyebrow``
     - Small uppercase tracking tag.
   * - ``editorial-callout``, ``editorial-note``
     - Editorial italic annotations.
   * - ``editorial-sublabel``
     - Metadata / parameter sublabel.
   * - ``editorial-flow``
     - Standard connection arrow.
   * - ``editorial-flow-primary``, ``editorial-flow-accent``
     - Emphasized happy-path connection arrow (atomic-tangerine).
   * - ``editorial-flow-muted``
     - Secondary or return connection arrow.
   * - ``editorial-flow-dashed``
     - Asynchronous, feedback, or write-back connector.
   * - ``editorial-flow-link``
     - External API or HTTP connection arrow.
   * - ``editorial-flow-success``
     - Positive / approved path arrow (green).
   * - ``editorial-flow-danger``
     - Negative / rejected / error path arrow (red).
