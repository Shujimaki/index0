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
    
    # Username is the full name from registration
    user = User.query.filter_by(full_name=username).first()
    
    if user and user.check_password(password):
        session['user_id'] = user.id
        session['user_name'] = user.full_name
        flash('Login successful!', 'success')
        return redirect(url_for('web.dashboard', user_id=user.id))
    else:
        flash('Invalid username or password.', 'error')
        return redirect(url_for('web.homepage'))


@bp.route('/register', methods=['POST'])
def register():
    """Handle user registration from auth page"""
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    region = request.form.get('region')
    province_code = request.form.get('province')
    city_code = request.form.get('city')
    
    if not all([name, email, password, region, province_code, city_code]):
        flash('All fields are required', 'error')
        return redirect(url_for('web.homepage'))
    
    # Check for existing user by email or name
    existing_user = User.query.filter(
        (User.email_address == email) | (User.full_name == name)
    ).first()
    if existing_user:
        flash('Name or email already registered. Please login or use different credentials.', 'error')
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
    new_user.set_password(password)
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


@bp.route('/onboarding')
def onboarding():
    """Onboarding page for new users"""
    return render_template('onboarding.html')


@bp.route('/onboarding2')
def onboarding2():
    """Onboarding page 2 - Emergency Kit and About"""
    return render_template('onboarding2.html')


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


