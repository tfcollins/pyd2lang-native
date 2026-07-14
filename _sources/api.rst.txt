API Reference
=============

.. module:: d2

compile
-------

.. autofunction:: d2.compile

Constants
---------

ADI Library
~~~~~~~~~~~

.. py:data:: ADI_COMPONENTS
   :type: list[str]

   List of all 64 ADI component class names (see :doc:`shapes`).

.. py:data:: ADI_THEME_CLASSES
   :type: list[str]

   List of all ADI theme class names:

   .. code-block:: python

      [
          "adi-container", "adi-signal", "adi-signal-analog",
          "adi-signal-digital", "adi-signal-clock", "adi-signal-power",
          "adi-title", "adi-note",
      ]

SW Library
~~~~~~~~~~

.. py:data:: SW_COMPONENTS
   :type: list[str]

   List of all 32 SW component class names (see :doc:`sw-shapes`).

.. py:data:: SW_THEME_CLASSES
   :type: list[str]

   List of all SW theme class names:

   .. code-block:: python

      [
          "sw-container", "sw-container-cream", "sw-container-green",
          "sw-container-amber", "sw-container-red", "sw-container-white",
          "sw-step-blue", "sw-step-green", "sw-step-amber", "sw-step-white",
          "sw-title", "sw-subtitle", "sw-note",
          "sw-flow", "sw-flow-data", "sw-flow-control", "sw-flow-async",
          "sw-flow-error", "sw-flow-success", "sw-flow-feedback", "sw-flow-light",
      ]

JIF Library
~~~~~~~~~~~

.. py:data:: JIF_COMPONENTS
   :type: list[str]

   List of all JIF component class names used by pyadi-jif ``Node.ntype`` values
   (see :doc:`jif-shapes`).

.. py:data:: JIF_THEME_CLASSES
   :type: list[str]

   List of all JIF theme class names:

   .. code-block:: python

      [
          "jif-container",
          "jif-container-clock", "jif-container-converter", "jif-container-fpga",
          "jif-title", "jif-subtitle", "jif-label", "jif-badge",
          "jif-signal", "jif-signal-reference", "jif-signal-clock",
          "jif-signal-sysref", "jif-signal-data", "jif-signal-feedback",
      ]

DataX Library
~~~~~~~~~~~~~

.. py:data:: DATAX_COMPONENTS
   :type: list[str]

   List of DataX semantic box class names (see :doc:`datax`).

.. py:data:: DATAX_THEME_CLASSES
   :type: list[str]

   List of DataX typography, panel, band, and flow class names (see
   :doc:`datax`).

clean Library
~~~~~~~~~~~~~

.. py:data:: CLEAN_COMPONENTS
   :type: list[str]

   List of the 21 clean component class names (flat, neutral-tint + clay-accent
   technical diagramming shapes; see :doc:`clean-shapes`).

.. py:data:: CLEAN_THEME_CLASSES
   :type: list[str]

   List of clean typography, panel, band, and flow class names.

General
~~~~~~~

.. py:data:: __version__
   :type: str

   Current package version string.
