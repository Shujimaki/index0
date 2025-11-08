from flask import Blueprint, render_template, jsonify
from datetime import datetime

bp = Blueprint('web', __name__)


@bp.route('/')
def homepage():
    return render_template('auth_page.html')


@bp.route('/api/status')
def application_status():
    return jsonify({
        'status': 'operational',
        'timestamp': datetime.now().isoformat(),
        'service': 'index0'
    })