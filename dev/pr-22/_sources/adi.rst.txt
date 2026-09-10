ADI Component Library
=====================

The built-in Analog Devices component library provides 21 analog/mixed-signal
component shapes and ADI-branded theme classes. Enable it by passing
``library="adi"`` to :func:`d2.compile`.

.. code-block:: python

   import d2

   svg = d2.compile(code, library="adi")

.. image:: _static/signal-chain-example.svg
   :alt: ADI signal chain example
   :align: center

.. toctree::
   :maxdepth: 2

   shapes
   theme
