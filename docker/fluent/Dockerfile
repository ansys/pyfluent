# Specify base image
FROM centos:7

# Copy Fluent archive
COPY ansys_inc.tgz .

# Extract ansys_inc
RUN tar -xzvf ansys_inc.tgz ansys_inc

# Remove ansys_inc.tgz
RUN rm -f ansys_inc.tgz

# Add description metadata
LABEL description="Ansys Fluent 2025 R1"

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
        mesa-libGLU-9.0.0-4.el7.x86_64 \
        libglvnd-glx-1.0.1-0.8.git5baa1e5.el7.x86_64 \
        libglvnd-1.0.1-0.8.git5baa1e5.el7.x86_64  && yum clean all

# Specify default Fluent executable
ENTRYPOINT ["/ansys_inc/v251/fluent/bin/fluent"]
