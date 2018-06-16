Colour - Dash
=============

..  image:: https://colour-science.org/images/Apps_Screenshot.png

Introduction
------------

Various colour science `Dash <https://dash.plot.ly/>`_ apps built on top of
`Colour <https://github.com/colour-science/colour>`_.

Installation
------------

Pull
~~~~

.. code-block:: bash

    $ docker pull colourscience/colour-dash

Run
~~~

.. code-block:: bash

    $ docker run -d \
    --name=colour-dash \
    -e COLOUR_DASH_SERVER=http://example.com:8010/ \
    -e COLOUR_DASH_CSS=https://colour-science.org/assets/css/all-nocdn.css \
    -e COLOUR_DASH_JS=https://colour-science.org/assets/js/analytics.js,https://cdnjs.cloudflare.com/ajax/libs/iframe-resizer/3.6.1/iframeResizer.contentWindow.min.js \
    -p 8010:8000 colourscience/colour-dash

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
