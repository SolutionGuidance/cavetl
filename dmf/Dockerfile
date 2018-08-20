# This dockerfile sets up and serves the leie application
FROM ubuntu

# Set environment variables, used throughout setup by shell scripts.
ENV DMF_CONFIG /app/config.py

# Install dependencies
FROM ubuntu
RUN apt-get update && apt-get install -y \
  python3 \
  python3-pip \
  python3-dev \
  build-essential

RUN pip3 install pipenv
COPY . /app

# These variables get overwritten if they are set earlier
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
RUN cd /app && pipenv install

# Make sure the app is reachable
EXPOSE 5001

# Run the server
ENTRYPOINT cd /app && pipenv run python3 serve.py