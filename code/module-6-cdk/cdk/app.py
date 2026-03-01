#!/usr/bin/env python3
"""CDK Application Entry Point."""

import os
import aws_cdk as cdk
from stacks.api_stack import ApiStack

app = cdk.App()

ApiStack(
    app,
    "FraudDetectionApi",
    description="Fraud Detection API - Course 4",
    env=cdk.Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT'),
        region=os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    )
)

app.synth()
