FROM continuumio/anaconda3
MAINTAINER TLQ, https://liquntang.wordpress.com/
COPY ./hashtag_app /usr/local/python/
EXPOSE 5000
WORKDIR /usr/local/python/
RUN pip install -r requirements.txt
ENV LANG C.UTF-8
CMD python app.py