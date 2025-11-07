from flask import Blueprint, request, jsonify, render_template, current_app, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request, get_jwt
from . import db
from .models import User, Course, Quiz
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

bp = Blueprint('routes', __name__)

# simple prometheus counter
REQUEST_COUNT = Counter('elearn_requests_total', 'Total HTTP requests')


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    data = request.get_json() or request.form
    username = data.get('username')
    password = data.get('password')
    role = (data.get('role') or 'student').lower()
    if not username or not password:
        return jsonify({'msg': 'username and password required'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'msg': 'user exists'}), 400

    # disallow creating admin via public registration
    if role == 'admin':
        return jsonify({'msg': 'creating admin via registration is not allowed'}), 403

    user = User(username=username, password=generate_password_hash(password), role=role)
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': 'registered', 'user': user.to_dict()}), 201


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    data = request.get_json() or request.form
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'msg': 'bad creds'}), 401

    # create token with identity as string id and role in additional claims
    token = create_access_token(identity=str(user.id), additional_claims={'username': user.username, 'role': user.role})
    return jsonify({'access_token': token, 'user': user.to_dict()})


@bp.route('/courses', methods=['GET', 'POST'])
def courses():
    REQUEST_COUNT.inc()
    # GET request: check Accept header to serve HTML or JSON
    if request.method == 'GET':
        # If Accept header includes text/html, serve the courses page template
        if 'text/html' in request.headers.get('Accept', ''):
            return render_template('courses.html')
        # Otherwise return JSON (API)
        cs = Course.query.all()
        return jsonify([c.to_dict() for c in cs])

    data = request.get_json() or {}
    title = data.get('title')
    desc = data.get('description')
    if not title:
        return jsonify({'msg': 'title required'}), 400
    # require authenticated teacher or admin to create courses
    try:
        verify_jwt_in_request()
    except Exception:
        return jsonify({'msg': 'authentication required to create course'}), 401

    claims = get_jwt() or {}
    role = claims.get('role')
    if role not in ('teacher', 'admin'):
        return jsonify({'msg': 'only teacher or admin can create courses'}), 403

    course = Course(title=title, description=desc)
    db.session.add(course)
    db.session.commit()
    return jsonify({'msg': 'created', 'course': course.to_dict()}), 201


@bp.route('/quiz/<int:course_id>', methods=['GET', 'POST'])
@jwt_required(optional=True)
def quiz(course_id):
    if request.method == 'GET':
        qs = Quiz.query.filter_by(course_id=course_id).all()
        return jsonify([q.to_dict() for q in qs])

    identity = get_jwt_identity()
    if not identity:
        return jsonify({'msg': 'login required to submit quiz'}), 401

    data = request.get_json() or {}
    question = data.get('question')
    answer = data.get('answer')
    if not question or not answer:
        return jsonify({'msg': 'question and answer required'}), 400
    q = Quiz(course_id=course_id, question=question, answer=answer)
    db.session.add(q)
    db.session.commit()
    return jsonify({'msg': 'quiz saved', 'quiz': q.to_dict()}), 201


@bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    # render profile page for authenticated user
    identity = get_jwt_identity()
    claims = get_jwt() or {}
    user_data = {
        'id': identity,
        'username': claims.get('username'),
        'role': claims.get('role')
    }
    return render_template('profile.html', user=user_data)


@bp.route('/api/profile', methods=['GET'])
@jwt_required()
def api_profile():
    # JSON endpoint for profile (used by client-side redirects)
    identity = get_jwt_identity()
    claims = get_jwt() or {}
    user_data = {
        'id': identity,
        'username': claims.get('username'),
        'role': claims.get('role')
    }
    return jsonify(user_data), 200


@bp.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}
    return render_template('profile.html', user_id=identity, username=username, role=role)
