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
   :widths: 28 72

   * - Class
     - Description
   * - ``adc``
     - Analog-to-digital converter block.
   * - ``dac``
     - Digital-to-analog converter block.
   * - ``ddc``
     - Digital downconverter or decimation block.
   * - ``duc``
     - Digital upconverter or interpolation block.
   * - ``crossbar``
     - Crossbar, router, or converter datapath mux.
   * - ``mux``
     - Multiplexer or clock/data select block.
   * - ``jesd204framer``
     - JESD204 framer block inside a converter.
   * - ``jesd204deframer``
     - JESD204 deframer block inside a converter.
   * - ``framer``
     - Remote JESD204 framer block.
   * - ``deframer``
     - Remote JESD204 deframer block.

Clocking Blocks
---------------

.. list-table::
   :header-rows: 1
   :widths: 28 72

   * - Class
     - Description
   * - ``input``
     - External reference, SYSREF, or device-clock input.
   * - ``out_clock_connected``
     - Output clock pin or connected clock output.
   * - ``divider``
     - Clock, feedback, output, or transceiver divider.
   * - ``phase-frequency-detector``
     - PLL phase-frequency detector.
   * - ``charge-pump``
     - PLL charge-pump block.
   * - ``loop-filter``
     - PLL loop-filter block.
   * - ``vco``
     - Voltage-controlled oscillator.
   * - ``voltage-controlled-oscillator``
     - Long-form VCO class used by some pyadi-jif clock drawings.
   * - ``cdr``
     - Clock-data recovery block.

FPGA And System Blocks
----------------------

.. list-table::
   :header-rows: 1
   :widths: 28 72

   * - Class
     - Description
   * - ``shell``
     - Grouping shell for internal sub-blocks.
   * - ``ip``
     - FPGA IP block such as JESD link, transport, or application logic.
   * - ``phy``
     - FPGA PHY block.
   * - ``transceiver``
     - FPGA transceiver block.
   * - ``serdes``
     - Serializer/deserializer block.
   * - ``decoder``
     - Link-layer decoder block.
   * - ``cpll``
     - Channel PLL block.
   * - ``qpll``
     - Quad PLL block.
   * - ``trx-dividers``
     - Transceiver divider and mux group.
