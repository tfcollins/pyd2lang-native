ADI Shapes
==========

The library provides 64 component shapes based on standard EE schematic symbols.
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
   * - ``dds``
     - .. image:: _static/icons/dds.svg
          :width: 80
     - Direct Digital Synthesizer. Digital input with phase accumulator,
       internal DAC, and sine wave output.
     - AD9914, AD9915, AD9833
   * - ``afe``
     - .. image:: _static/icons/afe.svg
          :width: 80
     - Analog Front End. Integrated signal chain with MUX, amplifier,
       filter, and ADC stages.
     - AD4134, ADAS3022, AD7768

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
   * - ``lna``
     - .. image:: _static/icons/lna.svg
          :width: 64
     - Low Noise Amplifier. Triangle with NF (noise figure) indicator.
     - ADL5523, HMC8410, ADL5521
   * - ``pa``
     - .. image:: _static/icons/pa.svg
          :width: 64
     - Power Amplifier. Bold triangle with Pout indicator for RF transmit
       chains.
     - HMC943APM5E, ADL5606, HMC1131
   * - ``gain-block``
     - .. image:: _static/icons/gain-block.svg
          :width: 64
     - RF Gain Block. Triangle with fixed gain label (+dB).
     - ADL5545, ADL5602, HMC311
   * - ``inamp``
     - .. image:: _static/icons/inamp.svg
          :width: 64
     - Instrumentation Amplifier. Triangle with differential +/− inputs
       and RG gain-set resistor.
     - AD8421, AD8220, AD8422
   * - ``tia``
     - .. image:: _static/icons/tia.svg
          :width: 64
     - Transimpedance Amplifier. Triangle with photodiode input and
       feedback resistor (Rf). Current-to-voltage conversion.
     - ADA4352-2, LTC6561, AD8015
   * - ``vga``
     - .. image:: _static/icons/vga.svg
          :width: 64
     - Variable Gain Amplifier. Triangle with gain control arrow
       indicating programmable gain.
     - AD8338, ADL5330, AD8367
   * - ``current-sense``
     - .. image:: _static/icons/current-sense.svg
          :width: 80
     - Current Sense Amplifier. Inline shunt resistor with sense
       amplifier triangle below.
     - AD8210, AD8217, LTC6102

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
   * - ``upconverter``
     - .. image:: _static/icons/upconverter.svg
          :width: 54
     - RF Upconverter / modulator. Mixer circle with upward arrow
       and LO input.
     - ADMV1013, HMC6505A, ADL5375
   * - ``downconverter``
     - .. image:: _static/icons/downconverter.svg
          :width: 54
     - RF Downconverter / demodulator. Mixer circle with downward arrow
       and LO input.
     - ADMV1014, HMC6147A, ADL5380
   * - ``rf-switch``
     - .. image:: _static/icons/rf-switch.svg
          :width: 80
     - RF Switch (SPDT/SP4T). Single pole with multiple throw positions
       for RF signal routing.
     - ADRF5020, HMC544A, ADRF5250
   * - ``rf-transceiver``
     - .. image:: _static/icons/rf-transceiver.svg
          :width: 80
     - Integrated RF Transceiver / MxFE. TX/RX paths with internal
       DAC/ADC and JESD204 digital interface.
     - AD9081, AD9084, ADRV9040
   * - ``clock-buffer``
     - .. image:: _static/icons/clock-buffer.svg
          :width: 80
     - Clock Fanout Buffer. Single input fanning out to multiple
       output clocks for distribution.
     - ADCLK846, ADCLK948, AD9508
   * - ``jitter-cleaner``
     - .. image:: _static/icons/jitter-cleaner.svg
          :width: 80
     - Jitter Cleaner / Clock Conditioner. Noisy clock in, clean
       clock out.
     - AD9544, HMC7044, AD9545

PLL Sub-Components
------------------

Individual building blocks for detailed PLL loop diagrams.

