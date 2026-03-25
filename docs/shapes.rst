ADI Shapes
==========

The library provides 27 component shapes based on standard EE schematic symbols.
Each shape is a D2 class applied with ``class: <name>``.

.. image:: _static/all-components.svg
   :alt: All ADI component shapes
   :align: center

Usage
-----

.. code-block:: python

   import d2

   code = """
   adc1: AD7606 { class: adc }
   amp1: LT6230 { class: amplifier }
   filt1: LTC1560 { class: filter-lp }

   amp1 -> filt1 -> adc1
   """

   svg = d2.compile(code, adi=True)

Data Converters
---------------

.. list-table::
   :header-rows: 1
   :widths: 15 15 35 35

   * - Class
     - Icon
     - Description
     - Example Parts
   * - ``adc``
     - .. image:: _static/icons/adc.svg
          :width: 80
     - Analog-to-Digital Converter. Five-sided shape (rectangle + triangle
       pointing right) with analog input waveform, arrow, and digital
       staircase output.
     - AD7606, AD9680, AD4020
   * - ``dac``
     - .. image:: _static/icons/dac.svg
          :width: 80
     - Digital-to-Analog Converter. Five-sided shape (triangle pointing left +
       rectangle) with digital staircase input, arrow, and analog output
       waveform.
     - AD5686, AD9144, AD1955

Amplifiers & Drivers
--------------------

.. list-table::
   :header-rows: 1
   :widths: 15 15 35 35

   * - Class
     - Icon
     - Description
     - Example Parts
   * - ``amplifier``
     - .. image:: _static/icons/amplifier.svg
          :width: 64
     - Op-amp / amplifier. Standard triangle symbol with inverting (−)
       and non-inverting (+) inputs.
     - LT6230, ADA4945, AD8251
   * - ``comparator``
     - .. image:: _static/icons/comparator.svg
          :width: 64
     - Comparator. Triangle with +/− inputs and threshold output
       indicators.
     - ADCMP600, ADCMP601, LT1016
   * - ``driver``
     - .. image:: _static/icons/driver.svg
          :width: 64
     - Buffer / line driver. Triangle with emphasized output bar.
     - ADA4897, ADN4605, AD8137

Filters
-------

.. list-table::
   :header-rows: 1
   :widths: 15 15 35 35

   * - Class
     - Icon
     - Description
     - Example Parts
   * - ``filter-lp``
     - .. image:: _static/icons/filter-lp.svg
          :width: 80
     - Low-pass filter. Rectangle with frequency response showing
       flat passband rolling off at cutoff.
     - LTC1560, LT1568, ADA4528
   * - ``filter-bp``
     - .. image:: _static/icons/filter-bp.svg
          :width: 80
     - Band-pass filter. Rectangle with frequency response showing
       a peaked passband.
     - ADA4945, SAW filters
   * - ``filter-hp``
     - .. image:: _static/icons/filter-hp.svg
          :width: 80
     - High-pass filter. Rectangle with frequency response showing
       roll-up from low frequencies to a flat passband.
     - Active RC implementations

Frequency Synthesis
-------------------

.. list-table::
   :header-rows: 1
   :widths: 15 15 35 35

   * - Class
     - Icon
     - Description
     - Example Parts
   * - ``pll``
     - .. image:: _static/icons/pll.svg
          :width: 80
     - Phase-Locked Loop. Rectangle with feedback loop symbol.
     - ADF4351, ADF4159, HMC830
   * - ``mixer``
     - .. image:: _static/icons/mixer.svg
          :width: 54
     - Mixer. Circle with X — the standard frequency mixer symbol.
     - ADL5801, HMC220, LTC5548
   * - ``oscillator``
     - .. image:: _static/icons/oscillator.svg
          :width: 54
     - Oscillator / VCO. Circle with sine wave inside.
     - ADCLK948, HMC-series VCOs
   * - ``clock``
     - .. image:: _static/icons/clock.svg
          :width: 80
     - Clock generator. Rectangle with square wave symbol.
     - AD9520, AD9528, HMC7044

Signal Routing
--------------

