# test coin dockerfile
FROM ubuntu:latest

# ssh part:

RUN apt update && apt install -y \
		      openssh-server \
		      sudo

# appli install:

WORKDIR /usr/src/lib
COPY lib .

WORKDIR /usr/src/bin
COPY scripts/find_square .

WORKDIR /usr/src
COPY example_file .

ENV PYTHONPATH /usr/src/lib
ENV PATH $PATH:/usr/src/bin

WORKDIR /

# user setup

RUN useradd -rm -d /home/machin -s /bin/bash -g root -G sudo -u 1000 machin 

RUN  echo 'machin:machin' | chpasswd

# ssh setup

RUN service ssh start

EXPOSE 22

CMD ["/usr/sbin/sshd","-D"]

