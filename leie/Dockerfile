# This dockerfile sets up and serves the leie application
FROM ubuntu

# Set environment variables, used throughout setup by shell scripts.
ENV GOPATH /app/golang
ENV PATH $PATH:$GOPATH/bin

# Install dependencies
RUN apt-get update && apt-get install -y \
  sqlite3 \
  python3 \
  python3-pip \
  python3-dev \
  build-essential \
  git \
  golang-go \
  pandoc

COPY . /app
RUN cd /app && pip3 install -r requirements.txt
RUN mkdir -p /app/golang
RUN go get -u -v github.com/pressly/goose/cmd/goose

# Kick off the migrations
RUN cd /app/leie && ./model.py && ./etl.py

# Make sure the app is reachable
EXPOSE 5000

# Run the server
ENTRYPOINT cd /app/leie && ./serve.py