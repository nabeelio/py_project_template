#
# Build a docker image and run the soccerbot application within
# with the python env being setup
#

# using debian jessie
# https://hub.docker.com/_/buildpack-deps/
#FROM buildpack-deps:trusty

FROM nabeelio/alpine-py:latest
MAINTAINER Nabeel Shahzad <hi@nabs.io>

ENV APP_HOME /opt/{{cookiecutter.package_name}}
ENV PATH "/opt/{{cookiecutter.package_name}}/env/bin:$PATH"

COPY scripts/chaperone.conf /etc/chaperone.d/chaperone.conf

RUN mkdir -p $APP_HOME
COPY . $APP_HOME

WORKDIR $APP_HOME
RUN pip install -r requirements.txt

CMD /usr/bin/chaperone --force
