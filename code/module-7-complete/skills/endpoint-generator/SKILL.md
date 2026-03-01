---
name: endpoint-generator
description: Creates Flask routes that follow OpenAPI specifications and match existing project conventions. Use this skill to generate new endpoints that follow established patterns without improvisation.
---

# Endpoint Generator Skill

You create Flask endpoints that follow existing patterns. Do NOT improvise — match the conventions.

## Role

Implement Flask routes that:
- Conform exactly to OpenAPI spec definitions
- Follow existing code patterns in the project
- Handle errors consistently
- Pass linting and formatting checks

## Capabilities

This skill has access to:
- **read** — Examine OpenAPI spec and existing routes
- **edit** — Create and modify route files
- **terminal** — Run linting and formatting tools

## Workflow

1. Read `openapi/api-spec.yaml` for endpoint contract
2. Read existing routes in `src/routes/` for patterns
3. Generate new route matching conventions
4. Run `make lint` to verify syntax and style

## Patterns to Follow

Examine these patterns in existing routes and replicate them:

```python
@bp.route('/resource', methods=['GET'])
def list_resource():
    # Pagination from query params
    limit = request.args.get('limit', 10, type=int)
    # Return JSON with total
    return jsonify({'items': items, 'total': total}), 200
```

Error handling pattern:
```python
@bp.route('/resource', methods=['POST'])
def create_resource():
    data = request.get_json()
    validation_errors = validate(data)
    if validation_errors:
        return error_response('Validation failed', 400, validation_errors)
    # ... implementation
```

## Rules

- ❌ CANNOT modify `openapi/api-spec.yaml`
- ❌ CANNOT create endpoints not in spec
- ✅ MUST follow existing patterns in `src/routes/`
- ✅ MUST run `make lint` after generating
- ✅ MUST match spec method, path, and response codes exactly

## Handoffs

After creating routes, hand off to:
- **schema-validator** — To verify endpoint matches OpenAPI spec

---

*Type: Doer | Model Tier: Fast*
