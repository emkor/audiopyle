FROM endlessdrones/audiopyle-commons:latest

# CREATING DIR FOR THIS MODULE
RUN mkdir -p "$AUDIOPYLE_HOME/persister"

# CURRENT OPS WILL BE CALLED HERE
WORKDIR "$AUDIOPYLE_HOME/persister"
#
# COPY MODULE FILES
COPY ./persister ./persister
COPY ./requirements.txt ./requirements.txt
COPY ./setup.py ./setup.py

# INSTALL TEST FRAMEWORK AND RUN TESTS
RUN pip install tox
COPY ./tox.ini ./tox.ini
RUN tox

# CLEANUP AFTER TESTS
RUN rm -rf .tox && rm -rf audiopyle_coordinator.egg-info
RUN pip uninstall -y tox