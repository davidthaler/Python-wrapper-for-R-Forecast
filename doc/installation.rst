Installation
============

To use this package, you will need Pandas and R with the forecast package.
You may also want to install the ``fpp`` package, which has useful time series data.
If you install ``fpp``, then that will pull in ``forecast`` as a dependency, 
so that is all you need.

External dependencies:
----------------------

* `Pandas`_ - tested on 0.17.0  
* `R`_ - tested on 3.1.2  
* `R forecast`_ - tested on 6.1  

Optional dependencies:
----------------------
* `fpp package`_ - contains time series data sets  
* `nose`_ - helpful if you want to run the tests  

.. _Pandas: http://pandas.pydata.org
.. _R: https://www.r-project.org/
.. _R forecast: https://cran.r-project.org/web/packages/forecast/forecast.pdf
.. _fpp package: https://cran.r-project.org/web/packages/fpp/index.html
.. _nose: https://nose.readthedocs.org


Instructions
------------

To install the R packages, start R and then use:

.. code-block:: bash

    install.packages('forecast')
    
The rforecast.py package is installed from git:

.. code-block:: bash

    git clone https://github.com/davidthaler/Python-wrapper-for-R-Forecast.git
    python setup.py install
