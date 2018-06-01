FROM nginx:alpine

LABEL org.colour-science.colour-nginx="0.1.0"

RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/

RUN rm /etc/nginx/conf.d/default.conf
COPY dash.conf /etc/nginx/conf.d/
