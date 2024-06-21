# Specify base image variable
ARG baseImage=rockylinux

# Create a build stage for Fluent from base image
FROM ${baseImage} as fluentbuilder

# Copy Fluent archive
COPY fluent.tgz /ansys_inc/

# Extract Fluent archive to ansys_inc and remove Fluent archive
RUN tar -xzf /ansys_inc/fluent.tgz --directory /ansys_inc/ && rm -f /ansys_inc/fluent.tgz

# Create a build stage for CEI from base image
FROM ${baseImage} as ceibuilder

# Copy CEI archive
COPY cei.tgz /ansys_inc/

# Extract CEI archive to ansys_inc and remove CEI archive
RUN tar -xzf /ansys_inc/cei.tgz --directory /ansys_inc/ && rm -f /ansys_inc/cei.tgz

# Create a build stage for CFD-Post from base image
FROM ${baseImage} as cfdpostbuilder

# Copy CFD-Post archive
COPY cfdpost.tgz /ansys_inc/

# Extract CFD-Post archive to ansys_inc and remove CFD-Post archive
RUN tar -xzf /ansys_inc/cfdpost.tgz --directory /ansys_inc/ && rm -f /ansys_inc/cfdpost.tgz

# Base image
FROM ${baseImage}

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

# Copy Fluent files to ansys_inc directory
COPY --from=fluentbuilder /ansys_inc /ansys_inc/

# Copy CEI files to ansys_inc directory
COPY --from=ceibuilder /ansys_inc /ansys_inc/

# Copy CFD-Post files to ansys_inc directory
COPY --from=cfdpostbuilder /ansys_inc /ansys_inc/

# Specify default Fluent executable
ENTRYPOINT ["/ansys_inc/v251/fluent/bin/fluent"]
