Examples
========

Basic Diagram
-------------

Compile a simple D2 diagram to SVG:

.. code-block:: python

   import d2

   svg = d2.compile("x -> y -> z")

   # Write to file
   with open("output.svg", "w") as f:
       f.write(svg)

Signal Chain
------------

A typical ADI signal chain with sensor, conditioning, and digitization:

.. code-block:: python

   import d2

   code = """
   direction: right

   sensor: ADXL345 { class: sensor }
   amp: LT6230 { class: amplifier }
   filt: LTC1560 { class: filter-lp }
   adc: AD7606 { class: adc }
   dsp: ADSP-21489 { class: dsp-fpga }

   sensor -> amp: Analog { class: adi-signal-analog }
   amp -> filt: Amplified { class: adi-signal-analog }
   filt -> adc: Filtered { class: adi-signal-analog }
   adc -> dsp: SPI { class: adi-signal-digital }

   clk: AD9520 { class: clock }
   clk -> adc: MCLK { class: adi-signal-clock }
   """

   svg = d2.compile(code, adi=True)

Nested Subsystems
-----------------

Group components into named subsystem containers:

.. code-block:: python

   import d2

   code = """
   analog-frontend: Analog Front End {
     class: adi-container

     amp: LNA { class: amplifier }
     filt: Anti-Alias { class: filter-lp }
     adc: AD7606 { class: adc }

     amp -> filt { class: adi-signal-analog }
     filt -> adc { class: adi-signal-analog }
   }

   digital-backend: Digital Backend {
     class: adi-container

     dsp: ADSP-21489 { class: dsp-fpga }
     dac: AD5686 { class: dac }

     dsp -> dac { class: adi-signal-digital }
   }

   analog-frontend -> digital-backend: SPI { class: adi-signal-digital }
   """

   svg = d2.compile(code, adi=True)

RF Receiver
-----------

An RF receiver front end with LO generation:

.. code-block:: python

   import d2

   code = """
   direction: right

   rf-frontend: RF Front End {
     class: adi-container

     lna: HMC8410 { class: amplifier }
     bpf: SAW Filter { class: filter-bp }
     mix: ADL5801 { class: mixer }

     lna -> bpf { class: adi-signal-analog }
     bpf -> mix { class: adi-signal-analog }
   }

   lo: LO Generation {
     class: adi-container

     pll: ADF4351 { class: pll }
     vco: VCO { class: oscillator }
     pll -> vco { class: adi-signal-analog }
   }

   lo -> rf-frontend.mix: LO { class: adi-signal-analog }

   adc: AD9680 { class: adc }
   rf-frontend -> adc: IF { class: adi-signal-analog }
   """

   svg = d2.compile(code, adi=True)

Dark Theme
----------

Use the dark variant for dark-background contexts:

.. code-block:: python

   import d2

   code = """
   adc: AD7606 { class: adc }
   dac: AD5686 { class: dac }
   adc -> dac: SPI { class: adi-signal-digital }
   """

   svg = d2.compile(code, adi=True, theme="dark")

Error Handling
--------------

Invalid D2 code raises ``RuntimeError``:

.. code-block:: python

   import d2

   try:
       svg = d2.compile("invalid {{ code", adi=True)
   except RuntimeError as e:
       print(f"Compilation failed: {e}")

Programmatic Component Listing
------------------------------

Iterate over available components:

.. code-block:: python

   import d2

   print("Available components:")
   for comp in d2.ADI_COMPONENTS:
       print(f"  - {comp}")

   print("Available theme classes:")
   for cls in d2.ADI_THEME_CLASSES:
       print(f"  - {cls}")
