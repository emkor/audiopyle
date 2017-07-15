FROM python:alpine

MAINTAINER mkorzeniowski93@gmail.com
LABEL version="0.4"
LABEL description="Latest Python Alpine image with numpy and vamp"


RUN apk add --no-cache g++ \
	&& pip install numpy \
	&& pip install vamp

CMD ["/bin/sh"]
