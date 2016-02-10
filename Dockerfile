FROM debian:jessie
MAINTAINER andrew@ei-grad.ru
EXPOSE 8000

RUN (echo "deb http://ppa.launchpad.net/no1wantdthisname/ppa/ubuntu trusty main"; \
     echo "deb-src http://ppa.launchpad.net/no1wantdthisname/ppa/ubuntu trusty main") \
    >> /etc/apt/sources.list.d/infinality.list && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E985B27B && \
    sed -i 's/main$/main non-free contrib/g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y wget python xvfb \
                       fontconfig-infinality \
                       iceweasel chromium \
                       ttf-dejavu \
                       ttf-mscorefonts-installer && \
    /etc/fonts/infinality/infctl.sh setstyle osx && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/*

RUN wget -O - https://bootstrap.pypa.io/get-pip.py | python

WORKDIR /usr/src/app/

RUN useradd -m app
VOLUME /home/app

CMD ["/usr/src/app/entrypoint.sh"]

ADD requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

USER app

ADD . /usr/src/app/
