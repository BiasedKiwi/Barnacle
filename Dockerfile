FROM ubuntu:latest

# Update packages.
RUN apt-get update
RUN apt-get upgrade -y

# Install Git.
RUN apt-get install -y git

# Create the barnacle directory, and cd into it.
RUN mkdir -p /barnacle
WORKDIR /barnacle
COPY . .

# Install dependencies.
RUN apt-get install -y python3 python3-setuptools python3-pip
RUN pip install -r requirements.txt

# Start Barnacle.
CMD [ "python3", "launcher.py" ]
