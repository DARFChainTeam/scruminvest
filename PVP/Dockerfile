FROM python:3.6-slim
#FROM ethereum/vyper
#FROM ethereum/solc

# Specify label-schema specific arguments and labels.
ARG BUILD_DATE
ARG VCS_REF

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
    apt-get install -y --no-install-recommends  apt-utils 
RUN apt-get install -y --no-install-recommends gnupg2 
RUN apt-get install -y --no-install-recommends dirmngr  
RUN apt-get install -y --no-install-recommends software-properties-common  
RUN apt-get install -y --no-install-recommends gcc 
RUN apt-get install -y --no-install-recommends libc6-dev 
RUN apt-get install -y --no-install-recommends libc-dev 
RUN apt-get install -y --no-install-recommends libssl-dev 
RUN apt-get install -y --no-install-recommends libgmp-dev 
RUN apt-get install -y --no-install-recommends pkg-config 
RUN apt-get install -y --no-install-recommends autoconf 
RUN apt-get install -y --no-install-recommends automake 
RUN apt-get install -y --no-install-recommends apt-utils 
RUN apt-get install -y --no-install-recommends libtool-bin 
RUN apt-get install -y --no-install-recommends libsecp256k1-dev 
RUN apt-get install -y --no-install-recommends git 
RUN apt-get install -y --no-install-recommends mc  

# RUN     rm -rf /var/lib/apt/lists/*

RUN pip install py-solc

RUN pip install populus

# spike for Populus Compile Error : "Force_Text"
RUN pip install eth-utils==0.8.1 web3==3.16.5

RUN pip install git+git://github.com/ethereum/vyper.git
#RUN  apt-get purge -y --auto-remove apt-utils gcc libc6-dev libc-dev libssl-dev pkg-config autoconf automake apt-utils libtool-bin libsecp256k1-dev



ADD .  /code

WORKDIR /code


ENTRYPOINT ["/bin/bash"]
