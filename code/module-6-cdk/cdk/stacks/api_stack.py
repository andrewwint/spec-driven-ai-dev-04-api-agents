"""
API Stack - Lambda + API Gateway.

Foundation for Course 5 deployment. Not deployed in Course 4.
"""

from aws_cdk import (
    Stack,
    Duration,
    CfnOutput,
    aws_lambda as lambda_,
    aws_apigateway as apigw,
)
from constructs import Construct


class ApiStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Lambda function for API
        api_lambda = lambda_.Function(
            self, "ApiHandler",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="lambda_handler.handler",
            code=lambda_.Code.from_asset("../src"),
            timeout=Duration.seconds(30),
            memory_size=256,
            environment={
                "DATABASE_PATH": "/tmp/app.db"
            }
        )

        # API Gateway
        api = apigw.LambdaRestApi(
            self, "FraudApi",
            handler=api_lambda,
            proxy=True,
            deploy_options=apigw.StageOptions(
                stage_name="v1",
                throttling_rate_limit=100,
                throttling_burst_limit=200
            )
        )

        CfnOutput(self, "ApiUrl", value=api.url)
