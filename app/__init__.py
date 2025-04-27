from flask import Flask, jsonify
from sqlalchemy import text
from .db.init_db import init_db

def create_app():
    app = Flask(__name__)

    # Initialize database
    Session = init_db()

    @app.route('/health')
    def health_check():
        try:
            # Test database connection
            session = Session()
            session.execute(text('SELECT 1'))
            session.commit()
            return jsonify({'status': 'healthy', 'database': 'connected'}), 200
        except Exception as e:
            return jsonify({'status': 'unhealthy', 'database': str(e)}), 500
        finally:
            session.close()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        Session.remove()

    return app 