JIF Shapes
==========

The library provides style-based classes for pyadi-jif block diagrams.
Each shape is a D2 class applied with ``class: <name>``. The public class names
intentionally match pyadi-jif ``Node.ntype`` values.

Usage
-----

.. code-block:: python

   import d2

   code = """
   adc: ADC { class: adc }
   ddc: DDC { class: ddc }
   framer: JESD204 Framer { class: jesd204framer }

   adc -> ddc -> framer
   """

   svg = d2.compile(code, library="jif")

Converter And JESD Blocks
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 22 24 54

   * - Shape
     - Class
     - Description
   * - .. d2::
          :library: jif
          :theme: light

          adc: ADC { class: adc }

     - ``adc``
     - Analog-to-digital converter block.
   * - .. d2::
          :library: jif
          :theme: light

          dac: DAC { class: dac }

     - ``dac``
     - Digital-to-analog converter block.
   * - .. d2::
          :library: jif
          :theme: light

          ddc: DDC { class: ddc }

     - ``ddc``
     - Digital downconverter or decimation block.
   * - .. d2::
          :library: jif
          :theme: light

          duc: DUC { class: duc }

     - ``duc``
     - Digital upconverter or interpolation block.
   * - .. d2::
          :library: jif
          :theme: light

          crossbar: Crossbar { class: crossbar }

     - ``crossbar``
     - Crossbar, router, or converter datapath mux.
   * - .. d2::
          :library: jif
          :theme: light

          mux: Mux { class: mux }

     - ``mux``
     - Multiplexer or clock/data select block.
   * - .. d2::
          :library: jif
          :theme: light

          framer: Framer { class: jesd204framer }

     - ``jesd204framer``
     - JESD204 framer block inside a converter.
   * - .. d2::
          :library: jif
          :theme: light

          deframer: Deframer { class: jesd204deframer }

     - ``jesd204deframer``
     - JESD204 deframer block inside a converter.
   * - .. d2::
          :library: jif
          :theme: light

          framer: Framer { class: framer }

     - ``framer``
     - Remote JESD204 framer block.
   * - .. d2::
          :library: jif
          :theme: light

          deframer: Deframer { class: deframer }

     - ``deframer``
     - Remote JESD204 deframer block.

Clocking Blocks
---------------

.. list-table::
   :header-rows: 1
   :widths: 22 24 54

   * - Shape
     - Class
     - Description
   * - .. d2::
          :library: jif
          :theme: light

          input: Input { class: input }

     - ``input``
     - External reference, SYSREF, or device-clock input.
   * - .. d2::
          :library: jif
          :theme: light

          output: Output { class: out_clock_connected }

     - ``out_clock_connected``
     - Output clock pin or connected clock output.
   * - .. d2::
          :library: jif
          :theme: light

          divider: Divider { class: divider }

     - ``divider``
     - Clock, feedback, output, or transceiver divider.
   * - .. d2::
          :library: jif
          :theme: light

          pfd: PFD { class: phase-frequency-detector }

     - ``phase-frequency-detector``
     - PLL phase-frequency detector.
   * - .. d2::
          :library: jif
          :theme: light

          cp: Charge Pump { class: charge-pump }

     - ``charge-pump``
     - PLL charge-pump block.
   * - .. d2::
          :library: jif
          :theme: light

          lf: Loop Filter { class: loop-filter }

     - ``loop-filter``
     - PLL loop-filter block.
   * - .. d2::
          :library: jif
          :theme: light

          vco: VCO { class: vco }

     - ``vco``
     - Voltage-controlled oscillator.
   * - .. d2::
          :library: jif
          :theme: light

          vco: VCO { class: voltage-controlled-oscillator }

     - ``voltage-controlled-oscillator``
     - Long-form VCO class used by some pyadi-jif clock drawings.
   * - .. d2::
          :library: jif
          :theme: light

          cdr: CDR { class: cdr }

     - ``cdr``
     - Clock-data recovery block.

FPGA And System Blocks
----------------------

.. list-table::
   :header-rows: 1
   :widths: 22 24 54

   * - Shape
     - Class
     - Description
   * - .. d2::
          :library: jif
          :theme: light

          shell: Shell { class: shell }

     - ``shell``
     - Grouping shell for internal sub-blocks.
   * - .. d2::
          :library: jif
          :theme: light

          ip: IP { class: ip }

     - ``ip``
     - FPGA IP block such as JESD link, transport, or application logic.
   * - .. d2::
          :library: jif
          :theme: light

          phy: PHY { class: phy }

     - ``phy``
     - FPGA PHY block.
   * - .. d2::
          :library: jif
          :theme: light

          trx: Transceiver { class: transceiver }

     - ``transceiver``
     - FPGA transceiver block.
   * - .. d2::
          :library: jif
          :theme: light

          serdes: SERDES { class: serdes }

     - ``serdes``
     - Serializer/deserializer block.
   * - .. d2::
          :library: jif
          :theme: light

          decoder: Decoder { class: decoder }

     - ``decoder``
     - Link-layer decoder block.
   * - .. d2::
          :library: jif
          :theme: light

          cpll: CPLL { class: cpll }

     - ``cpll``
     - Channel PLL block.
   * - .. d2::
          :library: jif
          :theme: light

          qpll: QPLL { class: qpll }

     - ``qpll``
     - Quad PLL block.
   * - .. d2::
          :library: jif
          :theme: light

          dividers: TRX Dividers { class: trx-dividers }

     - ``trx-dividers``
     - Transceiver divider and mux group.

