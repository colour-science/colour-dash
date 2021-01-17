Colour - Dash
=============

..  image:: https://www.colour-science.org/images/Apps_Screenshot.png

Introduction
------------

Various colour science `Dash <https://dash.plot.ly/>`__ apps built on top of
`Colour <https://github.com/colour-science/colour>`__.

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

    $ poetry install
    $ poetry run invoke docker-run

Code of Conduct
---------------

The *Code of Conduct*, adapted from the `Contributor Covenant 1.4 <https://www.contributor-covenant.org/version/1/4/code-of-conduct.html>`__,
is available on the `Code of Conduct <https://www.colour-science.org/code-of-conduct/>`__ page.

Contact & Social
----------------

The *Colour Developers* can be reached via different means:

- `Email <mailto:colour-developers@colour-science.org>`__
- `Discourse <https://colour-science.discourse.group/>`__
- `Facebook <https://www.facebook.com/python.colour.science>`__
- `Gitter <https://gitter.im/colour-science/colour>`__
- `Twitter <https://twitter.com/colour_science>`__

About
-----

| **Colour - Dash** by Colour Developers
| Copyright © 2018-2021 – Colour Developers – `colour-developers@colour-science.org <colour-developers@colour-science.org>`__
| This software is released under terms of New BSD License: https://opensource.org/licenses/BSD-3-Clause
| `https://github.com/colour-science/colour-dash <https://github.com/colour-science/colour-dash>`__