.. list-table::
   :header-rows: 1
   :widths: 15 15 35 35

   * - Class
     - Icon
     - Description
     - Example Parts
   * - ``pfd``
     - .. image:: _static/icons/pfd.svg
          :width: 80
     - Phase-Frequency Detector. Compares REF and feedback phases,
       outputs UP/DN pulses.
     - Integrated in ADF4351, ADF4159, HMC830
   * - ``charge-pump``
     - .. image:: _static/icons/charge-pump.svg
          :width: 80
     - Charge pump. Converts PFD UP/DN pulses to current output
       with matched source/sink current sources.
     - Integrated in ADF4351, HMC830
   * - ``loop-filter``
     - .. image:: _static/icons/loop-filter.svg
          :width: 80
     - Loop filter. RC network (second-order shown) that filters
       charge pump output to produce VCO tuning voltage.
     - Passive RC, active op-amp implementations
   * - ``vco``
     - .. image:: _static/icons/vco.svg
          :width: 54
     - Voltage-Controlled Oscillator. Circle with sine wave and
       Vtune input arrow.
     - HMC586, HMC733, integrated in ADF4351
   * - ``divider``
     - .. image:: _static/icons/divider.svg
          :width: 64
     - Frequency divider (÷N). Divides output frequency for
       PLL feedback path.
     - Integrated in ADF4351, HMC439, HMC862A

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
   * - ``digipot``
     - .. image:: _static/icons/digipot.svg
          :width: 64
     - Digital Potentiometer. Resistor with digitally-controlled wiper
       and SPI/I²C interface.
     - AD5292, AD5204, AD5270

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
   * - ``ldo``
     - .. image:: _static/icons/ldo.svg
          :width: 80
     - Low-Dropout Regulator. Vin/Vout with internal pass element
       and ground pin.
     - ADP1740, ADP7118, ADM7150
   * - ``dc-dc-buck``
     - .. image:: _static/icons/dc-dc-buck.svg
          :width: 80
     - Buck (Step-Down) Converter. Downward arrow with inductor
       symbol on output.
     - LT8610, ADP5054, LTM4700
   * - ``dc-dc-boost``
     - .. image:: _static/icons/dc-dc-boost.svg
          :width: 80
     - Boost (Step-Up) Converter. Upward arrow with inductor
       on input and diode.
     - LT8330, ADP1613, LT3467
   * - ``pmic``
     - .. image:: _static/icons/pmic.svg
          :width: 80
     - Power Management IC. Multi-rail output (3.3V, 1.8V, 1.2V)
       from single input.
     - MAX77714, ADP5350, LTC3589
   * - ``power-monitor``
     - .. image:: _static/icons/power-monitor.svg
          :width: 80
     - Power Monitor. Inline shunt resistor with V, I, P measurement
       block below.
     - LTC2947, LTC2945, ADM1278
   * - ``hot-swap``
     - .. image:: _static/icons/hot-swap.svg
          :width: 80
     - Hot Swap Controller. MOSFET switch with gate control and
       inrush protection.
     - LTC4287, ADM1272, LTC4260
   * - ``battery-charger``
     - .. image:: _static/icons/battery-charger.svg
          :width: 80
     - Battery Charger. Input power through charger block to
       battery symbol.
     - LTC4162, ADP5350, LT3650

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
   * - ``imu``
     - .. image:: _static/icons/imu.svg
          :width: 64
     - Inertial Measurement Unit. X/Y/Z axis indicator with rotation
       arrow for 6DOF/9DOF sensing.
     - ADIS16465, ADIS16505, ADIS16448
   * - ``temp-sensor``
     - .. image:: _static/icons/temp-sensor.svg
          :width: 64
     - Temperature Sensor IC. Thermometer symbol with scale marks
       and digital output.
     - ADT7420, ADT7310, TMP36

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
   * - ``jesd204``
     - .. image:: _static/icons/jesd204.svg
          :width: 80
     - JESD204B/C SerDes. Parallel data to high-speed serial lanes
       for converter-to-FPGA links.
     - AD9082, AD9144, AD9680
   * - ``lvds``
     - .. image:: _static/icons/lvds.svg
          :width: 80
     - LVDS Driver/Receiver. Single-ended to differential pair
       conversion with D+/D− outputs.
     - ADN4661, ADN4662, ADN4663

Industrial Interfaces
---------------------

.. list-table::
   :header-rows: 1
   :widths: 15 15 35 35

   * - Class
     - Icon
     - Description
     - Example Parts
   * - ``rs485``
     - .. image:: _static/icons/rs485.svg
          :width: 80
     - RS-485 Transceiver. Logic TX/RX on one side, differential
       A/B bus on the other.
     - ADM485, ADM2587E, MAX13487E
   * - ``can``
     - .. image:: _static/icons/can.svg
          :width: 80
     - CAN Bus Transceiver. TXD/RXD logic side to CANH/CANL
       differential bus.
     - ADM3055E, MAX33012E, ADM3053
   * - ``ethernet-phy``
     - .. image:: _static/icons/ethernet-phy.svg
          :width: 80
     - Ethernet PHY Transceiver. MII digital bus to MDI/RJ45
       physical interface.
     - ADIN1110, ADIN2111, ADIN1300

Motor & Gate Drive
------------------

.. list-table::
   :header-rows: 1
   :widths: 15 15 35 35

   * - Class
     - Icon
     - Description
     - Example Parts
   * - ``motor-driver``
     - .. image:: _static/icons/motor-driver.svg
          :width: 80
     - Motor Driver / H-Bridge. Four switches in H configuration
       driving a motor.
     - TMC5160, TMC2209, ADuM7234
   * - ``gate-driver``
     - .. image:: _static/icons/gate-driver.svg
          :width: 80
     - Gate Driver. Logic input through isolation barrier to
       high-current MOSFET/IGBT gate drive output.
     - ADuM4135, ADuM7234, LTC7060
