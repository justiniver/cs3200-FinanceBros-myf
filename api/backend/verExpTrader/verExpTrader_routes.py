# from flask import Blueprint, request, jsonify, make_response, current_app
# from backend.db_connection import db

# experienced_trader = Blueprint('experienced_trader', __name__)

# # Route to view the number of followers (GET)
# @experienced_trader.route('/followers/count/<int:user_id>', methods=['GET'])
# def get_follower_count(user_id):
#     current_app.logger.info(f'GET /followers/count/{user_id} route')
#     cursor = db.get_db().cursor()
#     cursor.execute('SELECT COUNT(*) as follower_count FROM follows WHERE following_id = %s', (user_id,))
    
#     follower_count = cursor.fetchone()[0]
#     the_response = make_response(jsonify({'follower_count': follower_count}))
#     the_response.status_code = 200
#     the_response.mimetype = 'application/json'
#     return the_response
