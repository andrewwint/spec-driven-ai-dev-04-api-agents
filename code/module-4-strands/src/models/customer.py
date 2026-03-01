"""
Customer Data Transfer Objects.

DTOs control what crosses the API boundary.
"""

from dataclasses import dataclass
import re


@dataclass
class CustomerDTO:
    """API representation of a customer."""
    id: int
    name: str
    email: str

    @classmethod
    def from_db_row(cls, row) -> 'CustomerDTO':
        return cls(id=row['id'], name=row['name'], email=row['email'])

    def to_dict(self) -> dict:
        return {'id': self.id, 'name': self.name, 'email': self.email}


@dataclass
class CustomerCreateDTO:
    """Input for creating a customer."""
    name: str
    email: str

    @classmethod
    def from_request(cls, data: dict) -> 'CustomerCreateDTO':
        errors = []

        name = data.get('name', '').strip() if data.get('name') else ''
        if not name:
            errors.append('name is required')
        elif len(name) > 100:
            errors.append('name must be 100 characters or less')

        email = data.get('email', '').strip().lower() if data.get('email') else ''
        if not email:
            errors.append('email is required')
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors.append('email format is invalid')

        if errors:
            raise ValueError('; '.join(errors))

        return cls(name=name, email=email)
