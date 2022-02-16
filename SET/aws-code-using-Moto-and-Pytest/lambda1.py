import boto3

class MyLambdaClient:
  def __init__(self, region_name="us-east-1"):
    self.client = boto3.client("lambda", region_name=region_name)
    
  def invoke(self, function_name, invocation_type, payload, log_type=None, client_context=None, qualifier=None):
    """Returns a success status with response data. """
    response = self.client.invoke(FunctionName=function_name, InvocationType=invocation_type, LogType=log_type, ClientContext=client_context, Payload=payload, Qualifier=qualifier)
    
    return response