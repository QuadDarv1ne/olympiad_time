from flask import render_template
from flask_login import login_required, current_user

def init_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/profile')
    @login_required
    def profile():
        return render_template('profile.html', username=current_user.username)
