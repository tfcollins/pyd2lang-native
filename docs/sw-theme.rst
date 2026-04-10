SW Theme
========

The SW theme provides ADI brand colors and styling classes adapted for software
architecture and AI system diagrams.

Color Palette
-------------

Light Theme
~~~~~~~~~~~

.. raw:: html

   <table style="border-collapse:collapse; margin:1em 0;">
   <tr>
     <td style="background:#0067B9; width:60px; height:40px; border:1px solid #ccc;"></td>
     <td style="padding-left:12px;"><strong>ADI Blue</strong> — <code>#0067B9</code> — Primary brand color</td>
   </tr>
   <tr>
     <td style="background:#004A87; width:60px; height:40px; border:1px solid #ccc;"></td>
     <td style="padding-left:12px;"><strong>Dark Blue</strong> — <code>#004A87</code> — Data flow emphasis</td>
   </tr>
   <tr>
     <td style="background:#D6EAF8; width:60px; height:40px; border:1px solid #ccc;"></td>
     <td style="padding-left:12px;"><strong>Pale Blue</strong> — <code>#D6EAF8</code> — Step highlights</td>
   </tr>
   <tr>
     <td style="background:#FDF6EC; width:60px; height:40px; border:1px solid #ccc;"></td>
     <td style="padding-left:12px;"><strong>Cream</strong> — <code>#FDF6EC</code> — Warm container fill</td>
   </tr>
   <tr>
     <td style="background:#E8F4FD; width:60px; height:40px; border:1px solid #ccc;"></td>
     <td style="padding-left:12px;"><strong>Background Blue</strong> — <code>#E8F4FD</code> — Container fill</td>
   </tr>
   <tr>
     <td style="background:#C8102E; width:60px; height:40px; border:1px solid #ccc;"></td>
     <td style="padding-left:12px;"><strong>Red</strong> — <code>#C8102E</code> — Error flows</td>
   </tr>
   <tr>
     <td style="background:#007A33; width:60px; height:40px; border:1px solid #ccc;"></td>
     <td style="padding-left:12px;"><strong>Green</strong> — <code>#007A33</code> — Success flows</td>
   </tr>
   <tr>
     <td style="background:#F5A623; width:60px; height:40px; border:1px solid #ccc;"></td>
     <td style="padding-left:12px;"><strong>Amber</strong> — <code>#F5A623</code> — Async / warning</td>
   </tr>
   </table>

Dark Theme
~~~~~~~~~~

The dark theme inverts colors for dark backgrounds:

.. raw:: html

   <table style="border-collapse:collapse; margin:1em 0;">
   <tr>
     <td style="background:#4D9AD5; width:60px; height:40px; border:1px solid #555;"></td>
     <td style="padding-left:12px;"><strong>ADI Blue</strong> — <code>#4D9AD5</code> — Primary accent</td>
   </tr>
   <tr>
     <td style="background:#0D1B2A; width:60px; height:40px; border:1px solid #555;"></td>
     <td style="padding-left:12px;"><strong>Background</strong> — <code>#0D1B2A</code> — Container fill</td>
   </tr>
   <tr>
     <td style="background:#2A2520; width:60px; height:40px; border:1px solid #555;"></td>
     <td style="padding-left:12px;"><strong>Cream</strong> — <code>#2A2520</code> — Warm container fill</td>
   </tr>
   <tr>
     <td style="background:#E0E0E0; width:60px; height:40px; border:1px solid #555;"></td>
     <td style="padding-left:12px;"><strong>Text</strong> — <code>#E0E0E0</code> — Primary text</td>
   </tr>
   <tr>
     <td style="background:#FF6B6B; width:60px; height:40px; border:1px solid #555;"></td>
     <td style="padding-left:12px;"><strong>Red</strong> — <code>#FF6B6B</code> — Error flows</td>
   </tr>
   <tr>
     <td style="background:#66BB6A; width:60px; height:40px; border:1px solid #555;"></td>
     <td style="padding-left:12px;"><strong>Green</strong> — <code>#66BB6A</code> — Success flows</td>
   </tr>
   <tr>
     <td style="background:#FFB74D; width:60px; height:40px; border:1px solid #555;"></td>
     <td style="padding-left:12px;"><strong>Amber</strong> — <code>#FFB74D</code> — Async / warning</td>
   </tr>
   </table>

Flow Classes
------------

Apply these classes on connections (edges) between components to indicate
flow type. Each uses a distinct color and stroke style.

.. list-table::
   :header-rows: 1
   :widths: 22 18 15 45

   * - Class
     - Color
     - Stroke
     - Use For
   * - ``sw-flow``
     - ADI Blue ``#0067B9``
     - Solid, 2px
     - Default data/control flow
   * - ``sw-flow-data``
     - Dark Blue ``#004A87``
     - Solid, 3px
     - Emphasized data flow
   * - ``sw-flow-control``
     - Grey ``#58595B``
     - Dashed, 2px
     - Control flow paths
   * - ``sw-flow-async``
     - Amber ``#F5A623``
     - Dashed, 2px
     - Async / event-driven flow
   * - ``sw-flow-error``
     - Red ``#C8102E``
     - Solid, 2px
     - Error paths
   * - ``sw-flow-success``
     - Green ``#007A33``
     - Solid, 2px
     - Success paths
   * - ``sw-flow-feedback``
     - Light Blue ``#4D9AD5``
     - Dashed, 2px
     - Feedback / loop-back
   * - ``sw-flow-light``
     - Light Grey ``#D1D3D4``
     - Solid, 2px
     - Subtle connectors

