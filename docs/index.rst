pyd2lang-native
===============

Native Python bindings for the `d2lang <https://d2lang.com>`_ diagram compiler.
Compile D2 diagram code to SVG directly from Python without requiring the ``d2`` CLI.

Includes two built-in component libraries with ADI brand themes:

- **ADI** — 64 analog/mixed-signal shapes for signal chain diagrams
- **SW** — 32 software/AI shapes for architecture and agent pipeline diagrams

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

   svg = d2.compile(code, library="adi")

With SW components:

.. code-block:: python

   import d2

   code = """
   agent: Auditor { class: sw-agent }
   model: Claude { class: sw-model }
   tool: Search { class: sw-tool }
   doc: Seed { class: sw-document }

   doc -> agent { class: sw-flow-data }
   agent -> tool -> model { class: sw-flow }
   model -> agent { class: sw-flow-feedback }
   """

   svg = d2.compile(code, library="sw")

.. toctree::
   :maxdepth: 2
   :caption: Contents

   api
   adi
   sw
   examples