Expanded JIF Blocks
-------------------

These additive classes support softer, more expressive pyadi-jif and JESD system
flowgraphs while preserving the existing class names.

.. list-table::
   :header-rows: 1
   :widths: 22 24 54

   * - Shape
     - Class
     - Description
   * - .. d2::
          :library: jif
          :theme: light

          dev: Converter Device { class: converter-device }

     - ``converter-device``
     - Top-level converter IC or converter subsystem container.
   * - .. d2::
          :library: jif
          :theme: light

          clk: Clock Chip { class: clock-chip }

     - ``clock-chip``
     - Top-level clock generator, jitter cleaner, or clock tree device.
   * - .. d2::
          :library: jif
          :theme: light

          link: JESD Link { class: jesd-link }

     - ``jesd-link``
     - JESD204 serial link or link group.
   * - .. d2::
          :library: jif
          :theme: light

          lane: Lane 0 { class: jesd-lane }

     - ``jesd-lane``
     - Individual JESD serial lane.
   * - .. d2::
          :library: jif
          :theme: light

          align: Lane Aligner { class: lane-aligner }

     - ``lane-aligner``
     - Lane alignment or deterministic-latency stage.
   * - .. d2::
          :library: jif
          :theme: light

          buf: Elastic Buffer { class: elastic-buffer }

     - ``elastic-buffer``
     - Elastic buffer, FIFO, or rate-matching storage.
   * - .. d2::
          :library: jif
          :theme: light

          s: Scrambler { class: scrambler }

     - ``scrambler``
     - JESD scrambler block.
   * - .. d2::
          :library: jif
          :theme: light

          ds: Descrambler { class: descrambler }

     - ``descrambler``
     - JESD descrambler block.
   * - .. d2::
          :library: jif
          :theme: light

          transport: Transport { class: transport }

     - ``transport``
     - FPGA transport or JESD application-layer block.
   * - .. d2::
          :library: jif
          :theme: light

          dma: DMA { class: dma }

     - ``dma``
     - DMA engine or memory-facing data mover.
   * - .. d2::
          :library: jif
          :theme: light

          axi: AXI Stream { class: axi-stream }

     - ``axi-stream``
     - AXI-stream or streaming fabric interface.
   * - .. d2::
          :library: jif
          :theme: light

          fabric: Fabric { class: fabric }

     - ``fabric``
     - FPGA fabric or grouped programmable-logic region.
   * - .. d2::
          :library: jif
          :theme: light

          cpu: Processor { class: processor }

     - ``processor``
     - Embedded processor or software-control block.
   * - .. d2::
          :library: jif
          :theme: light

          fpga: FPGA { class: fpga-device }

     - ``fpga-device``
     - Top-level FPGA or SoC device container.

Timing And Annotation Blocks
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 22 24 54

   * - Shape
     - Class
     - Description
   * - .. d2::
          :library: jif
          :theme: light

          ref: REF_IN { class: reference-clock }

     - ``reference-clock``
     - External clock reference input.
   * - .. d2::
          :library: jif
          :theme: light

          clk: Device Clock { class: device-clock }

     - ``device-clock``
     - Converter or FPGA device clock.
   * - .. d2::
          :library: jif
          :theme: light

          sample: Sample Clock { class: sample-clock }

     - ``sample-clock``
     - Converter sample clock.
   * - .. d2::
          :library: jif
          :theme: light

          sysref: SYSREF { class: sysref }

     - ``sysref``
     - JESD204 subclass timing reference.
   * - .. d2::
          :library: jif
          :theme: light

          src: External Source { class: external-source }

     - ``external-source``
     - Signal, clock, or data source outside the modeled system.
   * - .. d2::
          :library: jif
          :theme: light

          title: Capture Path { class: jif-title }

     - ``jif-title``
     - Diagram title text.
   * - .. d2::
          :library: jif
          :theme: light

          note: Subclass 1 deterministic latency { class: jif-note }

     - ``jif-note``
     - Small explanatory note.
   * - .. d2::
          :library: jif
          :theme: light

          chip: LMFS 4421 { class: jif-chip }

     - ``jif-chip``
     - Compact metadata label for rates, LMFS, lane counts, or subclass.

Flow Classes
------------

Apply these classes to edges to make connection semantics visible without
cluttering the diagram.

.. list-table::
   :header-rows: 1
   :widths: 24 26 50

   * - Class
     - Visual Role
     - Use For
   * - ``jif-signal``
     - Default teal connection
     - Generic JIF connections.
   * - ``jif-flow-data``
     - Thicker teal connection
     - Converter sample streams and internal datapaths.
   * - ``jif-flow-clock``
     - Green dashed connection
     - Device clocks, reference clocks, and PLL outputs.
   * - ``jif-flow-sysref``
     - Amber dashed connection
     - SYSREF and deterministic-latency timing markers.
   * - ``jif-flow-lane``
     - Indigo connection
     - JESD serial lanes or lane bundles.
   * - ``jif-flow-control``
     - Muted dotted connection
     - AXI-lite, SPI, software control, and configuration paths.
