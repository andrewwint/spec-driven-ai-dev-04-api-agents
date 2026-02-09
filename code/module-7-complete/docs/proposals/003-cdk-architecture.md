# Architecture Decision: Infrastructure as Code

## Question

What IaC tool should we use for AWS deployment?

## Options Evaluated

| Option | Pros | Cons |
|--------|------|------|
| **CDK (chosen)** | Python, type-safe, generates CloudFormation | AWS-only |
| Terraform | Multi-cloud, huge community | HCL language |
| CloudFormation | AWS-native, no dependencies | Verbose YAML |

## Decision

**Selected:** AWS CDK (Python)

**Rationale:**
- Python consistency with rest of course
- Type-safe constructs catch errors early
- Generates CloudFormation (portable)
- Natural for AWS-focused deployment

**Trade-offs accepted:**
- AWS lock-in (acceptable for this course)
- Smaller community than Terraform

## Migration Path

CDK generates CloudFormation templates. If multi-cloud needed later:
1. Export CloudFormation from CDK
2. Convert to Terraform using cf2tf
3. Or rewrite in Terraform (patterns transfer)

## Review Date

Revisit if multi-cloud becomes requirement.
