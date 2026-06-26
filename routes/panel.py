from flask import Blueprint
from controllers.panel_controller import PanelController
from controllers.auth_controller import role_required

panel_bp = Blueprint('panel', __name__)


@panel_bp.route('/panel', methods=['GET', 'POST'])
@role_required('admin')
def index():
    return PanelController.index()
