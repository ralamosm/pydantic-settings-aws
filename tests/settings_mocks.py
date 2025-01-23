import json
from typing import List, Optional

from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict
from typing_extensions import Annotated

from pydantic_settings_aws import (
    AWSBaseSettings,
    ParameterStoreBaseSettings,
    SecretsManagerBaseSettings,
    SingleParameterStoreBaseSettings,
)

from .boto3_mocks import ClientMock

dict_secrets_with_username_and_password = {
    "username": "myusername",
    "password": "password1234",
    "name": None,
}

secrets_with_username_and_password = json.dumps(
    dict_secrets_with_username_and_password
)

mock_secrets_with_username_and_pwd = ClientMock(
    secret_string=secrets_with_username_and_password
)


class MySecretsWithClientConfig(SecretsManagerBaseSettings):
    model_config = SettingsConfigDict(
        secrets_name="my/secret",
        secrets_client=mock_secrets_with_username_and_pwd,
    )

    username: str
    password: str
    name: Optional[str] = None


secrets_with_nested_content = json.dumps(
    {
        "username": "myusername",
        "password": "password1234",
        "nested": {"roles": ["user", "admin"]},
    }
)

mock_secrets_with_nested_content = ClientMock(
    secret_string=secrets_with_nested_content
)


class NestedContent(BaseModel):
    roles: List[str]


class SecretsWithNestedContent(SecretsManagerBaseSettings):
    model_config = SettingsConfigDict(
        secrets_name="my/secret",
        secrets_client=mock_secrets_with_nested_content,
    )

    username: str
    password: str
    nested: NestedContent


class ParameterSettings(ParameterStoreBaseSettings):
    my_ssm: Annotated[
        str,
        {"ssm": "my/parameter", "ssm_client": ClientMock(ssm_value="value")},
    ]


class ParameterWithTwoSSMClientSettings(ParameterStoreBaseSettings):
    model_config = SettingsConfigDict(ssm_client=ClientMock(ssm_value="value"))

    my_ssm: Annotated[
        str,
        {"ssm": "my/parameter", "ssm_client": ClientMock(ssm_value="value")},
    ]
    my_ssm_1: Annotated[
        str,
        {"ssm": "my/parameter", "ssm_client": ClientMock(ssm_value="value1")},
    ]
    my_ssm_2: Annotated[str, "my/ssm/2/parameter"]


class ParameterWithOptionalValueSettings(ParameterStoreBaseSettings):
    model_config = SettingsConfigDict(ssm_client=ClientMock())

    my_ssm: Annotated[Optional[str], "my/ssm/2/parameter"] = None


class AWSWithParameterAndSecretsWithDefaultBoto3Client(AWSBaseSettings):
    model_config = SettingsConfigDict(
        ssm_client=ClientMock(ssm_value="value"),
        secrets_client=mock_secrets_with_username_and_pwd,
        secrets_name="my/secret",
    )

    username: Annotated[str, {"service": "secrets"}]
    password: Annotated[str, {"service": "secrets"}]
    host: Annotated[str, {"service": "ssm"}]


class AWSWithParameterSecretsAndEnvironmentWithDefaultBoto3Client(AWSBaseSettings):
    model_config = SettingsConfigDict(
        ssm_client=ClientMock(ssm_value="value"),
        secrets_client=mock_secrets_with_username_and_pwd,
        secrets_name="my/secret",
    )

    username: Annotated[str, {"service": "secrets"}]
    password: Annotated[str, {"service": "secrets"}]
    host: Annotated[str, {"service": "ssm"}]
    server_name: str


class AWSWithUnknownService(AWSBaseSettings):
    my_name: Annotated[Optional[str], {"service": "s3"}] = None


class AWSWithNonDictMetadata(AWSBaseSettings):
    my_name: Annotated[Optional[str], "my irrelevant metadata"] = None

# Mock data for single parameter store JSON content
single_parameter_json_content = json.dumps({
    "username": "json-user",
    "password": "json-pass",
    "db_name": "test-db",
    "port": 5432
})

mock_single_parameter_store = ClientMock(ssm_value=single_parameter_json_content)

class SingleParameterSettings(SingleParameterStoreBaseSettings):
    model_config = SettingsConfigDict(
        ssm_client=mock_single_parameter_store,
        ssm_parameter_name="my/json/parameter"
    )

    username: str
    password: str
    db_name: str
    port: int

# Test invalid JSON content
mock_invalid_json_parameter = ClientMock(ssm_value="invalid{json")

class SingleParameterInvalidJSONSettings(SingleParameterStoreBaseSettings):
    model_config = SettingsConfigDict(
        ssm_client=mock_invalid_json_parameter,
        ssm_parameter_name="my/json/parameter"
    )

    username: Optional[str] = None
    password: Optional[str] = None

# Test empty/none parameter
mock_empty_parameter = ClientMock(ssm_value=None)

class SingleParameterEmptySettings(SingleParameterStoreBaseSettings):
    model_config = SettingsConfigDict(
        ssm_client=mock_empty_parameter,
        ssm_parameter_name="my/json/parameter"
    )

    username: Optional[str] = None
    password: Optional[str] = None
