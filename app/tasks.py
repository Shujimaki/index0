from app import database, email_service, task_queue
from app.models import User, NotificationSettings, SeismicEvent
from app.api import fetch_latest_earthquake_raw
from app.gemini_service import GeminiSummarizer
from app.location_service import LocationAnalyzer
from flask_mail import Message
from flask import current_app
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@task_queue.task(bind=True, max_retries=3, name='app.tasks.check_and_process_earthquakes')
def check_and_process_earthquakes(self):
    """Periodic task to check for new earthquakes and send notifications"""
    logger.info("🔍 Checking for new earthquake bulletins...")
    
    try:
        bulletin_data = fetch_latest_earthquake_raw()
        
        if not bulletin_data:
            logger.warning("No bulletin data retrieved")
            return "No data available"
        
        event_id = f"{bulletin_data['date_time']}_{bulletin_data['location']}"
        
        existing_event = SeismicEvent.query.filter_by(event_identifier=event_id).first()
        
        if existing_event and existing_event.has_been_processed:
            logger.info(f"Event {event_id} already processed")
            return "Already processed"
        
        magnitude = LocationAnalyzer.parse_magnitude(bulletin_data['magnitude'])
        
        if magnitude < 3.0:
            logger.info(f"Magnitude {magnitude} below minimum threshold")
            return f"Magnitude {magnitude} too low"
        
        logger.info(f"⚠️ Significant event detected: Magnitude {magnitude}")
        
        lat, lon = LocationAnalyzer.parse_coordinates(
            bulletin_data['latitude'],
            bulletin_data['longitude']
        )
        
        try:
            dt_string = bulletin_data['date_time'].replace(' - ', ' ').replace(' PST', '')
            event_time = datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")
        except:
            event_time = datetime.now()
        
        if not existing_event:
            depth = LocationAnalyzer.parse_magnitude(bulletin_data['depth'])
            new_event = SeismicEvent(
                event_identifier=event_id,
                event_magnitude=magnitude,
                event_location=bulletin_data['location'],
                latitude_coord=lat,
                longitude_coord=lon,
                depth_km=depth,
                occurred_at=event_time,
                has_been_processed=False
            )
            database.session.add(new_event)
            database.session.commit()
            current_event = new_event
        else:
            current_event = existing_event
        
        # Process notifications with Flask app config
        notifications_sent = process_notifications(
            current_event, 
            bulletin_data, 
            (lat, lon), 
            magnitude,
            current_app.config['GEMINI_API_KEY']
        )
        
        current_event.has_been_processed = True
        database.session.commit()
        
        result = f"✅ Event {event_id} processed: {notifications_sent} notifications sent"
        logger.info(result)
        return result
    
    except Exception as error:
        logger.error(f"❌ Error in monitoring task: {error}", exc_info=True)
        database.session.rollback()
        raise self.retry(exc=error, countdown=60)


def process_notifications(event, bulletin_data, quake_coords, magnitude, gemini_api_key):
    """Process and send notifications to affected users"""
    
    all_users = User.query.filter_by(is_active=True).all()
    sent_count = 0
    
    summarizer = GeminiSummarizer(gemini_api_key)
    impact_radius = LocationAnalyzer.calculate_affected_radius(magnitude)
    
    for user in all_users:
        settings = NotificationSettings.query.filter_by(user_id=user.id).first()
        
        if not settings:
            continue
        
        if magnitude < settings.magnitude_threshold:
            continue
        
        if settings.monitor_location_type == 'near_me':
            check_province = user.user_province
            check_city = user.user_city
        else:
            check_province = settings.alternate_province
            check_city = settings.alternate_city
        
        user_radius = min(impact_radius, settings.proximity_range_km)
        
        is_affected = LocationAnalyzer.is_location_affected(
            check_province,
            check_city,
            quake_coords,
            user_radius
        )
        
        if is_affected:
            if send_user_notification(user, settings, bulletin_data, summarizer):
                sent_count += 1
    
    return sent_count


def send_user_notification(user, settings, bulletin_data, summarizer):
    """Send earthquake notification email to user"""
    try:
        summary = summarizer.create_summary(bulletin_data, settings.add_safety_tips)
        
        subject = f"🚨 Earthquake Alert - Magnitude {bulletin_data['magnitude']}"
        
        body = f"""🚨 EARTHQUAKE NOTIFICATION 🚨

Dear {user.full_name},

{summary}

---
EARTHQUAKE DETAILS:
• Time: {bulletin_data['date_time']}
• Location: {bulletin_data['location']}
• Magnitude: {bulletin_data['magnitude']}
• Depth: {bulletin_data['depth']}
• Coordinates: {bulletin_data['latitude']}, {bulletin_data['longitude']}

Your monitored location: {user.user_city}, {user.user_province}
Full bulletin: {bulletin_data.get('detail_link', 'N/A')}

---
This is an automated notification from the Earthquake Monitoring System.
You can update your preferences in your dashboard.

Stay safe!"""

        email_msg = Message(
            subject=subject,
            recipients=[user.email_address],
            body=body
        )
        email_service.send(email_msg)
        
        logger.info(f"✅ Notification sent to {user.email_address}")
        return True
    except Exception as error:
        logger.error(f"❌ Failed to send email to {user.email_address}: {error}")
        return False