Example:

.. code-block:: text

   agent: Auditor { class: sw-agent }
   model: LLM { class: sw-model }

   agent -> model: Request { class: sw-flow }
   model -> agent: Response { class: sw-flow-feedback }
   agent -> log: Error { class: sw-flow-error }

Container Classes
-----------------

sw-container
~~~~~~~~~~~~

Groups components with ADI blue border and light blue fill. All containers use a modern ``border-radius: 12`` layout and feature prominent drop shadows for visual depth.

.. code-block:: text

   loop: Auditing Loop {
     class: sw-container

     agent: Auditor { class: sw-agent }
     model: Target { class: sw-model }
     agent -> model { class: sw-flow }
   }

.. list-table::
   :header-rows: 1
   :widths: 22 30

   * - Variant
     - Description
   * - ``sw-container``
     - Blue border, light blue fill
   * - ``sw-container-cream``
     - Grey border, warm cream fill
   * - ``sw-container-green``
     - Green border, light green fill
   * - ``sw-container-amber``
     - Amber border, light amber fill
   * - ``sw-container-red``
     - Red border, light red fill
   * - ``sw-container-white``
     - Grey border, white fill

Step Highlight Classes
----------------------

Apply to nodes inside workflow diagrams to color-code process steps,
similar to the Petri research page style.

.. list-table::
   :header-rows: 1
   :widths: 22 20 20

   * - Class
     - Fill
     - Stroke
   * - ``sw-step-blue``
     - ``#D6EAF8``
     - ``#0067B9``
   * - ``sw-step-green``
     - ``#E8F5E9``
     - ``#007A33``
   * - ``sw-step-amber``
     - ``#FFF3E0``
     - ``#F5A623``
   * - ``sw-step-white``
     - ``#FFFFFF``
     - ``#D1D3D4``

Example:

.. code-block:: text

   s1: Formulate hypothesis { class: sw-step-white }
   s2: Design scenarios { class: sw-step-blue }
   s3: Build environments { class: sw-step-amber }
   s4: Run models { class: sw-step-green }

   s1 -> s2 -> s3 -> s4 { class: sw-flow-light }

Typography Classes
------------------

sw-title
~~~~~~~~

Diagram title styled with ADI brand colors. Renders as text-only shape.

.. code-block:: text

   title: Agent Pipeline { class: sw-title }

sw-subtitle
~~~~~~~~~~~~

Subsection heading in dark text.

.. code-block:: text

   heading: Scoring Phase { class: sw-subtitle }

sw-note
~~~~~~~

Annotation block for notes. Renders as a page shape with muted colors.

.. code-block:: text

   note: |md
     Judge scores transcripts
     across multiple dimensions
   | { class: sw-note }

ADI Signal Classes
------------------

The SW library also includes the ADI theme's signal and layout classes, so you
can use hardware-style color coding alongside software components. These classes
adapt automatically to light and dark themes.

.. list-table::
   :header-rows: 1
   :widths: 22 18 15 45

   * - Class
     - Color (light)
     - Stroke
     - Use For
   * - ``adi-signal``
     - ADI Blue ``#0067B9``
     - Solid, 2px
     - Default signal connections
   * - ``adi-signal-analog``
     - Soft Black ``#231F20``
     - Solid, 2px
     - Analog signal paths
   * - ``adi-signal-digital``
     - ADI Blue ``#0067B9``
     - Dashed, 2px
     - Digital buses (SPI, I2S, JESD204B)
   * - ``adi-signal-clock``
     - Green ``#007A33``
     - Dashed, 1px
     - Clock distribution
   * - ``adi-signal-power``
     - Red ``#C8102E``
     - Solid, 2px
     - Power supply rails

Additional ADI layout classes are also available:

- ``adi-container`` — Blue border container (8px radius, drop shadow)
- ``adi-title`` — Bold title in ADI Blue
- ``adi-note`` — Muted annotation block (page shape)

Example mixing SW components with ADI signal styles:

.. code-block:: text

   server: API Server { class: sw-server }
   fpga: FPGA { class: sw-function }
   db: Telemetry DB { class: sw-database }

   server -> fpga: SPI Config { class: adi-signal-digital }
   fpga -> db: Data Stream { class: sw-flow-data }
   fpga -> server: Interrupt { class: adi-signal-clock }

Using Themes
------------

.. code-block:: python

   import d2

   # Light theme (default)
   svg_light = d2.compile(code, library="sw")

   # Dark theme
   svg_dark = d2.compile(code, library="sw", theme="dark")
