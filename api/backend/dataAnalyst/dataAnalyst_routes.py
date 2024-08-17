from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

dataAnalyst = Blueprint('dataAnalyst', __name__)


# GET u/users
# [Sarah-1]
# This function pulls all user data from the users table for the Data Analyst
@dataAnalyst.route('/users', methods=['GET'])
def get_all_users():
    current_app.logger.info('GET /users route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM users')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# GET /users{id}
# [Sarah-3]
# This function returns specific user data given a specific user_id
@dataAnalyst.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    current_app.logger.info(f'GET /users/{user_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = %s', (user_id,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# GET /influencers
# [Sarah-3]
# This function returns the verified private profile of all influencers
@dataAnalyst.route('/influencers', methods=['GET'])
def get_all_influencers():
    current_app.logger.info('GET /influencers route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM verifiedPrivateProfile')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# GET /portfolios{id}
# [Sarah-3]
# This function returns every stock in a specific given users portfolio
@dataAnalyst.route('/myportfolios_stock/<int:user_id>', methods=['GET'])
def get__user_portfolios_userID(user_id):
    current_app.logger.info(f'GET /personalPortfolio/{user_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT s.ticker AS Ticker, s.sharePrice AS sharePrice, s.stockName AS stockName,s.beta AS riskLevel FROM users u JOIN personalPortfolio ps ON u.user_id = ps.user_id JOIN portfolioStocks p ON ps.portfolio_id = p.portfolio_id JOIN stock s ON s.ticker = p.ticker WHERE u.user_id = %s', (user_id,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# PUT /banuser
# [Sarah-4]
# This function bans a user given a specific user_id
@dataAnalyst.route('/banUser/<user_id>', methods=['PUT'])
def ban_user(user_id):
    current_app.logger.info(f'PUT /d/users/{user_id} route')
    try:
        cursor = db.get_db().cursor()
        current_app.logger.info(f"Attempting to ban user with id: {user_id}")
        cursor.execute('UPDATE users SET banned = 1 WHERE user_id = %s', (user_id,))
        db.get_db().commit()
        if cursor.rowcount == 0:
            current_app.logger.info(f"No user found with id {user_id}")
            return jsonify({"error": "User not found"}), 404
        return jsonify({"message": f"User {user_id} has been banned successfully."}), 200   
    except Exception as e:
        current_app.logger.error(f"Error banning user {user_id}: {e}")
        db.get_db().rollback()
        return jsonify({"error": "Failed to ban user"}), 500
    finally:
        cursor.close()

# PUT /unbanuser
# [Sarah-4]
# This function unbans a user given a specific user_id
@dataAnalyst.route('/unbanUser/<user_id>', methods=['PUT'])
def unban_user(user_id):
    current_app.logger.info(f'PUT /d/users/{user_id} route')
    try:
        cursor = db.get_db().cursor()
        current_app.logger.info(f"Attempting to unban user with id: {user_id}")
        cursor.execute('UPDATE users SET banned = 0 WHERE user_id = %s', (user_id,))
        db.get_db().commit()
        if cursor.rowcount == 0:
            current_app.logger.info(f"No user found with id {user_id}")
            return jsonify({"error": "User not found"}), 404
        return jsonify({"message": f"User {user_id} has been unbanned successfully."}), 200
    except Exception as e:
        current_app.logger.error(f"Error unbanning user {user_id}: {e}")
        db.get_db().rollback()
        return jsonify({"error": "Failed to unban user"}), 500    
    finally:
        cursor.close()

# PUT / verifyuser
# [Sarah-4]
# This function verifies a user given a specific user_id
@dataAnalyst.route('/verify/<user_id>', methods=['PUT'])
def verify_user(user_id):
    current_app.logger.info(f'PUT /d/users/{user_id} route')
    try:
        cursor = db.get_db().cursor()
        current_app.logger.info(f"Attempting to verify user with id: {user_id}")
        cursor.execute('UPDATE users SET verified = 1 WHERE user_id = %s', (user_id,))
        db.get_db().commit()
        if cursor.rowcount == 0:
            current_app.logger.info(f"No user found with id {user_id}")
            return jsonify({"error": "User not found"}), 404
        return jsonify({"message": f"User {user_id} has been verified successfully."}), 200   
    except Exception as e:
        current_app.logger.error(f"Error verifying user {user_id}: {e}")
        db.get_db().rollback()
        return jsonify({"error": "Failed to verify user"}), 500
    finally:
        cursor.close()

# PUT / unverifyuser
# [Sarah-4]
# This function verifies a user given a specific user_id
@dataAnalyst.route('/unverify/<user_id>', methods=['PUT'])
def unverify_user(user_id):
    current_app.logger.info(f'PUT /d/users/{user_id} route')
    try:
        cursor = db.get_db().cursor()
        current_app.logger.info(f"Attempting to unverify user with id: {user_id}")
        cursor.execute('UPDATE users SET verified = 0 WHERE user_id = %s', (user_id,))
        db.get_db().commit()
        if cursor.rowcount == 0:
            current_app.logger.info(f"No user found with id {user_id}")
            return jsonify({"error": "User not found"}), 404
        return jsonify({"message": f"User {user_id} has been unverified successfully."}), 200
    except Exception as e:
        current_app.logger.error(f"Error unverifying user {user_id}: {e}")
        db.get_db().rollback()
        return jsonify({"error": "Failed to unverify user"}), 500    
    finally:
        cursor.close()


# GET /metrics
# [Sarah-1]
# This function returns dashboard metrics and notification metrics of a 
# all users
@dataAnalyst.route('/metrics', methods=['GET'])
def get_all_user_metrics():
    current_app.logger.info('GET /metrics route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT u.user_id AS user_id, SSN, f_name AS firstName, l_name AS lastName, password, email, verified, banned, phone, DOB, user_metric_id, dmStartTime, dmEndTime, mStartTime, mEndTime,activeUsers, portfolio_id, beta AS riskLevel, liquidated_Value, P_L AS profitLoss FROM users u JOIN userMetrics um ON u.user_id = um.user_id JOIN personalPortfolio pp ON pp.user_id = u.user_id ORDER BY u.user_id')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# GET /metrics/<user_id>
# [Sarah-1]
# This function returns dashboard metrics and notification metrics of a 
# given specified user
@dataAnalyst.route('/specificmetrics/<user_id>', methods=['GET'])
def get_specific_user_metrics(user_id):
    current_app.logger.info(f'GET /metrics/{user_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT u.user_id AS user_id, SSN, f_name AS firstName, l_name AS lastName, password, email, verified, banned, phone, DOB, user_metric_id, dmStartTime, dmEndTime, mStartTime, mEndTime,activeUsers, portfolio_id, beta AS riskLevel, liquidated_Value, P_L AS profitLoss FROM users u JOIN userMetrics um ON u.user_id = um.user_id JOIN personalPortfolio pp ON pp.user_id = u.user_id WHERE u.user_id = %s ORDER BY u.user_id', (user_id,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


