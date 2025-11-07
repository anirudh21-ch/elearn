from . import create_app, db
import os
from .models import User, Course, Quiz
from werkzeug.security import generate_password_hash

app = create_app()


def create_tables():
    # Flask 3.x removed `before_first_request`; create DB tables explicitly at startup
    with app.app_context():
        db.create_all()
        # ensure there is an admin user
        admin_user = User.query.filter_by(username=os.environ.get('ADMIN_USERNAME', 'admin')).first()
        if not admin_user:
            admin_pass = os.environ.get('ADMIN_PASSWORD', 'admin')
            u = User(username=os.environ.get('ADMIN_USERNAME', 'admin'), password=generate_password_hash(admin_pass), role='admin')
            db.session.add(u)
            db.session.commit()


if __name__ == '__main__':
    create_tables()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
