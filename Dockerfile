FROM python:3-alpine

RUN pip install colour-science
RUN pip install dash
RUN pip install dash-core-components
RUN pip install dash-html-components
RUN pip install dash-renderer
RUN pip install numpy
RUN pip install pandas
RUN pip install plotly
RUN pip install scipy

EXPOSE 8050

CMD ['python', 'app.py']