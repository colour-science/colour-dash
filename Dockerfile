FROM continuumio/miniconda

LABEL org.colour-science.colour-dash="0.1.0"

RUN apt-get update
RUN /opt/conda/bin/conda install -y -c conda-forge colour-science
RUN /opt/conda/bin/conda install -y pandas
RUN pip install dash
RUN pip install dash-core-components
RUN pip install dash-html-components
RUN pip install dash-renderer
RUN pip install plotly

EXPOSE 8050

CMD ["python", "app.py"]