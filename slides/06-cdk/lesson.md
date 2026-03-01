## Module 6: CDK Introduction (1.0 hr)

### Learning Objectives
- Understand Infrastructure as Code concepts
- See how CDK differs from CloudFormation/Terraform
- Create a basic CDK stack for the API
- Prepare foundation for Course 5 deployment

> **Note:** This is an introduction. Course 5 goes much deeper into CDK and deployment.

---

### 6.1 Infrastructure as Code Concepts (20 min)

**Concept:** Understand why we define infrastructure in code, not consoles.

#### The Problem with Console Clicking

```
┌──────────────────────────────────────────────────────────────────┐
│              CONSOLE CLICKING PROBLEMS                            │
│                                                                   │
│   "I set up the Lambda in the AWS console..."                    │
│                                                                   │
│   Problems:                                                       │
│   • Can't reproduce: "What settings did I click?"               │
│   • Can't review: No PR for infrastructure changes               │
│   • Can't version: Which config is in production?                │
│   • Drift happens: Someone changes it manually                   │
│   • No audit trail: Who changed what when?                       │
│   • Hard to replicate: Dev/staging/prod are all different       │
│                                                                   │
│   Infrastructure as Code solves all of these.                    │
└──────────────────────────────────────────────────────────────────┘
```

#### Infrastructure as Code Benefits

| Benefit | Description |
|---------|-------------|
| **Reproducible** | Same code = same infrastructure |
| **Reviewable** | PR review for infra changes |
| **Versioned** | Git history tracks all changes |
| **Testable** | Can test infra before deploying |
| **Documented** | Code IS the documentation |

#### CDK vs Alternatives

| Tool | Language | Cloud Support | When to Use |
|------|----------|---------------|-------------|
| **CDK** | Python, TypeScript, etc. | AWS only | AWS-heavy, prefer real code |
| **Terraform** | HCL | Multi-cloud | Multi-cloud, large community |
| **CloudFormation** | YAML/JSON | AWS only | AWS-native, don't need abstraction |
| **Pulumi** | Python, TypeScript, etc. | Multi-cloud | Multi-cloud, prefer real code |

**Why CDK for this course:**
- Uses Python (same as rest of course)
- AWS-native (good for learning AWS concepts)
- Real programming constructs (loops, conditions, functions)
- Generates CloudFormation (industry standard, portable)

> 🏢 **Enterprise Context:** Most enterprises use either Terraform (multi-cloud) or CDK (AWS-heavy). **The concepts transfer** — modules, state management, dependencies, drift detection all work the same way conceptually.

---

### 6.2 Basic CDK Stack (25 min)

**Concept:** Create a CDK stack that could deploy the API.

#### CDK Project Structure

```
cdk/
├── app.py              # CDK app entry point
├── cdk.json            # CDK configuration
├── requirements.txt    # CDK dependencies
└── stacks/
    └── api_stack.py    # API infrastructure stack
```

#### CDK App Entry Point

```python
# cdk/app.py
#!/usr/bin/env python3
"""
CDK application entry point.

This is where CDK stacks are instantiated and synthesized.
"""

import aws_cdk as cdk
from stacks.api_stack import ApiStack

app = cdk.App()

# Create the API stack
ApiStack(
    app, 
    "FraudDetectionApi",
    description="Fraud Detection API - Course 4",
    env=cdk.Environment(
        # Uses AWS_DEFAULT_REGION and AWS_ACCOUNT_ID from environment
        # or defaults to current credentials
    )
)

app.synth()
```

#### API Stack Definition

```python
# cdk/stacks/api_stack.py
"""
Infrastructure for the Fraud Detection API.

Creates:
- Lambda function running Flask app
- API Gateway for HTTP access
- (Course 5 adds: RDS, Cognito, CloudWatch)
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
    """Infrastructure for the Fraud Detection API."""
    
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        
        # Lambda function for the API
        # This runs your Flask app in a serverless environment
        api_lambda = lambda_.Function(
            self, "ApiHandler",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="lambda_handler.handler",  # Entry point
            code=lambda_.Code.from_asset(
                "../src",
                exclude=["__pycache__", "*.pyc", ".pytest_cache"]
            ),
            timeout=Duration.seconds(30),  # Match agent timeout
            memory_size=256,  # MB - adjust based on model size
            environment={
                "DATABASE_PATH": "/tmp/app.db",  # Lambda writable dir
                "INSIGHTS_MODEL": "anthropic/claude-3-haiku-20240307",
            },
            description="Fraud Detection API - Flask application"
        )
        
        # API Gateway - creates public HTTP endpoint
        api = apigw.LambdaRestApi(
            self, "FraudApi",
            handler=api_lambda,
            proxy=True,  # Proxy all requests to Lambda
            deploy_options=apigw.StageOptions(
                stage_name="v1",
                throttling_rate_limit=100,  # Requests per second
                throttling_burst_limit=200,  # Burst capacity
            ),
            description="Fraud Detection API Gateway"
        )
        
        # Output the API URL
        CfnOutput(
            self, "ApiUrl",
            value=api.url,
            description="API Gateway URL"
        )
        
        # Store for use by other stacks
        self.api = api
        self.api_lambda = api_lambda
```

