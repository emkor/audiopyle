FROM python:3.5-slim

MAINTAINER mkorzeniowski93@gmail.com
LABEL version="0.6"
LABEL description="Latest Python Alpine image with numpy and vamp"

# install_os_deps
RUN apt-get update
RUN apt-get install -y wget build-essential zlib1g-dev libssl-dev libffi-dev libmysqlclient-dev gcc ffmpeg libavcodec-extra-53

# install numpy and vamp
RUN pip install numpy
RUN pip install vamp

CMD ["/bin/bash"]