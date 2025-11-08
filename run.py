from app import build_application
import os

application = build_application(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    application.run(host='0.0.0.0', port=port, debug=True)