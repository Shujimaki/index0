from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash
from datetime import datetime
from app import database
from app.models import User, NotificationSettings, SeismicEvent
from app.ph_locations import get_all_provinces, get_cities_in_province
from app.api import get_latest_earthquake

bp = Blueprint('web', __name__)


@bp.route('/')
def homepage():
    return render_template('index.html', current_year=datetime.now().year)


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        province = request.form.get('province')
        city = request.form.get('city')
        
        if not all([full_name, email, province, city]):
            flash('All fields are required', 'error')
            return redirect(url_for('web.signup'))
        
        existing_user = User.query.filter_by(email_address=email).first()
        if existing_user:
            flash('Email already registered', 'error')
            return redirect(url_for('web.signup'))
        
        new_user = User(
            full_name=full_name,
            email_address=email,
            user_province=province,
            user_city=city
        )
        database.session.add(new_user)
        database.session.flush()
        
        settings = NotificationSettings(user_id=new_user.id)
        database.session.add(settings)
        database.session.commit()
        
        flash('Registration successful!', 'success')
        return redirect(url_for('web.dashboard', user_id=new_user.id))
    
    provinces = get_all_provinces()
    return render_template('signup.html', provinces=provinces, current_year=datetime.now().year)


@bp.route('/dashboard/<int:user_id>')
def dashboard(user_id):
    user = User.query.get_or_404(user_id)
    settings = NotificationSettings.query.filter_by(user_id=user_id).first()
    provinces = get_all_provinces()
    
    return render_template(
        'dashboard.html',
        user=user,
        settings=settings,
        provinces=provinces,
        current_year=datetime.now().year
    )


@bp.route('/dashboard/<int:user_id>/settings', methods=['POST'])
def update_settings(user_id):
    user = User.query.get_or_404(user_id)
    settings = NotificationSettings.query.filter_by(user_id=user_id).first()
    
    if not settings:
        settings = NotificationSettings(user_id=user_id)
        database.session.add(settings)
    
    settings.magnitude_threshold = float(request.form.get('magnitude_threshold', 3.0))
    settings.monitor_location_type = request.form.get('location_type', 'near_me')
    settings.add_safety_tips = request.form.get('include_tips') == 'on'
    settings.proximity_range_km = float(request.form.get('range_km', 100.0))
    
    if settings.monitor_location_type == 'custom':
        settings.alternate_province = request.form.get('custom_province')
        settings.alternate_city = request.form.get('custom_city')
    
    database.session.commit()
    flash('Settings updated successfully!', 'success')
    
    return redirect(url_for('web.dashboard', user_id=user_id))


@bp.route('/api/status')
def application_status():
    return jsonify({
        'status': 'operational',
        'timestamp': datetime.now().isoformat(),
        'service': 'index0-earthquake-monitor'
    })


@bp.route('/api/earthquake/latest')
def latest_earthquake():
    return get_latest_earthquake()


@bp.route('/api/provinces')
def api_provinces():
    return jsonify(get_all_provinces())


@bp.route('/api/cities/<province>')
def api_cities(province):
    return jsonify(get_cities_in_province(province))


@bp.route('/api/events')
def api_events():
    events = SeismicEvent.query.order_by(SeismicEvent.occurred_at.desc()).limit(20).all()
    return jsonify([event.serialize() for event in events])