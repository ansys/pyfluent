"""Error and warning messages for Fluent launcher and connection modules."""

ALLOW_REMOTE_HOST_NOT_PROVIDED_IN_REMOTE = (
    "Connecting to remote Fluent instances is not allowed. "
    "Set 'allow_remote_host=True' to connect to remote hosts."
)

ALLOW_REMOTE_HOST_NOT_PROVIDED_WITH_CERTIFICATES_FOLDER = (
    "To set `certificates_folder`, `allow_remote_host` must be True."
)

ALLOW_REMOTE_HOST_NOT_PROVIDED_WITH_INSECURE_MODE = (
    "To set `insecure_mode`, `allow_remote_host` must be True."
)

CERTIFICATES_FOLDER_NOT_PROVIDED_AT_LAUNCH = "To launch Fluent in remote mode, set `certificates_folder` containing TLS certificates."

CERTIFICATES_FOLDER_NOT_PROVIDED_AT_CONNECT = "To connect to a remote Fluent instance, set `certificates_folder` containing TLS certificates."

CERTIFICATES_FOLDER_PROVIDED_IN_STANDALONE = (
    "``certificates_folder`` is relevant only when launching or connecting to a remote Fluent instance and "
    "will be ignored for standalone launch mode."
)

INSECURE_MODE_PROVIDED_IN_STANDALONE = (
    "``insecure_mode`` is relevant only when launching or connecting to a remote Fluent instance and "
    "will be ignored for standalone launch mode."
)

BOTH_CERTIFICATES_FOLDER_AND_INSECURE_MODE_PROVIDED = (
    "`certificates_folder` and `insecure_mode` cannot be set at the same time."
)

CONNECTING_TO_LOCALHOST_INSECURE_MODE = (
    "Insecure gRPC mode is not allowed when connecting to localhost."
)

INSECURE_MODE_WARNING = (
    "The Fluent session will be connected in insecure gRPC mode. "
    "This mode is not recommended. For more details on the implications "
    "and usage of insecure mode, refer to the Fluent documentation."
)
