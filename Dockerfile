FROM continuumio/miniconda

RUN apt-get update

RUN /opt/conda/bin/conda install -y -c conda-forge colour-science
RUN pip install \
    dash \
    dash-core-components \
    dash-html-components \
    dash-renderer \
    gunicorn \
    plotly

RUN mkdir -p /home/dash/colour-dash
WORKDIR /home/dash/colour-dash
COPY . /home/dash/colour-dash

CMD sh -c 'if [ -z "${SSL_CERTIFICATE}" ]; then \
    gunicorn --log-level debug -b 0.0.0.0:8000 index:SERVER; else \
    gunicorn --certfile "${SSL_CERTIFICATE}" --keyfile "${SSL_KEY}" --log-level debug -b 0.0.0.0:8000 index:SERVER; fi'
