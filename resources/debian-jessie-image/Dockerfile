FROM debian:jessie

RUN apt-get update
RUN apt-get install -y wget build-essential libsqlite3-dev zlib1g-dev libncurses5-dev libgdbm-dev libbz2-dev libreadline-gplv2-dev libssl-dev libdb-dev

RUN wget "https://www.python.org/ftp/python/2.7.11/Python-2.7.11.tgz" && tar -xzf "Python-2.7.11.tgz"
RUN cd "/Python-2.7.11" && bash ./configure --enable-shared && make && make install && cd ..

RUN echo "export LD_LIBRARY_PATH=/usr/local/lib" >> /root/.profile
ENV LD_LIBRARY_PATH /usr/local/lib

RUN wget "https://bootstrap.pypa.io/get-pip.py" && python get-pip.py
RUN wget http://peak.telecommunity.com/dist/ez_setup.py && python ez_setup.py

RUN rm -rf "/Python-2.7.11" && rm -rf "/Python-2.7.11"
RUN rm -rf "Python-2.7.11.tgz" && rm -rf "Python-2.7.11.tgz"