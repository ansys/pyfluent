ARG baseImage=rockylinux/rockylinux:8.10

FROM ${baseImage}
LABEL description="Ansys Fluent 2026 R1"
MAINTAINER Ben Widmann "ben.widmann@ansys.com"
RUN yum install -y \
    findutils \
    tcsh.x86_64 \
    fontconfig.x86_64 \
    libXi.x86_64 \
    libSM.x86_64 \
    libICE.x86_64 \
    libXrandr.x86_64 \
    libXinerama.x86_64 \
    libXcursor.x86_64 \
    nss-3.90.0-7.el8_10.x86_64 \
    mesa-libGLU-9.0.0-15.el8.x86_64 \
    libglvnd-glx-1.3.4-2.el8.x86_64 \
    libtirpc-devel \
    glx-utils-8.4.0-5.20181118git1830dcb.el8.x86_64 \
    && yum clean all
RUN dnf install --enablerepo=powertools -y \
    libnsl2-devel \
    bison-devel \
    flex-devel \
    libglvnd-opengl \
    nss-softokn \
    libGLEW-2.0.0-6.el8.x86_64   
RUN dnf install --enablerepo=devel -y \
    libXcomposite
RUN dnf install -y \
    libXdamage \
    libXtst \
    libnsl

RUN dnf install -y \
    xorg-x11-server-Xvfb \
    xrandr \
    mesa-dri-drivers \
    && dnf clean all
ENV DISPLAY=:1
ENV QT_QPA_PLATFORM=offscreen

COPY ansys_inc /ansys_inc/

COPY entrypoint_xvfb.sh /entrypoint_xvfb.sh
RUN chmod a+x /entrypoint_xvfb.sh

ARG USERNAME=fluentuser
ARG USER_UID=10000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME && \
    chown -R $USER_UID:$USER_GID /home/$USERNAME

ENTRYPOINT [ "/entrypoint_xvfb.sh" ]
