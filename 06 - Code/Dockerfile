FROM buildpack-deps:jessie

# remove several traces of debian python
RUN apt-get purge -y python.*

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

# ENV PYPY_VERSION 2.4.0

RUN set -x \
	&& curl -SL "https://bitbucket.org/pypy/pypy/downloads/pypy2-v5.4.1-linux64.tar.bz2" \
		| tar -xjC /usr/local --strip-components=1 \
	&& curl -SL 'https://bootstrap.pypa.io/get-pip.py' | pypy
RUN apt-get update
RUN apt-get install -y libsasl2-dev python3-dev libldap2-dev libssl-dev
RUN pip install \
falcon==0.3.0 \
gunicorn==19.4.5 \
falcon-cors==1.0.1 \
requests==2.10.0 \	
grequests==0.3.0 \
redis==2.10.5 \
pyuca==1.1.2 \
beautifulsoup4==4.6.0

WORKDIR /usr/src/myapp
CMD ["gunicorn",  "app:api", "-b :5005", "-t 120"]
