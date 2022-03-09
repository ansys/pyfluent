ARG baseImage=centos:7
FROM ${baseImage} as builder
COPY lnamd64.tgz /ansys_inc/
RUN tar -xzf /ansys_inc/lnamd64.tgz --strip-components=2 --directory /ansys_inc/ && rm -f /ansys_inc/lnamd64.tgz

FROM ${baseImage}
LABEL description="Ansys Fluent 2022 R2"
MAINTAINER Laurence Janoo "laurence.janoo@ansys.com"
RUN yum install -y \
        mesa-libGLU-9.0.0-4.el7.x86_64 \
        libglvnd-glx-1.0.1-0.8.git5baa1e5.el7.x86_64 \
        libglvnd-1.0.1-0.8.git5baa1e5.el7.x86_64  && yum clean all
COPY --from=builder /ansys_inc /ansys_inc/
ENTRYPOINT ["/ansys_inc/v222/fluent/bin/fluent"]
