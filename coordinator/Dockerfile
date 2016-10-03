FROM endlessdrones/audiopyle-commons:latest

# CREATING DIR FOR THIS MODULE
RUN mkdir -p "$AUDIOPYLE_HOME/coordinator"

# CURRENT OPS WILL BE CALLED HERE
WORKDIR "$AUDIOPYLE_HOME/coordinator"
#
# COPY MODULE FILES
COPY ./coordinator ./coordinator
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
RUN rm -rf .tox && rm -rf audiopyle_coordinator.egg-info
RUN pip uninstall -y tox

# SET STARTUP SCRIPT AS ENTRYPOINT
COPY ./start_coordinator.py ./start_coordinator.py
ENTRYPOINT ["python", "-u", "./start_coordinator.py"]
