ARG baseImage=centos:7
FROM ${baseImage} as fluentbuilder
COPY fluent.tgz /ansys_inc/
RUN tar -xzf /ansys_inc/fluent.tgz --directory /ansys_inc/ && rm -f /ansys_inc/fluent.tgz

FROM ${baseImage} as ceibuilder
COPY cei.tgz /ansys_inc/
RUN tar -xzf /ansys_inc/cei.tgz --directory /ansys_inc/ && rm -f /ansys_inc/cei.tgz

FROM ${baseImage}
LABEL description="Ansys Fluent 2022 R2"
MAINTAINER Laurence Janoo "laurence.janoo@ansys.com"
RUN yum install -y \
        tcsh.x86_64 \
        libXrandr.x86_64 \
        libXinerama.x86_64 \
        libXcursor.x86_64 \
        mesa-libGLU-9.0.0-4.el7.x86_64 \
        libglvnd-glx-1.0.1-0.8.git5baa1e5.el7.x86_64 \
        libglvnd-1.0.1-0.8.git5baa1e5.el7.x86_64  && yum clean all
COPY --from=fluentbuilder /ansys_inc /ansys_inc/
COPY --from=ceibuilder /ansys_inc /ansys_inc/
ENTRYPOINT ["/ansys_inc/v222/fluent/bin/fluent"]
