FROM continuumio/miniconda

LABEL org.colour-science.colour-dash="0.1.0"

RUN apt-get update

RUN /opt/conda/bin/conda install -y -c conda-forge colour-science
RUN pip install dash
RUN pip install dash-core-components
RUN pip install dash-html-components
RUN pip install dash-renderer
RUN pip install gunicorn
RUN pip install plotly

RUN mkdir -p /home/dash/colour-dash
WORKDIR /home/dash/colour-dash
COPY . /home/dash/colour-dash

CMD ["gunicorn", "-b", "0.0.0.0:8000", "index:SERVER"]
