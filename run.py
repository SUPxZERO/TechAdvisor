from app import create_app, db
import os

# Create Flask application instance
app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    # Run the application
    app.run(
        host='0.0.0.0',
        port=5001,  # Changed to 5001 to avoid Windows port 5000 restrictions
        debug=app.config['DEBUG']
    )
