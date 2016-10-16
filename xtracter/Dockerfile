FROM endlessdrones/audiopyle-commons:latest

# CREATING DIR FOR THIS MODULE
RUN mkdir -p "$AUDIOPYLE_HOME/xtracter"

# CURRENT OPS WILL BE CALLED HERE
WORKDIR "$AUDIOPYLE_HOME/xtracter"

# COPY MODULE FILES
COPY ./xtracter ./xtracter
COPY ./devops ./devops
COPY ./requirements.txt ./requirements.txt
COPY ./setup.py ./setup.py

# DEPLOY
COPY ./deploy.sh ./deploy.sh
RUN chmod -R 775 ./deploy.sh
RUN bash ./deploy.sh
ENV VAMP_PATH "$AUDIOPYLE_HOME/xtracter/resources/vamp_plugins"

# INSTALL TEST FRAMEWORK AND RUN TESTS
RUN pip install tox
COPY ./tox.ini ./tox.ini
RUN tox

# CLEANUP AFTER TESTS
RUN rm -rf .tox && rm -rf audiopyle_xtracter.egg-info
RUN pip uninstall -y tox

# SET STARTUP SCRIPT AS ENTRYPOINT
COPY ./start_xtracter.py ./start_xtracter.py
ENTRYPOINT ["python", "-u", "./start_xtracter.py"]