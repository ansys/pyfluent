# Stage 1: Load the base image and execute deletions
FROM ghcr.io/ansys/fluent:v27.1.latest AS cleanup
USER root
RUN rm -rf \
    /ansys_inc/v271/commonfiles/CPython/3_13/linx64/Release/Ansys/PyFluentVisual \
    /ansys_inc/v271/commonfiles/CPython/3_13/linx64/Release/Ansys/PyFluentMcp \
    /ansys_inc/v271/commonfiles/CPython/3_13/linx64/Release/Ansys/PyTurboMeshing \
    /ansys_inc/v271/commonfiles/CPython/3_13/linx64/Release/Ansys/PyDynamicReporting \
    /ansys_inc/v271/commonfiles/CPython/3_13/linx64/Release/Ansys/PyEnsight \
    /ansys_inc/v271/commonfiles/CPython/3_13/linx64/Release/Ansys/PyGeometry \
    /ansys_inc/v271/commonfiles/CPython/3_13/linx64/Release/Ansys/PyCamClient \
    /ansys_inc/v271/commonfiles/CPython/3_13/linx64/Release/Ansys/PyCFXMcp \
    /ansys_inc/v271/commonfiles/CPython/3_13/linx64/Release/Ansys/PyFluidsMcp \
    /ansys_inc/v271/commonfiles/CPython/3_13/linx64/Release/Ansys/PyDPF \
    /ansys_inc/v271/commonfiles/CPython/3_13/linx64/Release/Ansys/lib \
    /ansys_inc/v271/commonfiles/CPython/3_13/linx64/Release/python/lib/python3.13/site-packages/PySide6 \
    /ansys_inc/v271/commonfiles/CPython/3_13/linx64/Release/python/lib/python3.13/site-packages/vtkmodules \
    /ansys_inc/v271/commonfiles/CPython/3_13/linx64/Release/python/lib/python3.13/site-packages/wx \
    /ansys_inc/v271/commonfiles/CPython/3_13/linx64/Release/python/lib/python3.13/site-packages/llvmlite \
    /ansys_inc/v271/commonfiles/CPython/3_13/linx64/Release/python/lib/python3.13/site-packages/scipy \
    /ansys_inc/v271/commonfiles/CPython/3_13/linx64/Release/python/lib/python3.13/test \
    /ansys_inc/v271/CAD \
    /ansys_inc/v271/ADR \
    /ansys_inc/v271/aisol \
    /ansys_inc/v271/Framework \
    /ansys_inc/v271/CFD-Post

# Stage 2: Build a completely empty filesystem shell
FROM scratch

# Grab the clean filesystem state. 
COPY --from=cleanup / /

LABEL description="Ansys Fluent + Meshing 2027 R1"
MAINTAINER Ben Widmann "ben.widmann@ansys.com"
ENV DISPLAY=:1
ENV QT_QPA_PLATFORM=offscreen
ENTRYPOINT [ "/entrypoint_xvfb.sh" ]
