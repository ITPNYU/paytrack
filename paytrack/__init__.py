from flask import Flask
from flask.ext.restless import APIManager
from paytrack.authn import login_manager, auth_func
from paytrack.config import config
from paytrack.database import Base, db_session, engine
from paytrack.models import Account, Credit, Invoice, Payer, Payment, Refund, User

app = Flask(__name__)
app.secret_key = config.get('secrets', 'SECRET')

# Flask-Login and authn code
login_manager.init_app(app)

def add_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'HEAD, GET, POST, PATCH, PUT, OPTIONS, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

# Flask-Restless API endpoints
# note: GET preprocessors pulled in via paytrack.authn.auth_func
manager = APIManager(app, session=db_session, preprocessors=dict(GET_SINGLE=[auth_func], GET_MANY=[auth_func]))
account_blueprint = manager.create_api(Account, methods=['GET', 'DELETE', 'PATCH', 'POST'], collection_name='account', url_prefix='/v1')
credit_blueprint = manager.create_api(Credit, methods=['GET', 'DELETE', 'PATCH', 'POST'], collection_name='credit', url_prefix='/v1')
invoice_blueprint = manager.create_api(Invoice, methods=['GET', 'DELETE', 'PATCH', 'POST'], collection_name='invoice', url_prefix='/v1')
payer_blueprint = manager.create_api(Payer, methods=['GET', 'DELETE', 'PATCH', 'POST'], collection_name='payer', url_prefix='/v1', include_methods = ['payments_due'])
payment_blueprint = manager.create_api(Payment, methods=['GET', 'POST'], collection_name='payment', url_prefix='/v1')
refund_blueprint = manager.create_api(Refund, methods=['GET', 'DELETE', 'PATCH', 'POST'], collection_name='refund', url_prefix='/v1')

app.after_request(add_cors_header)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
