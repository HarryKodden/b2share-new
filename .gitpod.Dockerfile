FROM gitpod/workspace-full

ENV PYTHON_VER=3.7.3

RUN pyenv install ${PYTHON_VER}
RUN pyenv global ${PYTHON_VER}
ENV PIP_USER=no

