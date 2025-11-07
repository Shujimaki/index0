from flask import Blueprint, render_template, jsonify
from datetime import datetime

bp = Blueprint('web', __name__)


@bp.route('/')
def homepage():
    return render_template('index.html', current_year=datetime.now().year)


@bp.route('/api/status')
def application_status():
    return jsonify({
        'status': 'operational',
        'timestamp': datetime.now().isoformat(),
        'service': 'index0'
    })