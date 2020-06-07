# pylint: disable=no-member
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from unittest import TestCase, mock
from airflow.version import version
from airflow.providers.google.cloud.utils.secrets_client import SecretsClient
from google.api_core.exceptions import NotFound

# noinspection DuplicatedCode,PyUnresolvedReferences
class TestSecretsClient(TestCase):

    @mock.patch("airflow.providers.google.cloud.utils.secrets_client._get_scopes")
    @mock.patch("airflow.providers.google.cloud.utils.secrets_client.get_credentials_and_project_id")
    @mock.patch("airflow.providers.google.cloud.utils.secrets_client.SecretManagerServiceClient")
    @mock.patch("airflow.providers.google.cloud.utils.secrets_client.ClientInfo")
    def test_auth(self, mock_client_info, mock_secrets_client, mock_get_credentials, mock_get_scopes):
        mock_client = mock.MagicMock()
        mock_client_info_mock = mock.MagicMock()
        mock_client_info.return_value = mock_client_info_mock
        mock_secrets_client.return_value = mock_client
        mock_get_scopes.return_value = ['scope1', 'scope2']
        mock_get_credentials.return_value = ("credentials", "project_id")
        secrets_client = SecretsClient(gcp_key_path="path.json", gcp_scopes="scope1,scope2")
        _ = secrets_client.client
        mock_client_info.assert_called_with(
            client_library_version='airflow_v' + version
        )
        mock_secrets_client.assert_called_with(
            credentials='credentials',
            client_info=mock_client_info_mock
        )
        mock_get_scopes.assert_called_with("scope1,scope2")
        mock_get_credentials.assert_called_with(
            key_path="path.json",
            keyfile_dict=None,
            scopes=['scope1', 'scope2']
        )

    @mock.patch("airflow.providers.google.cloud.utils.secrets_client._get_scopes")
    @mock.patch("airflow.providers.google.cloud.utils.secrets_client.get_credentials_and_project_id")
    @mock.patch("airflow.providers.google.cloud.utils.secrets_client.SecretManagerServiceClient")
    @mock.patch("airflow.providers.google.cloud.utils.secrets_client.ClientInfo")
    def test_auth_dict(self, mock_client_info, mock_secrets_client, mock_get_credentials, mock_get_scopes):
        mock_client = mock.MagicMock()
        mock_client_info_mock = mock.MagicMock()
        mock_client_info.return_value = mock_client_info_mock
        mock_secrets_client.return_value = mock_client
        mock_get_scopes.return_value = ['scope1', 'scope2']
        mock_get_credentials.return_value = ("credentials", "project_id")
        secrets_client = SecretsClient(gcp_keyfile_dict={"key": "value"}, gcp_scopes="scope1,scope2")
        _ = secrets_client.client
        mock_client_info.assert_called_with(
            client_library_version='airflow_v' + version
        )
        mock_secrets_client.assert_called_with(
            credentials='credentials',
            client_info=mock_client_info_mock
        )
        mock_get_scopes.assert_called_with("scope1,scope2")
        mock_get_credentials.assert_called_with(
            key_path=None,
            keyfile_dict={"key": "value"},
            scopes=['scope1', 'scope2']
        )

    @mock.patch("airflow.providers.google.cloud.utils.secrets_client")
    def test_get_non_existing_key(self, mock_secrets_client):
        mock_client = mock.MagicMock()
        mock_secrets_client.SecretManagerServiceClient.return_value = mock_client
        # Response does not contain the requested key
        mock_client.secrets.kv.v2.read_secret_version.side_effect = NotFound()
        secrets_client = SecretsClient(gcp_keyfile_dict={"key": "value"}, gcp_scopes="scope1,scope2")
        secret = secrets_client.get_secret(secret_path="missing")
        self.assertIsNone(secret)
        mock_client.secrets.kv.v2.read_secret_version.assert_called_once_with(
            mount_point='secret', path='missing', version=None)

    @mock.patch("airflow.providers.hashicorp.common.vault_client.hvac")
    def test_get_existing_key(self, mock_hvac):
        mock_client = mock.MagicMock()
        mock_hvac.Client.return_value = mock_client

        mock_client.secrets.kv.v2.read_secret_version.return_value = {
            'request_id': '94011e25-f8dc-ec29-221b-1f9c1d9ad2ae',
            'lease_id': '',
            'renewable': False,
            'lease_duration': 0,
            'data': {
                'data': {'secret_key': 'secret_value'},
                'metadata': {'created_time': '2020-03-16T21:01:43.331126Z',
                             'deletion_time': '',
                             'destroyed': False,
                             'version': 1}},
            'wrap_info': None,
            'warnings': None,
            'auth': None
        }

        vault_client = VaultClient(
            auth_type="radius",
            radius_host="radhost",
            radius_port=8110,
            radius_secret="pass",
            url="http://localhost:8180")
        secret = vault_client.get_secret(secret_path="missing")
        self.assertEqual({'secret_key': 'secret_value'}, secret)
        mock_client.secrets.kv.v2.read_secret_version.assert_called_once_with(
            mount_point='secret', path='missing', version=None)

    @mock.patch("airflow.providers.hashicorp.common.vault_client.hvac")
    def test_get_existing_key_v1_version(self, mock_hvac):
        mock_client = mock.MagicMock()
        mock_hvac.Client.return_value = mock_client
        vault_client = VaultClient(auth_type="token", token="s.7AU0I51yv1Q1lxOIg1F3ZRAS",
                                   url="http://localhost:8180", kv_engine_version=1)
        with self.assertRaisesRegex(VaultError, "Secret version"):
            vault_client.get_secret(secret_path="missing", secret_version=1)

    @mock.patch("airflow.providers.hashicorp.common.vault_client.hvac")
    def test_get_secret_metadata_v2(self, mock_hvac):
        mock_client = mock.MagicMock()
        mock_hvac.Client.return_value = mock_client
        mock_client.secrets.kv.v2.read_secret_metadata.return_value = {
            'request_id': '94011e25-f8dc-ec29-221b-1f9c1d9ad2ae',
            'lease_id': '',
            'renewable': False,
            'lease_duration': 0,
            'metadata': [
                {'created_time': '2020-03-16T21:01:43.331126Z',
                 'deletion_time': '',
                 'destroyed': False,
                 'version': 1},
                {'created_time': '2020-03-16T21:01:43.331126Z',
                 'deletion_time': '',
                 'destroyed': False,
                 'version': 2},
            ]
        }
        vault_client = VaultClient(auth_type="token", token="s.7AU0I51yv1Q1lxOIg1F3ZRAS",
                                   url="http://localhost:8180")
        metadata = vault_client.get_secret_metadata(secret_path="missing")
        self.assertEqual(
            {
                'request_id': '94011e25-f8dc-ec29-221b-1f9c1d9ad2ae',
                'lease_id': '',
                'renewable': False,
                'lease_duration': 0,
                'metadata': [
                    {'created_time': '2020-03-16T21:01:43.331126Z',
                     'deletion_time': '',
                     'destroyed': False,
                     'version': 1},
                    {'created_time': '2020-03-16T21:01:43.331126Z',
                     'deletion_time': '',
                     'destroyed': False,
                     'version': 2},
                ]
            }, metadata)
        mock_client.secrets.kv.v2.read_secret_metadata.assert_called_once_with(
            mount_point='secret', path='missing')

    @mock.patch("airflow.providers.hashicorp.common.vault_client.hvac")
    def test_get_secret_including_metadata_v2(self, mock_hvac):
        mock_client = mock.MagicMock()
        mock_hvac.Client.return_value = mock_client

        mock_client.secrets.kv.v2.read_secret_version.return_value = {
            'request_id': '94011e25-f8dc-ec29-221b-1f9c1d9ad2ae',
            'lease_id': '',
            'renewable': False,
            'lease_duration': 0,
            'data': {
                'data': {'secret_key': 'secret_value'},
                'metadata': {'created_time': '2020-03-16T21:01:43.331126Z',
                             'deletion_time': '',
                             'destroyed': False,
                             'version': 1}},
            'wrap_info': None,
            'warnings': None,
            'auth': None
        }
        vault_client = VaultClient(
            auth_type="radius",
            radius_host="radhost",
            radius_port=8110,
            radius_secret="pass",
            url="http://localhost:8180")
        metadata = vault_client.get_secret_including_metadata(secret_path="missing")
        self.assertEqual(
            {
                'request_id': '94011e25-f8dc-ec29-221b-1f9c1d9ad2ae',
                'lease_id': '',
                'renewable': False,
                'lease_duration': 0,
                'data': {
                    'data': {'secret_key': 'secret_value'},
                    'metadata': {'created_time': '2020-03-16T21:01:43.331126Z',
                                 'deletion_time': '',
                                 'destroyed': False,
                                 'version': 1}},
                'wrap_info': None,
                'warnings': None,
                'auth': None
            }, metadata)
        mock_client.secrets.kv.v2.read_secret_version.assert_called_once_with(
            mount_point='secret', path='missing', version=None)

    @mock.patch("airflow.providers.hashicorp.common.vault_client.hvac")
    def test_create_or_update_secret_v2(self, mock_hvac):
        mock_client = mock.MagicMock()
        mock_hvac.Client.return_value = mock_client

        vault_client = VaultClient(
            auth_type="radius",
            radius_host="radhost",
            radius_port=8110,
            radius_secret="pass",
            url="http://localhost:8180")
        vault_client.create_or_update_secret(
            secret_path="path",
            secret={'key': 'value'}
        )
        mock_client.secrets.kv.v2.create_or_update_secret.assert_called_once_with(
            mount_point='secret', secret_path='path', secret={'key': 'value'}, cas=None)

