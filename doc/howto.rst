How-To
======

Loading data
------------

Functions to read time series in with the correct index are in ``rforecast.ts_io``

To read data from a .csv file into a suitable Pandas Series:

.. code-block:: python

   from rforecast import ts_io
   x = ts_io.read_series('data/aus.csv')

To read in a time series in an R package, use ``ts_io.read_ts``. Here we read 
the *livestock* series from package ``fpp``.

.. code-block:: python

   x = ts_io.read_ts('livestock', pkgname='fpp')


Forecasting
-----------

Forecasting functions are in ``rforecast.wrappers``.

To construct a forecast, using the ``forecast`` function in R forecast:

.. code-block:: python

  from rforecast import wrappers
  fc = wrappers.forecast(x)

That function uses ``stlf`` if the series is non-seasonal with frequency 
greater that 12, and otherwise uses ``ets``.


Decomposition
-------------

Seasonal decompositions are in ``rforecast.wrappers``.

To get an STL decomposition:

.. code-block:: python

  dc = wrappers.stl(x, s_window=7)
  
Plotting
--------

Plot functions are in ``rforecast.plots``

To plot forecast prediction intervals:

.. code-block:: python

  plots.plot_forecast(fc, data=x)
  
If you have test data for the forecast period, you can plot that, too.

.. code-block:: python

  plots.plot_forecast(fc, data=x, test=x_test)

To plot a decomposition:

.. code-block:: python

  plots.plot_decomp(dc)
  






