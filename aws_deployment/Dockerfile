FROM --platform=x86_64 ubuntu:22.04 as build

#RUN apt-get install -y python-pip python3-dev curl unzip
RUN apt-get update && apt-get install -y curl unzip python3-pip

WORKDIR /app/deployment/

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && unzip awscliv2.zip && ./aws/install

COPY --chown=user:777 requirements.txt /app/deployment/requirements.txt
COPY --chown=user:777 requirements-dev.txt /app/deployment/requirements-dev.txt


RUN pip install -r requirements.txt && pip install -r requirements-dev.txt

COPY --chown=user:777  . .



FROM build as execute

CMD ["/bin/bash", "-c", "cdk synth", "&&", "cdk bootstrap"]