FROM endlessdrones/audiopyle-commons:tests-audio-converter

# CREATING DIR FOR THIS MODULE
RUN mkdir -p "$AUDIOPYLE_HOME/xtracter"

# CURRENT OPS WILL BE CALLED HERE
WORKDIR "$AUDIOPYLE_HOME/xtracter"

RUN dpkg -l libc6

# COPY MODULE FILES
ADD ./xtracter ./xtracter
ADD ./devops ./devops
ADD ./requirements.txt ./requirements.txt
ADD ./setup.py ./setup.py

# DEPLOY
ADD ./deploy.sh ./deploy.sh
RUN chmod -R 775 ./deploy.sh
RUN bash ./deploy.sh
ENV VAMP_PATH "$AUDIOPYLE_HOME/xtracter/resources/vamp_plugins"

# INSTALL TEST FRAMEWORK AND RUN TESTS
RUN pip install tox
ADD ./tox.ini ./tox.ini
RUN tox
