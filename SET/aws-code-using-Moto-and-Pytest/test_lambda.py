import pytest, boto3
from moto import mock_iam

from lambda1 import MyLambdaClient

@pytest.fixture
def function_name():
  return "lambda1"

@pytest.fixture
def invocation_type():
  return "Event"

@pytest.fixture
def payload():
  return {"company":"ingkle", "value":9999}
  
# @pytest.fixture
# def lambda_test(lambda_client, iam_client, function_name, invocation_type, payload):
  
#   lambda_client.create_function(FunctionName=function_name, Role="arn:aws:iam::123456789012:role/lambda", Code=dict(ZipFile=b'hello'), Handler="index.handler", Runtime="python3.10.0")
#   yield
  
def test_invoke(lambda_client):
  my_client = MyLambdaClient()
  functions = my_client.invoke(function_name="lambda1", invocation_type="Event", payload={"company":"ingkle", "value":9999})
  
  assert "lambda1" in functions
