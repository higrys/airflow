import re
from typing import Optional

from cached_property import cached_property
from google.api_core.exceptions import NotFound
from google.api_core.gapic_v1.client_info import ClientInfo
from google.cloud.secretmanager_v1 import SecretManagerServiceClient

from airflow.providers.google.cloud.utils.credentials_provider import (
    _get_scopes, get_credentials_and_project_id,
)
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.version import version

SECRET_ID_PATTERN = r"^[a-zA-Z0-9-_]*$"


class SecretsClient(LoggingMixin):

    """
    Retrieves Secrets object from GCP Secrets Manager

    :param gcp_key_path: Path to GCP Credential JSON file. Mutually exclusive with gcp_keyfile_dict.
        use default credentials in the current environment if not provided.
    :type gcp_key_path: str
    :param gcp_keyfile_dict: Dictionary of keyfile parameters. Mutually exclusive with gcp_key_path.
    :type gcp_keyfile_dict: dict
    :param gcp_scopes: Comma-separated string containing GCP scopes
    :type gcp_scopes: str
    """
    def __init__(
        self,
        gcp_key_path: Optional[str] = None,
        gcp_keyfile_dict: Optional[dict] = None,
        gcp_scopes: Optional[str] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.gcp_key_path = gcp_key_path
        self.gcp_keyfile_dict = gcp_keyfile_dict
        self.gcp_scopes = gcp_scopes
        self.credentials: Optional[str] = None
        self.project_id: Optional[str] = None

    @staticmethod
    def is_valid_secret_name(secret_name: str) -> bool:
        """
        Returns true if the secret name is valid.
        :param secret_name: name of the secret
        :type secret_name: str
        :return:
        """
        return bool(re.match(SECRET_ID_PATTERN, secret_name))

    @cached_property
    def client(self) -> SecretManagerServiceClient:
        """
        Create an authenticated KMS client
        """
        scopes = _get_scopes(self.gcp_scopes)
        self.credentials, self.project_id = get_credentials_and_project_id(
            keyfile_dict=self.gcp_keyfile_dict,
            key_path=self.gcp_key_path,
            scopes=scopes
        )
        _client = SecretManagerServiceClient(
            credentials=self.credentials,
            client_info=ClientInfo(client_library_version='airflow_v' + version)
        )
        return _client

    def get_secret(self, secret_id: str, secret_version: str = 'latest') -> Optional[str]:
        """
        Get secret value from the Secret Manager.

        :param secret_id: Secret Key
        :type secret_id: str
        :param secret_version: version of the secret (default is 'latest')
        :type secret_version: str
        """
        name = self.client.secret_version_path(self.project_id, secret_id, secret_version)
        try:
            response = self.client.access_secret_version(name)
            value = response.payload.data.decode('UTF-8')
            return value
        except NotFound:
            self.log.error(
                "GCP API Call Error (NotFound): Secret ID %s not found.", secret_id
            )
            return None
