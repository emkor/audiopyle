FROM endlessdrones/audiopyle-base-image:latest

# SETTING GLOBAL ENV FOR FURTHER USE
ENV AUDIOPYLE_HOME "/audiopyle"

# CREATING DIR FOR THIS MODULE
RUN mkdir -p "$AUDIOPYLE_HOME/commons"

# CURRENT OPS WILL BE CALLED HERE
WORKDIR "$AUDIOPYLE_HOME/commons"

# COPY MODULE FILES
COPY ./commons ./commons
COPY ./requirements.txt ./requirements.txt
COPY ./setup.py ./setup.py

# DEPLOY
COPY ./deploy.sh ./deploy.sh
RUN chmod -R 775 ./deploy.sh
RUN bash ./deploy.sh

# INSTALL TEST FRAMEWORK AND RUN TESTS
RUN pip install tox
COPY ./tox.ini ./tox.ini
RUN tox

# CLEANUP AFTER TESTS
RUN rm -rf .tox && rm -rf audiopyle_commons.egg-info
RUN pip uninstall -y tox