#### What This Creates

```
┌─────────────────────────────────────────────────────────────┐
│                   CDK STACK CREATES                          │
│                                                              │
│   Internet                                                   │
│      │                                                       │
│      ▼                                                       │
│   ┌─────────────────┐                                       │
│   │  API Gateway    │  ← Public HTTPS endpoint              │
│   │  /v1/*          │  ← Rate limiting, throttling          │
│   └────────┬────────┘                                       │
│            │                                                 │
│            ▼                                                 │
│   ┌─────────────────┐                                       │
│   │  Lambda         │  ← Your Flask app                     │
│   │  (Serverless)   │  ← Pay only when called               │
│   │                 │  ← Auto-scales                        │
│   └────────┬────────┘                                       │
│            │                                                 │
│            ▼                                                 │
│   ┌─────────────────┐                                       │
│   │  Your Code      │  ← Same Flask app, same routes       │
│   │  (app.py)       │  ← No changes needed                  │
│   └─────────────────┘                                       │
│                                                              │
│   CDK generates CloudFormation → CloudFormation creates AWS │
└─────────────────────────────────────────────────────────────┘
```

> 💡 **Progressive Disclosure:** We're creating the foundation here. Course 5 adds:
> - RDS PostgreSQL (database upgrade)
> - Cognito (authentication)
> - CloudWatch (monitoring and alerts)
> - CodePipeline (CI/CD automation)

**Hands-On:**
- Create `cdk/` directory structure
- Create `cdk/app.py` and `cdk/stacks/api_stack.py`
- Run `cdk synth` to see generated CloudFormation
- **Do NOT deploy** — Course 5 covers actual deployment

```bash
cd cdk
pip install aws-cdk-lib constructs
cdk synth  # Generates CloudFormation template
# Output in cdk.out/FraudDetectionApi.template.json
```

---

### 6.3 ROI Trade-off: Infrastructure Decisions (15 min)

**Concept:** Document infrastructure decisions using the proposal pattern.

#### Infrastructure Proposal Document

```markdown
# docs/proposals/003-cdk-architecture.md

## Decision: CDK for Infrastructure as Code

### Context
Need infrastructure as code for deploying Flask API to AWS.
Must support local development, staging, and production environments.

### Options Considered

| Option | Pros | Cons |
|--------|------|------|
| **CDK (Python)** | Same language as app, AWS-native, type-safe | AWS-only |
| **Terraform** | Multi-cloud, huge community, mature | Different language (HCL) |
| **CloudFormation** | AWS-native, widely used | Verbose YAML, hard to test |
| **Serverless Framework** | Easy Lambda deployment | Limited to serverless |

### Decision: CDK

Choosing CDK because:
1. **Python consistency** — Same language as application code
2. **Type safety** — IDE autocomplete, catch errors before deploy
3. **Real programming** — Loops, conditions, functions for complex logic
4. **Generates CloudFormation** — Portable if we need to switch

### Trade-offs Accepted

| Trade-off | Mitigation |
|-----------|------------|
| AWS lock-in | CDK generates CloudFormation; can convert if needed |
| Smaller community than Terraform | AWS documentation is excellent |
| Team needs to learn CDK | Same concepts as Terraform |

### Migration Path (if needed)

If multi-cloud becomes necessary:
1. CDK generates CloudFormation templates
2. Tools exist: `cf2tf` converts CloudFormation → Terraform
3. Core concepts (stacks, resources, dependencies) transfer directly

### Implementation Notes

- Start with single stack for simplicity
- Course 5 will add: database stack, auth stack, monitoring
- Environment variables for environment-specific config
- Use CDK context for dev/staging/prod differences

### Review Checklist

- [ ] Lambda memory sized for model loading
- [ ] Timeout matches agent timeout (30s)
- [ ] Rate limiting configured
- [ ] Outputs defined for cross-stack references
```

> 🏢 **Enterprise Context:** Document your infrastructure decisions. When someone asks "why CDK instead of Terraform?" — you have an answer with:
> - Options considered
> - Rationale for decision
> - Trade-offs acknowledged
> - Migration path if needed

---

### Module 6 Checkpoint

**By end of Module 6, you have:**
- ✅ Understanding of Infrastructure as Code
- ✅ Basic CDK stack (not deployed)
- ✅ Infrastructure decision documented
- ✅ Foundation for Course 5 deployment

**Git tag:** `module-6-cdk`

**HISTORY.md Entry:**
```markdown
## Module 6 Complete

### Implemented
- CDK project structure in cdk/
- Basic api_stack.py with Lambda + API Gateway
- Infrastructure proposal document

### Decisions (docs/proposals/003-cdk-architecture.md)
- Using CDK for AWS infrastructure
- Trade-off: AWS lock-in acceptable for learning
- Migration path to Terraform documented if needed

### What's NOT Deployed
- CDK stack created but NOT deployed to AWS
- No AWS resources created
- Actual deployment covered in Course 5

### Course 5 Will Add
- RDS PostgreSQL database
- Cognito authentication
- CloudWatch monitoring
- CodePipeline CI/CD

### Next: Module 7 — Integration & Handoff
```

---

