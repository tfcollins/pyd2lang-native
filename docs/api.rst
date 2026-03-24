API Reference
=============

.. module:: d2

compile
-------

.. autofunction:: d2.compile

Constants
---------

.. py:data:: ADI_COMPONENTS
   :type: list[str]

   List of all available ADI component class names:

   .. code-block:: python

      [
          "adc", "dac", "amplifier", "filter-lp", "filter-bp", "filter-hp",
          "pll", "mixer", "oscillator", "comparator", "summer", "multiplexer",
          "switch", "voltage-reference", "voltage-regulator", "sensor",
          "dsp-fpga", "clock", "driver", "isolator", "attenuator",
      ]

.. py:data:: ADI_THEME_CLASSES
   :type: list[str]

   List of all available ADI theme class names:

   .. code-block:: python

      [
          "adi-container", "adi-signal", "adi-signal-analog",
          "adi-signal-digital", "adi-signal-clock", "adi-signal-power",
          "adi-title", "adi-note",
      ]

.. py:data:: __version__
   :type: str

   Current package version string.
