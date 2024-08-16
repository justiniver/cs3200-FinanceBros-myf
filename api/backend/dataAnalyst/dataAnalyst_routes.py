
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

dataAnalyst = Blueprint('dataAnalyst', __name__)


# GET /user

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


# GET /influencers/{id}

@dataAnalyst.route('/influencers/<verified_user_id>', methods=['GET'])
def get_influencer_by_id(verified_user_id):
    current_app.logger.info(f'GET /influencers/{verified_user_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM verifiedPublicProfile WHERE verified_user_id = %s', (verified_user_id,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# GET /portfolios

@dataAnalyst.route('/portfolios', methods=['GET'])
def get_all_portfolios():
    current_app.logger.info('GET /portfolios route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM personalPortfolio')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# GET /portfolios/{id}

@dataAnalyst.route('/portfolios/<portfolio_id>', methods=['GET'])
def get_portfolio_by_id(portfolio_id):
    current_app.logger.info(f'GET /portfolios/{portfolio_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM personalPortfolio WHERE portfolio_id = %s', (portfolio_id,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# GET /stocks

@dataAnalyst.route('/stocks', methods=['GET'])
def get_all_stocks():
    current_app.logger.info('GET /stocks route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM stock')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response



# GET /stocks/{id}

@dataAnalyst.route('/stocks/<ticker>', methods=['GET'])
def get_stock_by_id(ticker):
    current_app.logger.info(f'GET /stock/{ticker} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM stock WHERE ticker = %s', (ticker,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# GET /notifications

@dataAnalyst.route('/notifications', methods=['GET'])
def get_all_notifications():
    current_app.logger.info('GET /notifications route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM notifications')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# GET /notifications/{id}

@dataAnalyst.route('/notifications/<notification_id>', methods=['GET'])
def get_notification_by_id(notification_id):
    current_app.logger.info('GET /notifications/{notification_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM notifications WHERE notification_id = %s', (notification_id,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

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



# GET user metrics

@dataAnalyst.route('/metrics', methods=['GET'])
def get_all_user_metrics():
    current_app.logger.info('GET /metrics route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM users u JOIN userMetrics um ON u.user_id = um.user_id JOIN personalPortfolio pp ON pp.user_id = n.user_id ORDER BY u.user_id')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response