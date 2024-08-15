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
def create_notification(data):
    current_app.logger.info('POST /notifications route')
    data = request.get_json()
    cursor = db.get_db().cursor()
    cursor.execute(
        'INSERT INTO notifications (notification_id, text, likes, user_id) '
        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
        (data['notification_id'], data['text'], data['likes'], data['user_id'])
    )
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
@experiencedTrader.route('/followers/<verified_user_id>', methods=['GET'])
def get_all_followers(verified_user_id):
    current_app.logger.info('GET /followers route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT u.username\
                    FROM follows f join users u on f.follower_id = u.user_id\
                   WHERE following_id = %s', (verified_user_id,))
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
        'UPDATE  SET bio = %s WHERE user_id = %s',
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


@experiencedTrader.route('/public_profile/<user_id>', methods=['GET'])
def get_public_profile(user_id):
    current_app.logger.info('GET /public_profile{user_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT biography, verified_username, photo_url FROM verifiedPublicProfile WHERE user_id = %s', (user_id,))
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@experiencedTrader.route('/update-bio/<int:user_id>/<update_bio>', methods=['PUT'])
def update_bio(user_id, update_bio):
    current_app.logger.info(f'PUT /update-bio/{user_id}/{update_bio} route')

    try:
        cursor = db.get_db().cursor()
        cursor.execute(
            'UPDATE verifiedPublicProfile SET biography = %s WHERE user_id = %s',
            (update_bio, user_id)
        )
        db.get_db().commit()

        # Return a success message with status code 200
        return jsonify({'message': 'Bio updated successfully'}), 200

    except Exception as e:
        current_app.logger.error(f"Error updating bio for user {user_id}: {str(e)}")
        return jsonify({'error': 'Failed to update user bio'}), 500

@experiencedTrader.route('/update-username/<int:user_id>/<update_username>', methods=['PUT'])
def update_username(user_id, update_username):
    current_app.logger.info(f'PUT /update-bio/{user_id}/{update_username} route')

    try:
        cursor = db.get_db().cursor()
        cursor.execute(
            'UPDATE verifiedPublicProfile SET verified_username = %s WHERE user_id = %s',
            (update_username, user_id)
        )
        db.get_db().commit()

        # Return a success message with status code 200
        return jsonify({'message': 'Username updated successfully'}), 200

    except Exception as e:
        current_app.logger.error(f"Error updating bio for user {user_id}: {str(e)}")
        return jsonify({'error': 'Failed to update user bio'}), 500


@experiencedTrader.route('/update-photo/<int:user_id>/<update_photo>', methods=['PUT'])
def update_photo(user_id, update_photo):
    current_app.logger.info(f'PUT /update-bio/{user_id}/{update_photo} route')

    try:
        cursor = db.get_db().cursor()
        cursor.execute(
            'UPDATE verifiedPublicProfile SET photo_url = %s WHERE user_id = %s',
            (update_photo, user_id)
        )
        db.get_db().commit()

        # Return a success message with status code 200
        return jsonify({'message': 'Profile photo updated successfully'}), 200

    except Exception as e:
        current_app.logger.error(f"Error updating bio for user {user_id}: {str(e)}")
        return jsonify({'error': 'Failed to update user bio'}), 500