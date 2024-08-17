from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

experiencedTrader = Blueprint('experiencedTrader', __name__)

# GET /notifications
# [Alex-1]
# This function returns the notifications that a verified user posts that this specified user follows
@experiencedTrader.route('/user_notifications/<user_id>', methods=['GET'])
def get_user_notifications(user_id):
    current_app.logger.info('GET /notifications{user_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT DISTINCT n.user_id, n.timeCreated, n.text, n.likes\
                   FROM userNotifications un join notifications n on un.user_id = n.user_id\
                   WHERE un.user_id = %s', (user_id,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# POST /follow{id}
# [Alex ADDED]
# This function allows the verified user to follow other verfied users.
@experiencedTrader.route('/follow/<int:user_id>/<int:following_id>', methods=['POST'])
def follow_user_verified(user_id, following_id):
    current_app.logger.info(f'POST /follow/{user_id}/{following_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('INSERT INTO follows (follower_id, following_id) VALUES (%s, %s)', (user_id, following_id))
    response = make_response({'message': f'User {user_id} followed {following_id} successfully'})
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

# GET /follows
# [Alex-4]
# This functions allows the verfied users to see all usernames that follow them
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

# GET /portfolios/{user_id}
# [Alex ADDED]
# Displays their specific portfolios data
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

# GET /portfolios/{user_id}
# [Alex ADDED]
# Displays their specific stocks within their portfolio
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
# [Alex-ADDED]
# This functions allows the user to follow other verified people
@experiencedTrader.route('/follow/<int:user_id>/<int:following_id>', methods=['POST'])
def follow_user(user_id, following_id):
    current_app.logger.info(f'POST /follow/{user_id}/{following_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('INSERT INTO follows (follower_id, following_id) VALUES (%s, %s)', (user_id, following_id))
    response = make_response({'message': f'User {user_id} followed {following_id} successfully'})
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

# GET /public_profile/{user_id}
# [Alex_1]
# This function allows the verified user to see public profiles of other users by user_id
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

# PUT /updateProfile
# [Alex-4]
# This function updates the users profile biography.
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

        
        return jsonify({'message': 'Bio updated successfully'}), 200

    except Exception as e:
        current_app.logger.error(f"Error updating bio for user {user_id}: {str(e)}")
        return jsonify({'error': 'Failed to update user bio'}), 500

# PUT /updateProfile
# [Alex-4]
# This function updates the users profile username
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

# PUT /updateProfile
# [Alex-4]
# This function updates the users profile picture
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
    
# Post /notifications
# [Alex-1]
# This functions allows the verified user to create notifications
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
    
# Get /notifications/<user_id>
# [Alex ADDED]
# This function returns all of their previous written notifcations.
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

# DELETE /notifications/{notif_id}
# [Alex-1]
# This function allows the user to delete a notication they created by notification_id
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

# PUT /notifications/{notif_id}
# [Alex-1]
# This function allows the user to update a notication they created by notification_id
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

# GET /recStocks
# [Alex-ADDED]
# Returns top 5 rec. stocks that the stock has the lowest beta of all stocks.
@experiencedTrader.route('/recstocks', methods=['GET'])
def get_all_stocks():
    current_app.logger.info('GET /stocks route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM stock')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response