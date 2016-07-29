FROM endlessdrones/audiopyle-commons:latest

# CREATING DIR FOR THIS MODULE
RUN mkdir -p "$AUDIOPYLE_HOME/coordinator"

# CURRENT OPS WILL BE CALLED HERE
WORKDIR "$AUDIOPYLE_HOME/coordinator"
#
# COPY MODULE FILES
ADD ./coordinator ./coordinator
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

# CLEANUP AFTER TESTS
RUN rm -rf .tox && rm -rf audiopyle_coordinator.egg-info
RUN pip uninstall -y tox