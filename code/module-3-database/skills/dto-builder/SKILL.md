---
name: dto-builder
description: Creates Data Transfer Objects (DTOs) from OpenAPI schemas that match API specifications. Use this skill when you need to generate DTO classes with proper validation and conversion methods (from_db_row, to_dict, from_request).
---

# DTO Builder Skill

You create Data Transfer Objects that match OpenAPI schemas. DTOs control the API boundary.

## Role

Build DTO classes that:
- Match OpenAPI schema specifications exactly
- Include conversion methods for database-to-API and request-to-internal data flows
- Apply validation at the API boundary
- Maintain consistency with existing DTO patterns

## Capabilities

This skill has access to:
- **read** — Examine OpenAPI specs and existing DTOs
- **edit** — Create and modify DTO files

## Workflow

1. Read `openapi/api-spec.yaml` for schemas
2. Read existing DTOs in `src/models/` to understand patterns
3. Create DTO with `from_db_row()`, `to_dict()`, `from_request()` methods
4. Validate conversion methods match schema fields exactly

## Patterns

This is the standard DTO pattern to follow:

```python
@dataclass
class ResourceDTO:
    id: int
    name: str

    @classmethod
    def from_db_row(cls, row):
        return cls(id=row['id'], name=row['name'])

    def to_dict(self):
        return {'id': self.id, 'name': self.name}
```

Include input-specific DTOs (CreateDTO, UpdateDTO) with validation:

```python
@dataclass
class ResourceCreateDTO:
    name: str

    def validate(self):
        if not self.name or len(self.name) < 1:
            raise ValueError("name is required")
        return True
```

## Rules

- ❌ CANNOT modify OpenAPI spec
- ❌ CANNOT add fields not in schema
- ✅ MUST match schema exactly
- ✅ Validation only in input DTOs (CreateDTO)
- ✅ Output DTOs (ResponseDTO) are read-only mappings

## Handoffs

After creating DTOs, hand off to:
- **schema-validator** — To verify DTO implementation matches OpenAPI spec

---

*Type: Doer | Model Tier: Fast*
