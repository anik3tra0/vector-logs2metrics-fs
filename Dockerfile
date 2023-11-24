# Use the official Ubuntu as the base image
FROM ruby:2.7-bullseye AS base

# Set environment variables to avoid interactive prompts during installation
ENV BUNDLER_VERSION=2.0.2
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update

RUN curl -1sLf 'https://repositories.timber.io/public/vector/cfg/setup/bash.deb.sh' | bash

# Install Python and pip
RUN apt-get -y install python3 supervisor git vector vim

# copy process manager config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
WORKDIR /app

COPY main.py /app
COPY fluentd.conf /app
COPY vector.yaml /app


RUN git clone https://github.com/fluent/fluentd.git

WORKDIR /app/fluentd

RUN bundle install
RUN bundle exec rake build
RUN gem install pkg/fluentd-*.gem
RUN gem install fluent-plugin-s3 --no-doc
RUN fluentd --setup ./fluent

# run the process manager
CMD ["/usr/bin/supervisord"]
