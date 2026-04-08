SW Shapes
=========

The library provides 32 software and AI component shapes.
Each shape is a D2 class applied with ``class: <name>``.

Usage
-----

.. code-block:: python

   import d2

   code = """
   agent: Auditor { class: sw-agent }
   model: Claude { class: sw-model }
   tool: Search { class: sw-tool }

   agent -> tool -> model
   """

   svg = d2.compile(code, library="sw")

Core Software / Infrastructure
-------------------------------

.. list-table::
   :header-rows: 1
   :widths: 18 15 67

   * - Class
     - Icon
     - Description
   * - ``sw-server``
     - .. image:: ../lib/sw/icons/sw-server.svg
          :width: 80
     - Server or backend service. Rack/tower silhouette.
   * - ``sw-database``
     - .. image:: ../lib/sw/icons/sw-database.svg
          :width: 80
     - Database or data store. Classic cylinder shape.
   * - ``sw-queue``
     - .. image:: ../lib/sw/icons/sw-queue.svg
          :width: 80
     - Message queue or job queue. Horizontal stack with arrows.
   * - ``sw-api``
     - .. image:: ../lib/sw/icons/sw-api.svg
          :width: 80
     - API endpoint or REST service. Angle brackets with slash.
   * - ``sw-cloud``
     - .. image:: ../lib/sw/icons/sw-cloud.svg
          :width: 80
     - Cloud service or external SaaS. Cloud outline.
   * - ``sw-container-svc``
     - .. image:: ../lib/sw/icons/sw-container-svc.svg
          :width: 80
     - Container or microservice. Nested box (Docker-style).
   * - ``sw-function``
     - .. image:: ../lib/sw/icons/sw-function.svg
          :width: 80
     - Serverless function or Lambda. Lambda/f(x) symbol.
   * - ``sw-cache``
     - .. image:: ../lib/sw/icons/sw-cache.svg
          :width: 80
     - Cache layer (Redis, CDN). Lightning bolt symbol.
   * - ``sw-storage``
     - .. image:: ../lib/sw/icons/sw-storage.svg
          :width: 80
     - Object storage or file system. Stacked file rectangles.
   * - ``sw-gateway``
     - .. image:: ../lib/sw/icons/sw-gateway.svg
          :width: 80
     - API gateway or load balancer. Shield with arrows.
   * - ``sw-browser``
     - .. image:: ../lib/sw/icons/sw-browser.svg
          :width: 80
     - Browser or web client. Window chrome with address bar.
   * - ``sw-mobile``
     - .. image:: ../lib/sw/icons/sw-mobile.svg
          :width: 80
     - Mobile app client. Phone outline.
   * - ``sw-terminal``
     - .. image:: ../lib/sw/icons/sw-terminal.svg
          :width: 80
     - CLI or terminal interface. Prompt symbol.
   * - ``sw-config``
     - .. image:: ../lib/sw/icons/sw-config.svg
          :width: 80
     - Configuration or settings. Gear/cog icon.

AI/ML & Agent Workflow
----------------------

.. list-table::
   :header-rows: 1
   :widths: 18 15 67

   * - Class
     - Icon
     - Description
   * - ``sw-model``
     - .. image:: ../lib/sw/icons/sw-model.svg
          :width: 80
     - LLM or ML model. Neural network node pattern.
   * - ``sw-agent``
     - .. image:: ../lib/sw/icons/sw-agent.svg
          :width: 80
     - AI agent or autonomous agent. Robot head silhouette.
   * - ``sw-prompt``
     - .. image:: ../lib/sw/icons/sw-prompt.svg
          :width: 80
     - Prompt or system message. Chat bubble with dots.
   * - ``sw-document``
     - .. image:: ../lib/sw/icons/sw-document.svg
          :width: 80
     - Document or seed instruction. Page with folded corner.
   * - ``sw-eval``
     - .. image:: ../lib/sw/icons/sw-eval.svg
          :width: 80
     - Evaluation step or judge. Checkmark in circle.
   * - ``sw-score``
     - .. image:: ../lib/sw/icons/sw-score.svg
          :width: 80
     - Score indicator or metric. Gauge with colored dots.
   * - ``sw-tool``
     - .. image:: ../lib/sw/icons/sw-tool.svg
          :width: 80
     - Tool or tool call. Wrench icon.
   * - ``sw-action``
     - .. image:: ../lib/sw/icons/sw-action.svg
          :width: 80
     - Action or step execution. Play triangle.
   * - ``sw-loop``
     - .. image:: ../lib/sw/icons/sw-loop.svg
          :width: 80
     - Loop or iteration cycle. Circular refresh arrows.
   * - ``sw-branch``
     - .. image:: ../lib/sw/icons/sw-branch.svg
          :width: 80
     - Decision or branch point. Diamond shape.
   * - ``sw-dataset``
     - .. image:: ../lib/sw/icons/sw-dataset.svg
          :width: 80
     - Dataset or training data. Table grid icon.
   * - ``sw-pipeline``
     - .. image:: ../lib/sw/icons/sw-pipeline.svg
          :width: 80
     - Pipeline or workflow. Connected chevrons.

Communication & Observation
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 18 15 67

   * - Class
     - Icon
     - Description
   * - ``sw-message``
     - .. image:: ../lib/sw/icons/sw-message.svg
          :width: 80
     - Message or notification. Envelope icon.
   * - ``sw-log``
     - .. image:: ../lib/sw/icons/sw-log.svg
          :width: 80
     - Log or audit trail. Scrolling text icon.
   * - ``sw-metric``
     - .. image:: ../lib/sw/icons/sw-metric.svg
          :width: 80
     - Metric or monitoring. Bar chart with trend line.
   * - ``sw-user``
     - .. image:: ../lib/sw/icons/sw-user.svg
          :width: 80
     - User or human-in-the-loop. Person silhouette.
   * - ``sw-team``
     - .. image:: ../lib/sw/icons/sw-team.svg
          :width: 80
     - Team or group of users. Two-person silhouette.
   * - ``sw-webhook``
     - .. image:: ../lib/sw/icons/sw-webhook.svg
          :width: 80
     - Webhook or callback. Hook icon.
