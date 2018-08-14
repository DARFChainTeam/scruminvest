FROM python:3.6-slim
#FROM ethereum/vyper

# Specify label-schema specific arguments and labels.
ARG BUILD_DATE
ARG VCS_REF
ARG WORKPATH

LABEL org.label-schema.build-date=$BUILD_DATE \
    org.label-schema.name="Vyper" \
    org.label-schema.description="Vyper is an experimental programming language" \
    org.label-schema.url="https://vyper.readthedocs.io/en/latest/" \
    org.label-schema.vcs-ref=$VCS_REF \
    org.label-schema.vcs-url="https://github.com/ethereum/vyper" \
    org.label-schema.vendor="Ethereum" \
    org.label-schema.schema-version="1.0"

# coincurve requires libgmp
RUN apt-get update && \
    apt-get install -y --no-install-recommends apt-utils gcc libc6-dev libc-dev libssl-dev libgmp-dev pkg-config autoconf automake apt-utils libtool-bin libsecp256k1-dev git mc  && \
    rm -rf /var/lib/apt/lists/*
RUN pip install populus

# spike for Populus Compile Error : "Force_Text"
RUN pip install eth-utils==0.8.1 web3==3.16.5


RUN pip install git+git://github.com/ethereum/vyper.git
RUN  apt-get purge -y --auto-remove apt-utils gcc libc6-dev libc-dev libssl-dev pkg-config autoconf automake apt-utils libtool-bin libsecp256k1-dev

ADD $WORKPATH  /code

WORKDIR /code


ENTRYPOINT ["/bin/bash"]
