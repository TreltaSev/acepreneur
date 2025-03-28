FROM alpine:3.19

## Install Packages
RUN apk add --update --no-cache python3 pipx git libpq-dev gcc py3-pip python3-dev g++

# Instal Siblnk
RUN git clone https://github.com/TreltaSev/siblink.git && \
    cd ./siblink && \
    pipx install . && \
    cd ../ && \
    rm -rf ./siblink

# Set path to use the siblink command

ENV PATH = "${PATH}:/root/.local/bin"

# Copy Project
COPY . /backend
WORKDIR /backend

# Build backend w/ Siblink
RUN siblink init

CMD ["siblink", "run", "."]