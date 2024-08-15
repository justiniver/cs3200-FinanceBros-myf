from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

experiencedTrader = Blueprint('experiencedTrader', __name__)

# GET /notifications
# [Alex-1]
@experiencedTrader.route('/notifications/<user_id>', methods=['GET'])
def get_all_notifications(user_id):
    current_app.logger.info('GET /notifications{user_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT *\
                   FROM userNotifications un join notifications n on un.user_id = n.user_id\
                   WHERE un.user_id = %s', (user_id,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# POST /notifications
# [Alex-1]
@experiencedTrader.route('/create-notifications', methods=['POST'])
def create_notification():
    current_app.logger.info('POST /notifications route')
    # Get JSON data from the request
    data = request.get_json()
    # Validate required fields
    if 'text' not in data or 'user_id' not in data:
        return jsonify({'error': 'Missing required data'}), 400
    cursor = db.get_db().cursor()
    # Manually generate the next notification_id
    cursor.execute('SELECT COALESCE(MAX(notification_id), 0) + 1 FROM notifications')
    next_notification_id = cursor.fetchone()[0]
    # Insert the new notification with the manually generated ID
    cursor.execute(
        'INSERT INTO notifications (notification_id, text, user_id) '
        'VALUES (%s, %s, %s)',
        (next_notification_id, data['text'], 1964)
    )
    # Commit the transaction
    db.get_db().commit()
    return jsonify({'message': 'Notification created successfully'}), 201



# POST /notifications/{id}
# This should be fixed to /notifications from /notifications/{id}
@experiencedTrader.route('/notifications/<int:notification_id>', methods=['POST'])
def update_notification(text, user_id, notification_id):
    current_app.logger.info(f'PUT /notifications/{notification_id} route')
    data = request.get_json()
    cursor = db.get_db().cursor()
    cursor.execute(
        'UPDATE notifications SET text = %s WHERE notification_id = %s AND user_id = %s',
        (text, user_id,)
    )
    db.get_db().commit()
    return jsonify({'message': 'Notification updated successfully'}), 200

# GET /follows
# [Alex-4]
@experiencedTrader.route('/follows/<user_id>', methods=['GET'])
def get_all_followers(user_id):
    current_app.logger.info('GET /follows{user_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT follower_id\
                    FROM follows\
                    WHERE following_id = %s', (user_id,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# GET /users/{id}
# [Alex-4]
@experiencedTrader.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    current_app.logger.info(f'GET /users/{user_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * from users WHERE user_id = %s', (user_id,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# PUT /users/{id}
# [Alex-3]
@experiencedTrader.route('/update-users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    current_app.logger.info(f'PUT /users/{user_id} route')
    data = request.get_json()
    cursor = db.get_db().cursor()
    cursor.execute(
        'UPDATE users SET bio = %s WHERE user_id = %s',
        (data['bio'], user_id)
    )
    db.get_db().commit()
    return jsonify({'message': 'User updated successfully'}), 200

# GET /stocks
# [Alex-1]
@experiencedTrader.route('/stocks-in-portfolio/<portoflio_id>', methods=['GET'])
def get_all_stocks_in_portfolio(portoflio_id):
    current_app.logger.info('GET /personalPortfolio{portfolio_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM personalPortfolio WHERE portfolio_id = %s', (portoflio_id,))
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# POST /users

@experiencedTrader.route('/follow', methods=['POST'])
def follow_user():
    data = request.json
    follower_id = data.get('follower_id') 
    following_id = data.get('following_id')
    current_app.logger.info(f'POST /follow route - Follower ID: {follower_id}, Following ID: {following_id}')
    cursor = db.get_db().cursor()
    cursor.execute('''
        INSERT INTO follows (follower_id, following_id, timestamp, count, user_id)
        VALUES (%s, %s, CURRENT_TIMESTAMP, %s, %s)
    ''', (follower_id, following_id, follower_id))
    db.get_db().commit()
    the_response = make_response({'message': 'User followed successfully'})
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# DELETE /users

@experiencedTrader.route('/unfollow', methods=['DELETE'])
def unfollow_user():
    data = request.json
    follower_id = data.get('follower_id') 
    following_id = data.get('following_id')  
    current_app.logger.info(f'DELETE /unfollow route - Follower ID: {follower_id}, Following ID: {following_id}')
    cursor = db.get_db().cursor()
    cursor.execute('''
        DELETE FROM follows
        WHERE follower_id = %s AND following_id = %s
    ''', (follower_id, following_id))
    db.get_db().commit()
    the_response = make_response({'message': 'User unfollowed successfully'})
    the_response.status_code = 200 
    the_response.mimetype = 'application/json'
    return the_response


