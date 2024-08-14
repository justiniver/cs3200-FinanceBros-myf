
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

user = Blueprint('user', __name__)


# GET /users
# [Emily-1]
@user.route('/users', methods=['GET'])
def get_all_users():
    current_app.logger.info('GET /users route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM users')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# POST /users
# [Emily-1]
@user.route('/users/create', methods=['POST'])
def create_user(data):
    current_app.logger.info('POST /users route')
    data = request.get_json()
    cursor = db.get_db().cursor()
    cursor.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)', 
                   (data['username'], data['email'], data['password']))
    db.get_db().commit()
    the_response = make_response({'message': 'User created successfully'})
    the_response.status_code = 201
    the_response.mimetype = 'application/json'
    return the_response

# GET /users/{id}
# [Emily-2]
@user.route('/users/<int:user_id>', methods=['GET'])
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
# [Emily-4]
@user.route('/influencers', methods=['GET'])
def get_all_influencers():
    current_app.logger.info('GET /influencers route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM users WHERE verified = True')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# POST /influencers/{id}/notifications
# [Emily-4]
@user.route('/influencers/<int:influencer_id>/notifications', methods=['POST'])
def create_influencer_notification(influencer_id, message):
    current_app.logger.info(f'POST /influencers/{influencer_id}/notifications route')
    data = request.get_json()
    cursor = db.get_db().cursor()
    cursor.execute('INSERT INTO notifications (influencer_id, message) VALUES (%s, %s)', 
                   (influencer_id, message,))
    db.get_db().commit()
    the_response = make_response({'message': 'Notification created successfully'})
    the_response.status_code = 201
    the_response.mimetype = 'application/json'
    return the_response

# GET /influencers/{id}
# [Emily-4]
@user.route('/influencers/<int:influencer_id>', methods=['GET'])
def get_influencer_by_id(influencer_id):
    current_app.logger.info(f'GET /influencers/{influencer_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM erifiedPublicProfile WHERE verified_user_id = %s', (influencer_id,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# GET /portfolios
# [Emily-2]
@user.route('/portfolios', methods=['GET'])
def get_all_portfolios():
    current_app.logger.info('GET /portfolios route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM personalPortfolio')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# POST /portfolios/{id}
# [Emily-1]
@user.route('/portfolios/<int:user_id>', methods=['POST'])
def create_portfolio(user_id, portfolio_id):
    current_app.logger.info(f'POST /portfolios/{user_id} route')
    data = request.get_json()
    cursor = db.get_db().cursor()
    cursor.execute('INSERT INTO personalPortfolios (user_id, portoflio_id) VALUES (%s, %s)', 
                   (user_id, portfolio_id))
    db.get_db().commit()
    the_response = make_response({'message': 'Portfolio created successfully'})
    the_response.status_code = 201
    the_response.mimetype = 'application/json'
    return the_response

@user.route('/portfolios_stock/<int:user_id>', methods=['POST'])
def get_portfolio_stocks(user_id):
        current_app.logger.info(f'POST /portfolios_stock/{user_id} route')
        data = request.get_json()
        cursor = db.get_db().cursor()
        cursor.execute('Select portS.ticker, s.sharePrice, s.stockName, s.beta\
                        from users u JOIN personalPortfolio ps on u.user_id = ps.user_id\
                        JOIN portfolioStocks portS ON ps.portfolio_id = portS.portfolio_id\
                        JOIN stock s ON s.ticker = portS.ticker')
        db.get_db().commit()
        the_response = make_response()
        the_response.status_code = 201
        the_response.mimetype = 'application/json'
        return the_response

# GET /portfolios/{id}
# [Emily-2]
@user.route('/portfolios/<int:portfolio_id>', methods=['GET'])
def get_portfolio_by_id(portfolio_id):
    current_app.logger.info(f'GET /portfolios/{portfolio_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM personalPortfolios WHERE portfolio_id = %s', (portfolio_id,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# GET /stocks
# [Emily-2]
@user.route('/stocks', methods=['GET'])
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
# [Emily-2]
@user.route('/stocks/<int:stock_id>', methods=['GET'])
def get_stock_by_ticker(ticker):
    current_app.logger.info(f'GET /stock/{ticker} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM stock WHERE ticker = %s', (ticker,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# GET /notifications
# [Emily-3]
@user.route('/notifications', methods=['GET'])
def get_all_notifications():
    current_app.logger.info('GET /notifications route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM notifications')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
