from app import app,db
from app.models import User, gameRecord
@app.route('/users', methods=['POST'])
def create_game():
    pass

@app.route('/users/<int:id>', methods=['PUT'])
def update_game(id):
    pass