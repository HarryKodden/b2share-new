FROM gitpod/workspace-full

ENV PYTHON_VER=3.7.3
ENV PIP_USER=no

RUN pyenv install ${PYTHON_VER}
RUN pyenv local ${PYTHON_VER}

