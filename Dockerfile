FROM ubuntu

MAINTAINER Hamid Samani "samani.hamid@gmail.com"

# Update the sources list
RUN apt-get update

# Install required packages
RUN apt-get install python3-minimal

# Create work directory
RUN mkdir -p home/app

# Copy source files to work directory
ADD source/*.py /home/app/

# Specify work directory
WORKDIR home/app