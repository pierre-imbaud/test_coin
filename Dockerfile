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


# user setup

RUN useradd -rm -d /home/machin -s /bin/bash -g root -G sudo -u 1000 machin 

RUN  echo 'machin:machin' | chpasswd

WORKDIR /home/machin

# these wont work, even to .bashrc or .bash_profile: probably settable thru sshd_config...
# Please set these from ssh command

# RUN echo PATH=$PATH:/usr/src/bin > .profile
# RUN echo export PYTHONPATH=/usr/src/lib >> .profile

COPY example_file .


# ssh setup

RUN service ssh start

EXPOSE 22

CMD ["/usr/sbin/sshd","-D"]

