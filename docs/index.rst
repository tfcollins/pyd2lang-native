pyd2lang-native
===============

Native Python bindings for the `d2lang <https://d2lang.com>`_ diagram compiler.
Compile D2 diagram code to SVG directly from Python without requiring the ``d2`` CLI.

Includes a built-in `Analog Devices <https://www.analog.com>`_ component library
with 21 analog/mixed-signal shapes and ADI brand themes.

Installation
------------

.. code-block:: bash

   pip install pyd2lang-native

Quick Start
-----------

.. code-block:: python

   import d2

   svg = d2.compile("x -> y")

With ADI components:

.. code-block:: python

   import d2

   code = """
   direction: right
   adc1: AD7606 { class: adc }
   filt1: LTC1560 { class: filter-lp }
   amp1: LT6230 { class: amplifier }

   amp1 -> filt1: Analog { class: adi-signal-analog }
   filt1 -> adc1: Filtered { class: adi-signal-analog }
   """

   svg = d2.compile(code, adi=True)

.. toctree::
   :maxdepth: 2
   :caption: Contents

   api
   adi
   examples
