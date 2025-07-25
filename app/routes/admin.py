from flask import Blueprint, render_template
from app.utils.jwt_utils import token_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@token_required
def dashboard():
    return render_template('admin/dashboard.html')