@bp.route('/test-notification', methods=['POST'])
def test_notification():
    """Test if user would receive notification for a simulated earthquake"""
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    user = User.query.get_or_404(user_id)
    settings = NotificationSettings.query.filter_by(user_id=user_id).first()
    
    if not settings:
        return jsonify({'success': False, 'error': 'No settings found'}), 404
    
    # Get test earthquake parameters
    test_magnitude = float(request.form.get('test_magnitude', 4.5))
    test_region = request.form.get('test_region')
    test_province_code = request.form.get('test_province')
    test_city_code = request.form.get('test_city')
    
    # Get location names
    region_data = PHILIPPINE_GEOGRAPHY.get(test_region)
    if not region_data or test_province_code not in region_data['provinces']:
        return jsonify({'success': False, 'error': 'Invalid location selection'}), 400
    
    test_province_name = region_data['provinces'][test_province_code]['name']
    test_city_name = None
    for city in region_data['provinces'][test_province_code]['cities']:
        if city['value'] == test_city_code:
            test_city_name = city['name']
            break
    
    if not test_city_name:
        return jsonify({'success': False, 'error': 'Invalid city selection'}), 400
    
    # Check magnitude criteria
    if test_magnitude < settings.magnitude_threshold:
        return jsonify({
            'success': True,
            'would_send': False,
            'reason': f'Earthquake magnitude ({test_magnitude}) is below your threshold ({settings.magnitude_threshold})',
            'test_earthquake': {
                'magnitude': test_magnitude,
                'location': f'{test_city_name}, {test_province_name}'
            }
        })
    
    # Check location criteria
    location_matches = False
    match_reason = ""
    
    if settings.monitor_location_type == 'near_me':
        # Check if earthquake location matches user's registered location
        if test_province_name.lower() == user.user_province.lower() or \
           test_city_name.lower() == user.user_city.lower():
            location_matches = True
            match_reason = f'Earthquake location ({test_city_name}, {test_province_name}) matches your registered location ({user.user_city}, {user.user_province}) and magnitude ({test_magnitude}) exceeds your threshold ({settings.magnitude_threshold})'
        else:
            match_reason = f'Earthquake location ({test_city_name}, {test_province_name}) does not match your registered location ({user.user_city}, {user.user_province})'
    else:  # custom location
        # Check if earthquake matches custom location
        if settings.alternate_province and settings.alternate_city:
            if test_province_name.lower() == settings.alternate_province.lower() or \
               test_city_name.lower() == settings.alternate_city.lower():
                location_matches = True
                match_reason = f'Earthquake location ({test_city_name}, {test_province_name}) matches your monitored location ({settings.alternate_city}, {settings.alternate_province}) and magnitude ({test_magnitude}) exceeds your threshold ({settings.magnitude_threshold})'
            else:
                match_reason = f'Earthquake location ({test_city_name}, {test_province_name}) does not match your monitored location ({settings.alternate_city}, {settings.alternate_province})'
        else:
            match_reason = 'Custom location monitoring is enabled but no location is set'
    
    # If criteria met, send actual test email
    if location_matches:
        from app.gemini_service import GeminiSummarizer
        from app import email_service
        from flask_mail import Message
        from datetime import datetime
        
        try:
            # Create test earthquake data
            test_earthquake_data = {
                'date_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S PST'),
                'latitude': '14.5995',
                'longitude': '120.9842',
                'depth': '10 km',
                'magnitude': str(test_magnitude),
                'location': f'{test_city_name}, {test_province_name}',
                'detail_link': 'https://earthquake.phivolcs.dost.gov.ph/test-notification'
            }
            
            # Generate AI summary
            from flask import current_app
            summarizer = GeminiSummarizer(current_app.config['GEMINI_API_KEY'])
            summary = summarizer.create_summary(test_earthquake_data, settings.add_safety_tips)
            
            # Compose email
            subject = f"🧪 TEST - Earthquake Alert - Magnitude {test_magnitude}"
            
            body = f"""🧪 TEST EARTHQUAKE NOTIFICATION 🧪

⚠️ THIS IS A TEST EMAIL - NOT A REAL EARTHQUAKE ⚠️

Dear {user.full_name},

{summary}

---
TEST EARTHQUAKE DETAILS:
• Time: {test_earthquake_data['date_time']}
• Location: {test_earthquake_data['location']}
• Magnitude: {test_earthquake_data['magnitude']}
• Depth: {test_earthquake_data['depth']}
• Coordinates: {test_earthquake_data['latitude']}, {test_earthquake_data['longitude']}

Your monitored location: {user.user_city}, {user.user_province}

---
SOURCE: This earthquake information is sourced from PHIVOLCS (Philippine Institute of 
Volcanology and Seismology) official earthquake bulletins.

DISCLAIMER: This summary was generated by artificial intelligence. While we strive for 
accuracy, please refer to the official PHIVOLCS bulletin for authoritative information.

---
⚠️ THIS IS A TEST EMAIL FROM YOUR DASHBOARD
You ran a test to verify your notification settings are working correctly.

This is an automated notification from the Earthquake Monitoring System.
You can update your preferences in your dashboard.

Stay safe!"""
            
            # Send email
            email_msg = Message(
                subject=subject,
                recipients=[user.email_address],
                body=body
            )
            email_service.send(email_msg)
            
            return jsonify({
                'success': True,
                'would_send': True,
                'email_sent': True,
                'reason': match_reason + '<br><br>✉️ <strong>Test email sent to ' + user.email_address + '</strong>',
                'test_earthquake': {
                    'magnitude': test_magnitude,
                    'location': f'{test_city_name}, {test_province_name}'
                }
            })
        except Exception as e:
            return jsonify({
                'success': True,
                'would_send': True,
                'email_sent': False,
                'reason': match_reason + f'<br><br>⚠️ Email would be sent, but failed: {str(e)}',
                'test_earthquake': {
                    'magnitude': test_magnitude,
                    'location': f'{test_city_name}, {test_province_name}'
                }
            })
    else:
        return jsonify({
            'success': True,
            'would_send': False,
            'email_sent': False,
            'reason': match_reason,
            'test_earthquake': {
                'magnitude': test_magnitude,
                'location': f'{test_city_name}, {test_province_name}'
            }
        })


@bp.route('/api/events')
def api_events():
    """Get recent seismic events"""
    events = SeismicEvent.query.order_by(SeismicEvent.occurred_at.desc()).limit(20).all()
    return jsonify([event.serialize() for event in events])