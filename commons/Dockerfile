FROM python:2.7.11-wheezy

# SETTING GLOBAL ENV FOR FURTHER USE
ENV AUDIOPYLE_HOME "/audiopyle"

# CREATING DIR FOR THIS MODULE
RUN mkdir -p "$AUDIOPYLE_HOME/commons"

# CURRENT OPS WILL BE CALLED HERE
WORKDIR "$AUDIOPYLE_HOME/commons"

# COPY MODULE FILES
ADD ./commons ./commons
ADD ./requirements.txt ./requirements.txt
ADD ./setup.py ./setup.py

# DEPLOY
ADD ./deploy.sh ./deploy.sh
RUN chmod -R 775 ./deploy.sh
RUN bash ./deploy.sh

# INSTALL TEST FRAMEWORK AND RUN TESTS
RUN pip install tox
ADD ./tox.ini ./tox.ini
RUN tox
