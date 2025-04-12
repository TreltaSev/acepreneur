FROM alpine:3.19

## Install Packages
RUN apk add --update --no-cache python3 pipx git libpq-dev gcc py3-pip python3-dev g++

# Install Siblink
RUN git clone https://github.com/TreltaSev/siblink.git && \
    cd ./siblink && \
    pipx install . && \
    cd ../ && \
    rm -rf ./siblink

# Set PATH to use the siblink command
ENV PATH="${PATH}:/root/.local/bin"

# Copy requirements and init early!
WORKDIR /backend
COPY requirements.txt .
RUN siblink init

# Now copy the rest of the backend
COPY . .

CMD ["siblink", "run", "."]
