FROM continuumio/anaconda3
MAINTAINER TLQ, https://liquntang.wordpress.com/
EXPOSE 5000
RUN apt-get update && apt-get install -y apache2 apache2-dev vim \
 && apt-get clean \
 && apt-get autoremove \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /var/www/hashtag_app/
COPY ./hashtag_app.wsgi /var/www/hashtag_app/hashtag_app.wsgi
COPY ./hashtag_app /var/www/hashtag_app
RUN pip install -r requirements.txt
RUN /opt/conda/bin/mod_wsgi-express install-module
RUN mod_wsgi-express setup-server hashtag_app.wsgi \
    --port=5000 --user www-data \--group www-data \
    --server-root=/etc/mod_wsgi-express-80

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y locales
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8
ENV LANG en_US.UTF-8 

CMD /etc/mod_wsgi-express-80/apachectl start -D FOREGROUND
