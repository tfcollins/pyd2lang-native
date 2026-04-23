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
