# our base image
FROM centos:7

LABEL description="Linux Fluent"
MAINTAINER FBU Fluent DevOps "fbu-fluent-buildteam@ansys.com"

RUN yum install -y \
        mesa-libGLU-9.0.0-4.el7.x86_64 \
        libglvnd-glx-1.0.1-0.8.git5baa1e5.el7.x86_64 \
        libglvnd-1.0.1-0.8.git5baa1e5.el7.x86_64  && yum clean all
COPY lnamd64.tgz /ansys_inc/
RUN tar -xzf /ansys_inc/lnamd64.tgz --strip-components=2 --directory /ansys_inc/ && rm -f /ansys_inc/lnamd64.tgz
