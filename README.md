# Pydantic Settings AWS

[![CI](https://github.com/ceb10n/pydantic-settings-aws/actions/workflows/ci.yml/badge.svg)](https://github.com/ceb10n/pydantic-settings-aws/actions)
[![codecov](https://codecov.io/github/ceb10n/pydantic-settings-aws/graph/badge.svg?token=K77HYDZR3P)](https://codecov.io/github/ceb10n/pydantic-settings-aws)
[![PyPI - Implementation](https://img.shields.io/pypi/implementation/pydantic-settings-aws)](https://pypi.org/project/pydantic-settings-aws)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pydantic-settings-aws)](https://pypi.org/project/pydantic-settings-aws)
[![Pydantic v2 only](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://docs.pydantic.dev/latest/contributing/#badges)
[![PyPI - License](https://img.shields.io/pypi/l/pydantic-settings-aws)](https://pypi.org/project/pydantic-settings-aws)

Settings management using Pydantic and Amazon Web Services / Secrets Manager.

## 💽 Installation

Install using `pip install -U pydantic-settings-aws`.

## 📜 Example

You can create and manage your own secrets manager client or leave it to pydantic-settings-aws.

If you want to leave to pydantic-settings-aws to deal with boto3, you can either pass your credential information or leave it to boto3 to figure it out.

To check how boto3 will look for your configurations, check [Configuring credentials](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#configuring-credentials).

### 🧑🏻‍💻 With secrets manager client

```python
import boto3
from pydantic_settings_aws import SecretsManagerBaseSettings


client = boto3.client("secretsmanager")


class AWSSecretsSettings(SecretsManagerBaseSettings):
    model_config = SettingsConfigDict(
        secrets_name="my/secret",
        secrets_client=client
    )

    username: str
    password: str
    name: str | None = None

my_settings = AWSSecretsSettings()
```

And your secrets manager should be:

```json
{
    "username": "admin",
    "password": "admin",
    "name": "John"
}
```

### 🙋🏾‍♂️ With profile name

```python
class AWSSecretsSettings(SecretsManagerBaseSettings):
    model_config = SettingsConfigDict(
        secrets_name="my/secret",
        aws_region="us-east-1",
        aws_profile="dev"
    )

    username: str
    password: str
```

### 🔑 With access key

```python
class AWSSecretsSettings(SecretsManagerBaseSettings):
    model_config = SettingsConfigDict(
        secrets_name="my/secret",
        aws_region="us-east-1",
        aws_access_key_id="aws_access_key_id",
        aws_secret_access_key="aws_secret_access_key",
        aws_session_token="aws_session_token"
    )

    username: str
    password: str
```

### 🔒 With AWS IAM Identity Center (SSO)

```shell
aws sso login --profile my-profile
```

```python
class AWSSecretsSettings(SecretsManagerBaseSettings):
    model_config = SettingsConfigDict(
        secrets_name="my/secret"
    )

    username: str
    password: str
```

### 📄 With JSON Parameter Store

If you have a single JSON-encoded parameter in Parameter Store, you can use `SingleParameterStoreBaseSettings`:

```python
class DatabaseSettings(SingleParameterStoreBaseSettings):
    model_config = SettingsConfigDict(
        ssm_parameter_name="/my/json/parameter",  # Parameter Store parameter name
        aws_profile="dev"  # Optional AWS profile
    )

    username: str
    password: str
    host: str
    port: int
```

Your Parameter Store parameter should contain a JSON string like:

```json
{
    "username": "admin",
    "password": "secret",
    "host": "db.example.com",
    "port": 5432
}
```

The class will automatically:

1. Fetch the parameter from Parameter Store
2. Parse it as JSON
3. Map the JSON fields to your class fields

## 👩🏼‍⚖️ License

This project is licensed under the terms of the [MIT license.](LICENSE)
