#!/bin/sh

# Image name
SHA='sha256'
SUBSTRING=$(echo ${FLUENT_IMAGE_TAG}| cut -c 1-6)
if [ "$SUBSTRING" == "$SHA" ]
then
  _IMAGE_NAME="ghcr.io/ansys/pyfluent@${FLUENT_IMAGE_TAG}"
else
  _IMAGE_NAME="ghcr.io/ansys/pyfluent:${FLUENT_IMAGE_TAG:-latest}"
fi

# Pull fluent image based on tag
docker pull ghcr.io/ansys/fluent:v26.1.68

# Remove all dangling images
docker image prune -f
