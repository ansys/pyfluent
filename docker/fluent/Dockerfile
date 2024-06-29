# Specify base image
FROM centos:7

# User variables
ARG USERNAME=fluent
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

# Copy ansys_inc
COPY ansys_inc /ansys_inc

# Add metadata
LABEL description="Ansys Fluent 2025 R1"
LABEL email="pyansys.core@ansys.com"

# OCI label
LABEL org.opencontainers.image.documentation="https://fluent.docs.pyansys.com"

# Install dependencies
RUN yum install -y \
        tcsh.x86_64 \
        fontconfig.x86_64 \
        libXi.x86_64 \
        libSM.x86_64 \
        libICE.x86_64 \
        libXrandr.x86_64 \
        libXinerama.x86_64 \
        libXcursor.x86_64 \
        mesa-libGLU.x86_64 \
        libglvnd-glx.x86_64 \
        libglvnd.x86_64  && yum clean all

# Set user
USER $USERNAME

# Specify default Fluent executable
ENTRYPOINT ["/ansys_inc/v251/fluent/bin/fluent"]
