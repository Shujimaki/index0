#!/bin/bash
# Setup script for Index0 Earthquake Monitoring System

echo "🚀 Setting up Index0 Earthquake Monitoring System..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  WARNING: .env file not found!"
    echo "Please ensure you have a .env file with the following variables:"
    echo "  - GEMINI_API_KEY"
    echo "  - MAIL_USERNAME"
    echo "  - MAIL_PASSWORD"
    echo "  - MAIL_DEFAULT_SENDER"
    echo "  - REDIS_URL"
fi

# Initialize database if migrations folder doesn't exist
if [ ! -d "migrations" ]; then
    echo "🗄️  Initializing database..."
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
else
    echo "🗄️  Running database migrations..."
    flask db migrate -m "Update schema"
    flask db upgrade
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 To run the application:"
echo "   Terminal 1: python run.py"
echo "   Terminal 2: celery -A celery_worker.task_queue worker --loglevel=info"
echo "   Terminal 3: celery -A celery_worker.task_queue beat --loglevel=info"
echo ""
echo "🌐 Open http://localhost:5001 in your browser"
echo ""
