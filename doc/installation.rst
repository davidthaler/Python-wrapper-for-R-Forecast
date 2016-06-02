Installation
============

To use this package, you will need Pandas, Matplotlib and R with the forecast package.
You may also want to install the ``fpp`` package, which has useful time series data.
If you install ``fpp``, then that will pull in ``forecast`` as a dependency, 
so that is all you need.

External dependencies:
----------------------

* `Pandas`_ - tested on 0.17.0  
* `Matplotlib`_ - tested 1.4.3  
* `R`_ - tested on 3.1.2  
* `R forecast`_ - tested on 6.1  

Optional dependencies:
----------------------
* `fpp package`_ - contains time series data sets  
* `nose`_ - helpful if you want to run the tests  
* `coverage`_ - if you want coverage statistics

.. _Pandas: http://pandas.pydata.org
.. _Matplotlib: http://matplotlib.org
.. _R: https://www.r-project.org/
.. _R forecast: https://cran.r-project.org/web/packages/forecast/forecast.pdf
.. _fpp package: https://cran.r-project.org/web/packages/fpp/index.html
.. _nose: https://pypi.python.org/pypi/nose/
.. _coverage: https://pypi.python.org/pypi/coverage

Installation Instructions
-------------------------

To install the R packages, start R and then use:

.. code-block:: bash

    install.packages('forecast')
    
The rforecast.py package is installed from git:

.. code-block:: bash

    git clone https://github.com/davidthaler/Python-wrapper-for-R-Forecast.git
    cd Python-wrapper-for-R-Forecast
    python setup.py install


Documentation Build
-------------------

The documentation builds with Sphinx (developed Sphinx 1.3).
If you have Sphinx installed, you can build the documentation using the Makefile 
in ``doc``:

.. code-block:: bash

  cd doc
  make html

Then the built documentation will start at: *doc/_build/html/index.html*.

Testing
-------

Tests are in *test/* under the install directory. 
From that level, if you have nose installed, you can run all of the tests with:

.. code-block:: bash

   nosetests -v

If you have the *coverage* nose plugin, you can get statement coverage

.. code-block:: bash

  nosetests -v --cover-package=rforecast --with-cover
