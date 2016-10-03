FROM python:2.7.12

MAINTAINER lAzUr <jonwing.lee@gmail.com>

ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR off
ENV PIP_DISABLE_PIP_VERSION_CHECK on

RUN mkdir /application
RUN mkdir /log
WORKDIR /application

ADD requirement.txt /application
ADD etc /etc
ADD Feiton /application
RUN pip install -r requirement.txt -i http://pypi.doubanio.com/simple --trusted-host=pypi.doubanio.com && rm -f requirement.txt

VOLUME /www

# application env
ENV STATIC /www

EXPOSE 80
ADD entry-point.sh /
RUN chmod +x /entry-point.sh
ADD startup.sh /
RUN chmod +x /startup.sh
ENTRYPOINT ["/entry-point.sh"]
CMD ["/startup.sh"]
