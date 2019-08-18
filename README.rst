Colour - Dash
=============

..  image:: https://www.colour-science.org/images/Apps_Screenshot.png

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
    -e COLOUR_DASH_CSS=https://www.colour-science.org/assets/css/all-nocdn.css \
    -e COLOUR_DASH_JS=https://www.colour-science.org/assets/js/analytics.js,https://cdnjs.cloudflare.com/ajax/libs/iframe-resizer/3.6.1/iframeResizer.contentWindow.min.js \
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

Code of Conduct
---------------

The *Code of Conduct*, adapted from the `Contributor Covenant 1.4 <https://www.contributor-covenant.org/version/1/4/code-of-conduct.html>`_,
is available on the `Code of Conduct <https://www.colour-science.org/code-of-conduct/>`_ page.

About
-----

| **Colour - Dash** by Colour Developers
| Copyright © 2018-2019 – Colour Developers – `colour-science@googlegroups.com <colour-science@googlegroups.com>`_
| This software is released under terms of New BSD License: https://opensource.org/licenses/BSD-3-Clause
| `https://github.com/colour-science/colour-dash <https://github.com/colour-science/colour-dash>`_
