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

General
~~~~~~~

.. py:data:: __version__
   :type: str

   Current package version string.
