from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash, session
from datetime import datetime
from app import database
from app.models import User, NotificationSettings, SeismicEvent
from app.ph_locations import get_all_provinces, get_cities_in_province
from app.api import get_latest_earthquake
from app.cities import PHILIPPINE_GEOGRAPHY, REGIONS_LIST

bp = Blueprint('web', __name__)


@bp.route('/')
def homepage():
    """Landing page with login/registration"""
    return render_template('auth_page.html', 
                          logo_url='/static/yaniglogo.png',
                          regions=REGIONS_LIST)


@bp.route('/login', methods=['POST'])
def login():
    """Handle user login"""
    username = request.form.get('username')
    password = request.form.get('password')
    
    # For now, using email as username since we don't have password field
    # In production, implement proper password hashing
    user = User.query.filter_by(email_address=username).first()
    
    if user:
        session['user_id'] = user.id
        session['user_name'] = user.full_name
        flash('Login successful!', 'success')
        return redirect(url_for('web.dashboard', user_id=user.id))
    else:
        flash('User not found. Please register first.', 'error')
        return redirect(url_for('web.homepage'))


@bp.route('/register', methods=['POST'])
def register():
    """Handle user registration from auth page"""
    name = request.form.get('name')
    email = request.form.get('email')
    region = request.form.get('region')
    province_code = request.form.get('province')
    city_code = request.form.get('city')
    
    if not all([name, email, region, province_code, city_code]):
        flash('All fields are required', 'error')
        return redirect(url_for('web.homepage'))
    
    existing_user = User.query.filter_by(email_address=email).first()
    if existing_user:
        flash('Email already registered. Please login.', 'error')
        return redirect(url_for('web.homepage'))
    
    # Get actual province and city names from codes
    province_name = None
    city_name = None
    
    region_data = PHILIPPINE_GEOGRAPHY.get(region)
    if region_data and province_code in region_data['provinces']:
        province_name = region_data['provinces'][province_code]['name']
        cities = region_data['provinces'][province_code]['cities']
        for city in cities:
            if city['value'] == city_code:
                city_name = city['name']
                break
    
    if not province_name or not city_name:
        flash('Invalid location selection', 'error')
        return redirect(url_for('web.homepage'))
    
    new_user = User(
        full_name=name,
        email_address=email,
        user_province=province_name,
        user_city=city_name
    )
    database.session.add(new_user)
    database.session.flush()
    
    settings = NotificationSettings(user_id=new_user.id)
    database.session.add(settings)
    database.session.commit()
    
    session['user_id'] = new_user.id
    session['user_name'] = new_user.full_name
    flash('Registration successful!', 'success')
    return redirect(url_for('web.dashboard', user_id=new_user.id))


@bp.route('/logout')
def logout():
    """Handle user logout"""
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('web.homepage'))


@bp.route('/dashboard/<int:user_id>')
def dashboard(user_id):
    """User dashboard with settings"""
    user = User.query.get_or_404(user_id)
    settings = NotificationSettings.query.filter_by(user_id=user_id).first()
    
    if not settings:
        settings = NotificationSettings(user_id=user_id)
        database.session.add(settings)
        database.session.commit()
    
    return render_template(
        'dashboard.html',
        user=user,
        user_name=user.full_name,
        logo_url='/static/yaniglogo.png',
        settings=settings,
        regions=REGIONS_LIST,
        current_year=datetime.now().year
    )


@bp.route('/save-preferences', methods=['POST'])
@bp.route('/dashboard/<int:user_id>/settings', methods=['POST'])
def update_settings(user_id=None):
    """Update user notification settings"""
    if not user_id:
        user_id = session.get('user_id')
    
    if not user_id:
        flash('Please login first', 'error')
        return redirect(url_for('web.homepage'))
    
    user = User.query.get_or_404(user_id)
    settings = NotificationSettings.query.filter_by(user_id=user_id).first()
    
    if not settings:
        settings = NotificationSettings(user_id=user_id)
        database.session.add(settings)
    
    # Get magnitude from slider
    settings.magnitude_threshold = float(request.form.get('magnitude', 3.0))
    
    # Get location preference
    location_pref = request.form.get('location_preference', 'near_me')
    settings.monitor_location_type = location_pref
    
    if location_pref == 'custom':
        region_code = request.form.get('region')
        province_code = request.form.get('province')
        city_code = request.form.get('city')
        
        # Get actual names from codes
        region_data = PHILIPPINE_GEOGRAPHY.get(region_code)
        if region_data and province_code in region_data['provinces']:
            settings.alternate_province = region_data['provinces'][province_code]['name']
            cities = region_data['provinces'][province_code]['cities']
            for city in cities:
                if city['value'] == city_code:
                    settings.alternate_city = city['name']
                    break
    
    # Safety tips checkbox
    settings.add_safety_tips = request.form.get('safety_tips') == 'on'
    settings.proximity_range_km = float(request.form.get('range_km', 100.0))
    
    database.session.commit()
    flash('Settings saved successfully!', 'success')
    
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


@bp.route('/api/provinces/<region_code>')
def api_provinces_by_region(region_code):
    """Get provinces for a region"""
    region_data = PHILIPPINE_GEOGRAPHY.get(region_code)
    
    if region_data:
        provinces = [
            {"value": code, "name": data["name"]} 
            for code, data in region_data["provinces"].items()
        ]
        return jsonify(provinces)
    else:
        return jsonify([])


@bp.route('/api/cities/<region_code>/<province_code>')
def api_cities_by_province(region_code, province_code):
    """Get cities for a province in a region"""
    region_data = PHILIPPINE_GEOGRAPHY.get(region_code)
    
    if region_data and province_code in region_data["provinces"]:
        return jsonify(region_data["provinces"][province_code]["cities"])
    else:
        return jsonify([])


@bp.route('/api/events')
def api_events():
    """Get recent seismic events"""
    events = SeismicEvent.query.order_by(SeismicEvent.occurred_at.desc()).limit(20).all()
    return jsonify([event.serialize() for event in events])