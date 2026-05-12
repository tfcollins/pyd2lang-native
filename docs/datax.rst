ADI DataX Overview Library
==========================

The built-in DataX library provides semantic classes for recreating the
hand-authored SVG overview diagrams used in ``doc-adi/docs/overview``. Enable it
by passing ``library="datax"`` to :func:`d2.compile`.

.. code-block:: python

   import d2

   svg = d2.compile(code, library="datax")

Use the DataX library for:

- **Stack overviews** - panels, DataX bands, and layered architecture diagrams
- **Workflow diagrams** - hardware, processor, HDL, driver, and application boxes
- **Transport diagrams** - local, USB, network, and serial backend flows
- **Trade-off diagrams** - positive, warning, muted, and note callouts

Example
-------

.. code-block:: text

   direction: down

   title: ADI DataX Technology Stack { class: datax-title }

   stack: Layered architecture {
     class: datax-panel

     datax: ADI DataX {
       class: datax-band
       hdl: Layer 3: HDL / Firmware { class: datax-hdl }
       drivers: Layer 4: Drivers { class: datax-driver }
       libs: Layer 5: Libraries { class: datax-info }
       bindings: Layer 6: Ecosystem Bindings { class: datax-application }
     }

     apps: Layer 7: Applications { class: datax-application-alt }
     hwif: Layer 2: Hardware Interface { class: datax-processor }
     hw: Layer 1: Hardware { class: datax-hardware }

     apps -> datax.bindings -> datax.libs -> datax.drivers -> datax.hdl -> hwif -> hw {
       class: datax-flow
     }
   }

.. d2::
   :library: datax
   :alt: DataX overview stack example
   :align: center

   direction: down

   title: ADI DataX Technology Stack { class: datax-title }

   stack: Layered architecture {
     class: datax-panel

     datax: ADI DataX {
       class: datax-band
       hdl: Layer 3: HDL / Firmware { class: datax-hdl }
       drivers: Layer 4: Drivers { class: datax-driver }
       libs: Layer 5: Libraries { class: datax-info }
       bindings: Layer 6: Ecosystem Bindings { class: datax-application }
     }

     apps: Layer 7: Applications { class: datax-application-alt }
     hwif: Layer 2: Hardware Interface { class: datax-processor }
     hw: Layer 1: Hardware { class: datax-hardware }

     apps -> datax.bindings -> datax.libs -> datax.drivers -> datax.hdl -> hwif -> hw {
       class: datax-flow
     }
   }

Semantic Box Classes
--------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Class
     - Use
   * - ``datax-panel``
     - Outer grouped panel matching the overview SVG surface.
   * - ``datax-band``
     - ADI DataX scope band for layers or subsystems covered by DataX.
   * - ``datax-hardware``
     - Analog hardware, boards, devices, converters, sensors, and instruments.
   * - ``datax-hardware-alt``
     - Alternate hardware or device-under-test blocks.
   * - ``datax-processor``
     - FPGA SoCs, Raspberry Pi, microcontrollers, and host processors.
   * - ``datax-hdl``
     - HDL reference designs, FPGA fabric, firmware, and no-OS blocks.
   * - ``datax-driver``
     - Linux IIO drivers, IIOD, libiio bridge layers, and driver services.
   * - ``datax-application``
     - Bindings, scripts, GUI tools, MATLAB, Python, and custom applications.
   * - ``datax-application-alt``
     - Alternate or top-level application blocks.
   * - ``datax-info``
     - Network, host, library, backend, and explanatory blocks.
   * - ``datax-note-box`` / ``datax-note-warm``
     - Highlighted notes and warm callouts.
   * - ``datax-good`` / ``datax-warn``
     - Strengths and weaknesses or positive and warning callouts.
   * - ``datax-muted`` / ``datax-blank``
     - Neutral or empty grouping blocks.

Typography and Flow Classes
---------------------------

Use ``datax-title``, ``datax-subtitle``, ``datax-panel-label``,
``datax-panel-sublabel``, ``datax-section-label``, ``datax-layer-label``,
``datax-label``, and ``datax-note`` for text-only labels.

Use ``datax-flow`` for standard arrows, ``datax-flow-dashed`` for remote or
optional links, ``datax-flow-accent`` for emphasized transitions,
``datax-flow-muted`` for low-emphasis links, and ``datax-flow-good`` /
``datax-flow-warn`` for positive and warning paths.

Dark Theme
----------

The DataX library supports the same dark theme mode as the other libraries:

.. code-block:: python

   svg = d2.compile(code, library="datax", theme="dark")
