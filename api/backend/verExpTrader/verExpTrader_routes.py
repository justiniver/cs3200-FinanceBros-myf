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

# GET /myportfolios
@experiencedTrader.route('/myportfolios/<int:user_id>', methods=['GET'])
def get_my_portfolios(user_id):
    current_app.logger.info(f'GET /personalPortfolio/{user_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT P_L, liquidated_Value, beta FROM personalPortfolio WHERE user_id = %s', (user_id,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@experiencedTrader.route('/portfolios_stock/<int:user_id>', methods=['GET'])
def get_portfolios_userID(user_id):
    current_app.logger.info(f'GET /personalPortfolio/{user_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT s.ticker, s.sharePrice, s.stockName, s.beta FROM users u JOIN personalPortfolio ps ON u.user_id = ps.user_id JOIN portfolioStocks p ON ps.portfolio_id = p.portfolio_id JOIN stock s ON s.ticker = p.ticker WHERE u.user_id = %s', (user_id,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
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
    


@experiencedTrader.route('/create-notifications/<text>', methods=['POST'])
def create_notifications(text):
    current_app.logger.info(f'POST /create-notifications{text} route')

    try:
        cursor = db.get_db().cursor()
        cursor.execute(
            'INSERT INTO notifications(text, user_id) VALUES (%s, 1964)', (text,))
        db.get_db().commit()

        # Return a success message with status code 200
        return jsonify({'message': 'Notification created successfully'}), 200

    except Exception as e:
        current_app.logger.error(f"Error creating notification: {str(e)}")
        return jsonify({'error': 'Failed to create notification'}), 500
    
@experiencedTrader.route('/get_notifications/<user_id>', methods=['GET'])
def get_all_written_notifications(user_id):
    current_app.logger.info('GET /notifications{user_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT *\
                   FROM notifications\
                   WHERE user_id = %s', (user_id,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@experiencedTrader.route('/delete_notifications/<notif_id>', methods=['DELETE'])
def delete_written_notifications(notif_id):
    current_app.logger.info(f'DELETE /notifications/{notif_id} route')
    
    try:
        with db.get_db().cursor() as cursor:
            cursor.execute('DELETE FROM notifications WHERE notification_id = %s', (notif_id,))
            db.get_db().commit()

        return jsonify({'message': 'Notification deleted successfully'}), 200

    except Exception as e:
        current_app.logger.error(f"Error deleting notification: {str(e)}")
        return jsonify({'error': 'Failed to delete notification'}), 500

@experiencedTrader.route('/update_notifications/<notif_id>/<message>', methods=['PUT'])
def update_written_notifications(notif_id, message):
    current_app.logger.info(f'PUT /update_notifications/{notif_id} with message: {message}')
    
    try:
        with db.get_db().cursor() as cursor:
            cursor.execute('UPDATE notifications SET text = %s WHERE notification_id = %s', (message, notif_id))
            db.get_db().commit()

        return jsonify({'message': 'Notification updated successfully'}), 200

    except Exception as e:
        current_app.logger.error(f"Error updating notification: {str(e)}")
        return jsonify({'error': 'Failed to update notification'}), 500