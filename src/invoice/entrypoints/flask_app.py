from flask import Flask, jsonify, request, abort
from invoice.service_layer import handlers
from invoice.domain import commands
from invoice import bootstrap
from invoice import views
import logging
import re

logger = logging.getLogger(__name__)
app = Flask(__name__)

allowed_ips = ['127.0.0.1', '192.168.1.1', '0.0.0.0', '172.18.0.1']

def check_ip():
    if request.remote_addr not in allowed_ips:
        abort(403, f'Forbidden: Your IP {request.remote_addr} is not allowed to access this resource.')

app.before_request(check_ip)

class BusWrapper:
    def __init__(self, bus):
        self.bus = bus
app.message_bus = BusWrapper(bootstrap.bootstrap())

@app.route('/invoices', methods=['POST'])
def create_invoice():
    
    data = request.json
    if 'email' not in data or 'amount' not in data:
        abort(400, "Missing required fields in the request. The request should have email and amount fields.")
    if not is_valid_email(data['email']):
        abort(400, "Invalid email")
    if not is_valid_amount(data['amount']):
        abort(400, "Invalid amount")
    cmd = commands.CreateInvoice(
        email=data['email'],
        amount=data['amount']
    )
    try:
        print(f'Got command {cmd}')
        app.message_bus.bus.handle(cmd)
        return 'Message dispatched', 201
    except Exception as e:
        logger.exception(e)
        return 'Internal server error', 500

@app.route('/invoices', methods=['GET'])
def get_invoice():
    
    data = request.json
    if 'email' not in data:
        abort(400, "Missing required fields in the request. The request should have email field.")
    if not is_valid_email(data['email']):
        abort(400, "Invalid email")
    result = views.get_invoice_by_email(data['email'], uow=app.message_bus.bus.uow)
    if not result:
        return "Invoice not found", 404
    return jsonify(result), 200

@app.route('/invoices', methods=['PUT'])
def update_invoice():
    data = request.json
    if 'id' not in data or 'amount' not in data:
        abort(400, "Missing required fields in the request. The request should have id and amount fields.")
    if not is_valid_invoice_id(data['id']):
        abort(400, "Invalid invoice_id")
    if not is_valid_amount(data['amount']):
        abort(400, "Invalid amount")
    cmd = commands.UpdateInvoice(
        id=data['id'],
        amount=data['amount']
    )
    try:
        print(f'Got command {cmd}')
        app.message_bus.bus.handle(cmd)
        return 'Update dispatched', 201
    except Exception as e:
        logger.exception(e)
        return 'Internal server error', 500

@app.route('/invoices/<int:invoice_id>', methods=['DELETE'])
def delete_invoice(invoice_id):
    if not is_valid_invoice_id(invoice_id):
        abort(400, "Invalid invoice_id")
    cmd = commands.DeleteInvoice(
        id=invoice_id
    )
    try:
        print(f'Got command {cmd}')
        app.message_bus.bus.handle(cmd)
        return 'Delete dispatched', 200
    except Exception as e:
        logger.exception(e)
        return 'Internal server error', 500

@app.route('/report', methods=['POST'])
def generate_report():
    data = request.json
    if 'email' not in data:
        abort(400, "Missing required fields in the request. The request should have email field.")
    if not is_valid_email(data['email']):
        abort(400, "Invalid email")
    cmd = commands.GenerateInvoiceReport(
        email=data['email']
    )
    try:
        print(f'Got command {cmd}')
        app.message_bus.bus.handle(cmd)
        return 'Report generation dispatched', 200
    except Exception as e:
        logger.exception(e)
        return 'Internal server error', 500

def is_valid_invoice_id(invoice_id):
    return isinstance(invoice_id, int) and invoice_id > 0

def is_valid_email(email):
    email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return bool(re.match(email_regex, email))

def is_valid_amount(amount):
    return isinstance(amount, int) and amount > 0
