import boto3
import os
import pytest

from moto import mock_s3, mock_sqs, mock_appsync, mock_lambda, mock_iam


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    
    
@pytest.fixture
def iam_client(aws_credentials):
    with mock_iam():
        conn = boto3.client("iam", region_name="us-east-1")
        yield conn

@pytest.fixture
def lambda_client(aws_credentials):
    with mock_lambda():
        conn = boto3.client("lambda", region_name="us-east-1")
        yield conn
        
@pytest.fixture
def s3_client(aws_credentials):
    with mock_s3():
        conn = boto3.client("s3", region_name="us-east-1")
        yield conn


@pytest.fixture
def sqs_client(aws_credentials):
    with mock_sqs():
        conn = boto3.client("sqs", region_name="us-east-1")
        yield conn
