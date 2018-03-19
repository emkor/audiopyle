FROM endlessdrones/audiopyle-extractor

MAINTAINER mkorzeniowski93@gmail.com
LABEL version="0.1"
LABEL description="Image containing integration tests"

# CREATE AND SET DIRECTORIES
RUN mkdir -p /audiopyle/testcases
WORKDIR /audiopyle/testcases

# COPY SOURCE CODE FOR TESTCASES
COPY . .

# INSTALL AUDIOPYLE TESTCASES
RUN pip install .

ENTRYPOINT ["/audiopyle/wait-for-it.sh", "-t", "30", "coordinator:8080", "--", "python", "-m", "pytest", "-v"]
