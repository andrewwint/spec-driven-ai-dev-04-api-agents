"""Customer Management Endpoints."""

from flask import Blueprint, request, jsonify
from src.database.db import get_connection
from src.models.customer import CustomerDTO, CustomerCreateDTO

customers_bp = Blueprint('customers', __name__)


@customers_bp.route('/customers', methods=['GET'])
def list_customers():
    """List customers with pagination."""
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)

    if limit < 1 or limit > 100:
        return jsonify({'error': 'limit must be 1-100'}), 400

    with get_connection() as conn:
        total = conn.execute('SELECT COUNT(*) FROM customers').fetchone()[0]
        cursor = conn.execute(
            'SELECT * FROM customers ORDER BY id LIMIT ? OFFSET ?',
            (limit, offset)
        )
        customers = [CustomerDTO.from_db_row(row).to_dict() for row in cursor.fetchall()]

    return jsonify({
        'customers': customers,
        'total': total,
        'limit': limit,
        'offset': offset
    }), 200


@customers_bp.route('/customers', methods=['POST'])
def create_customer():
    """Create a customer."""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Request body required'}), 400

    try:
        customer_input = CustomerCreateDTO.from_request(data)
    except ValueError as e:
        return jsonify({'error': 'Validation failed', 'details': str(e).split('; ')}), 400

    with get_connection() as conn:
        existing = conn.execute(
            'SELECT id FROM customers WHERE email = ?',
            (customer_input.email,)
        ).fetchone()

        if existing:
            return jsonify({'error': 'Email already exists'}), 409

        cursor = conn.execute(
            'INSERT INTO customers (name, email) VALUES (?, ?)',
            (customer_input.name, customer_input.email)
        )
        conn.commit()

        created = conn.execute(
            'SELECT * FROM customers WHERE id = ?',
            (cursor.lastrowid,)
        ).fetchone()

    return jsonify(CustomerDTO.from_db_row(created).to_dict()), 201


@customers_bp.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id: int):
    """Get customer by ID."""
    with get_connection() as conn:
        row = conn.execute(
            'SELECT * FROM customers WHERE id = ?',
            (customer_id,)
        ).fetchone()

        if not row:
            return jsonify({'error': 'Customer not found'}), 404

    return jsonify(CustomerDTO.from_db_row(row).to_dict()), 200