.. list-table::
   :header-rows: 1
   :widths: 15 15 35 35

   * - Class
     - Icon
     - Description
     - Example Parts
   * - ``multiplexer``
     - .. image:: _static/icons/multiplexer.svg
          :width: 64
     - Multiplexer. Trapezoid shape — wide inputs, narrow output.
     - ADG1206, ADG1606, ADG726
   * - ``switch``
     - .. image:: _static/icons/switch.svg
          :width: 80
     - Analog switch. Rectangle with open switch contact symbol.
     - ADG1419, ADG836, ADG1213
   * - ``summer``
     - .. image:: _static/icons/summer.svg
          :width: 48
     - Summing junction. Circle with + symbol.
     - Op-amp summing circuits
   * - ``attenuator``
     - .. image:: _static/icons/attenuator.svg
          :width: 80
     - Attenuator. Rectangle with pi-pad resistor network symbol.
     - HMC472A, HMC624A

Power & Reference
-----------------

.. list-table::
   :header-rows: 1
   :widths: 15 15 35 35

   * - Class
     - Icon
     - Description
     - Example Parts
   * - ``voltage-reference``
     - .. image:: _static/icons/voltage-reference.svg
          :width: 80
     - Voltage reference. Rectangle with zener diode symbol.
     - ADR4525, ADR3440, LT6656
   * - ``voltage-regulator``
     - .. image:: _static/icons/voltage-regulator.svg
          :width: 80
     - Voltage regulator. Rectangle with REG block, input/output arrows,
       and ground symbol.
     - ADP7118, ADP1720, LT3045

Digital & Sensing
-----------------

.. list-table::
   :header-rows: 1
   :widths: 15 15 35 35

   * - Class
     - Icon
     - Description
     - Example Parts
   * - ``dsp-fpga``
     - .. image:: _static/icons/dsp-fpga.svg
          :width: 80
     - DSP / FPGA. Rectangle with chip grid pattern and pin indicators.
     - ADSP-21489, ADSP-BF706
   * - ``sensor``
     - .. image:: _static/icons/sensor.svg
          :width: 80
     - Sensor. Rectangle with measurement waveform symbol.
     - ADXL345, AD590, ADIS16475
   * - ``isolator``
     - .. image:: _static/icons/isolator.svg
          :width: 80
     - Digital isolator. Rectangle split by dashed isolation barrier
       with signal arrows passing through.
     - ADuM1201, ADuM4160, ADuM3160

Beamforming
-----------

.. list-table::
   :header-rows: 1
   :widths: 15 15 35 35

   * - Class
     - Icon
     - Description
     - Example Parts
   * - ``beamformer``
     - .. image:: _static/icons/beamformer.svg
          :width: 80
     - Beamformer IC. Array of antenna elements converging into a beam
       pattern with radiation lines.
     - ADAR1000, ADAR3002, ADMV4828

FPGA IP & Interfaces
--------------------

.. list-table::
   :header-rows: 1
   :widths: 15 15 35 35

   * - Class
     - Icon
     - Description
     - Example Parts
   * - ``axi-interconnect``
     - .. image:: _static/icons/axi-interconnect.svg
          :width: 80
     - AXI interconnect / crossbar. Grid of bus lines with junction dots
       representing the switch matrix.
     - Xilinx AXI Interconnect IP, Intel Avalon
   * - ``spi``
     - .. image:: _static/icons/spi.svg
          :width: 80
     - SPI bus interface. Four labeled signal lines (SCLK, MOSI, MISO, CS)
       with directional arrows.
     - Xilinx AXI Quad SPI, custom SPI controllers
   * - ``gpio``
     - .. image:: _static/icons/gpio.svg
          :width: 80
     - GPIO bank. Grid of I/O pin indicators with bidirectional arrows.
     - Xilinx AXI GPIO, MCP23017
   * - ``i2c``
     - .. image:: _static/icons/i2c.svg
          :width: 80
     - I²C bus interface. Two-wire bus (SCL/SDA) with pull-up resistors,
       device tap, and bidirectional arrows.
     - Xilinx AXI IIC, custom I2C controllers
   * - ``aurora``
     - .. image:: _static/icons/aurora.svg
          :width: 80
     - Aurora high-speed serial link. TX/RX lanes with differential pair
       indicators for multi-gigabit interconnect.
     - Xilinx Aurora 8B/10B, Aurora 64B/66B
