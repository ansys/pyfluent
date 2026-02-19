"""
Pull a Fluent Docker image based on the FLUENT_IMAGE_TAG environment variable.
"""

import re
import subprocess
import time

from ansys.fluent.core import config
from ansys.fluent.core.docker.utils import get_ghcr_fluent_image_name

MAX_RETRIES = 5
BASE_DELAY = 1.0  # seconds


def pull_fluent_image():  # pylint: disable=missing-raises-doc
    """Pull Fluent Docker image and clean up dangling images."""
    fluent_image_tag = config.fluent_image_tag
    image_name = get_ghcr_fluent_image_name(fluent_image_tag)
    separator = "@" if fluent_image_tag.startswith("sha256") else ":"
    full_image_name = f"{image_name}{separator}{fluent_image_tag}"

    # Retry logic for handling rate limits (429 errors)

    for attempt in range(MAX_RETRIES):
        try:
            subprocess.run(
                ["docker", "pull", full_image_name],
                check=True,
                capture_output=True,
                text=True,
            )
            break  # Success, exit retry loop
        except subprocess.CalledProcessError as e:
            stderr_output = e.stderr.lower()

            # Check if it's a 429 rate limit error
            if "toomanyrequests" in stderr_output or "429" in stderr_output:
                if attempt < MAX_RETRIES - 1:
                    # Parse retry-after hint if available
                    retry_after = None
                    match = re.search(
                        r"retry-after:\s*([\d.]+)\s*ms", e.stderr, re.IGNORECASE
                    )
                    if match:
                        retry_after = float(match.group(1)) / 1000

                    # Use retry-after if available, otherwise exponential backoff
                    delay = retry_after if retry_after else BASE_DELAY * (2**attempt)

                    print(
                        f"Rate limit hit (429), retrying in {delay:.2f} seconds... (attempt {attempt + 1}/{MAX_RETRIES})"
                    )
                    time.sleep(delay)
                else:
                    print(
                        "Max retries reached. Failed to pull image due to rate limiting."
                    )
                    raise
            else:
                # Not a rate limit error, re-raise immediately
                raise

    subprocess.run(["docker", "image", "prune", "-f"], check=True)


if __name__ == "__main__":
    pull_fluent_image()
