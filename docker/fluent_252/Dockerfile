# Specify base image
FROM ubuntu:20.04

# User variables
ARG USERNAME=fluent
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

# Copy ``ansys_inc`` directory
COPY ansys_inc /ansys_inc

# Add metadata
LABEL description="Ansys Fluent 2025 R2"
LABEL email="pyansys.core@ansys.com"

# OCI label
LABEL org.opencontainers.image.documentation="https://fluent.docs.pyansys.com"

# Install dependencies
RUN apt-get -y update && apt-get -y install \
    csh \
    fontconfig \
    libxi-dev \
    libsm6 \
    libice-dev \
    libxrandr-dev \
    libxinerama-dev \
    libxcursor-dev \
    libglu1-mesa \
    libglvnd-dev \
    libnspr4 \
    libnss3-tools \
    libnss3 \
    libtirpc3 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrender1 \
    libx11-6 \
    libxext6 \
    libxtst6 \
    libdbus-1-3 && apt-get clean all

RUN printf '/usr/lib/x86_64-linux-gnu/nss\n' > /etc/ld.so.conf.d/nss.conf && ldconfig
ENV LD_LIBRARY_PATH="/usr/lib/x86_64-linux-gnu/nss:${LD_LIBRARY_PATH}"

# Specify working directory
ARG WORK_DIR=fluent_work_dir
ENV WORKING_DIRECTORY=/home/$USERNAME/$WORK_DIR

# Specify home directory
ENV HOME=/home/$USERNAME

# Add a working directory and make it accessible to any user
RUN mkdir -p $WORKING_DIRECTORY \
    && \
    chown -R $USERNAME:$USERNAME $WORKING_DIRECTORY \
    && \
    chmod a+rwx $WORKING_DIRECTORY

# Set the user
USER $USERNAME

# Set working directory
WORKDIR /home/$USERNAME/$WORKING_DIRECTORY

# Specify default Fluent executable
ENTRYPOINT ["/ansys_inc/v252/fluent/bin/fluent"]
