Colour - Dash
=============

..  image:: http://colour-science.org/images/Apps_Screenshot.png

Introduction
------------

Various `Dash <https://dash.plot.ly/>`_ apps using `Colour <https://github.com/colour-science/colour>`_.

Installation
------------

Pull
~~~~

.. code-block:: bash

    $ docker pull colourscience/colour-dash

Run
~~~

.. code-block:: bash

    $ docker run -d --name=colour-dash -p 8010:8000 colourscience/colour-dash

Development
-----------

.. code-block:: bash

    $ conda create -y -n python-colour-dash
    $ source activate python-colour-dash
    $ conda install -y -c conda-forge colour-science
    $ conda install invoke
    $ pip install dash dash-core-components dash-html-components dash-renderer plotly
    $ python index.py

About
-----

| **Colour - Dash** by Colour Developers
| Copyright © 2018 – Colour Developers – `colour-science@googlegroups.com <colour-science@googlegroups.com>`_
| This software is released under terms of New BSD License: http://opensource.org/licenses/BSD-3-Clause
| `http://github.com/colour-science/colour-dash <http://github.com/colour-science/colour-dash>`_
