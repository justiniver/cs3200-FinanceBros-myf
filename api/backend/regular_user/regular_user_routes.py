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

@user.route('/users/<username>', methods=['GET'])
def get_username_by_id(username):
    current_app.logger.info(f'GET /users/{username} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT user_id FROM users WHERE username = %s', (username,))
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
    cursor.execute('SELECT username FROM users WHERE verified = True')
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
@user.route('/influencers/<username>', methods=['GET'])
def get_influencer_by_username(username):
    current_app.logger.info(f'GET /influencers/{username} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT verified_username, biography, photo_url\
                    FROM verifiedPublicProfile WHERE verified_username = %s', (username,))
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

# # POST /portfolios/{id}
# # CHANGE THIS TO INSERTING STOCKS IN USER PORTFOLIO
# # [Emily-1]
# @user.route('/portfolios/<int:user_id>', methods=['POST'])
# def create_portfolio(user_id, portfolio_id):
#     current_app.logger.info(f'POST /portfolios/{user_id} route')
#     data = request.get_json()
#     cursor = db.get_db().cursor()
#     cursor.execute('INSERT INTO personalPortfolio (user_id, portoflio_id) VALUES (%s, %s)', 
#                    (user_id, portfolio_id))
#     db.get_db().commit()
#     the_response = make_response({'message': 'Portfolio created successfully'})
#     the_response.status_code = 200
#     the_response.mimetype = 'application/json'
#     return the_response


# GET /myportfolios
@user.route('/myportfolios/<int:user_id>', methods=['GET'])
def get_my_portfolios(user_id):
    current_app.logger.info(f'GET /personalPortfolio/{user_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT P_L, liquidated_Value, beta FROM personalPortfolio WHERE user_id = %s', (user_id,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@user.route('/portfolios_stock/<int:user_id>', methods=['GET'])
def get_portfolios_userID(user_id):
    current_app.logger.info(f'GET /personalPortfolio/{user_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT s.ticker, s.sharePrice, s.stockName, s.beta FROM users u JOIN personalPortfolio ps ON u.user_id = ps.user_id JOIN portfolioStocks p ON ps.portfolio_id = p.portfolio_id JOIN stock s ON s.ticker = p.ticker WHERE u.user_id = %s', (user_id,))
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

@user.route('/recStocks', methods=['GET'])
def recStocks():
    current_app.logger.info('GET /stocks route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM stock ORDER BY beta LIMIT 5')
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

# GET notifications/{user_id}
@user.route('/notifications/<int:user_id>', methods=['GET'])
def get_notifications_for_user(user_id):
    current_app.logger.info(f'GET /notifications/{user_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM notifications WHERE user_id = %s', (user_id,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


@user.route('/follow/<int:user_id>/<int:following_id>', methods=['POST'])
def follow_user(user_id, following_id):
    current_app.logger.info(f'POST /follow/{user_id}/{following_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('INSERT INTO follows (follower_id, following_id) VALUES (%s, %s)', (user_id, following_id))
    response = make_response({'message': f'User {user_id} followed {following_id} successfully'})
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

# GET /ticker
# [Emily-2]
@user.route('/getTicker', methods=['GET'])
def get_all_ticker():
    current_app.logger.info('GET /getTicker route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT ticker FROM stock')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@user.route('/addStockToPortfolio/<int:portfolio_id>/<string:ticker>', methods=['POST'])
def addStock(portfolio_id, ticker):
    current_app.logger.info(f'POST /addStock route for portfolio_id: {portfolio_id} and ticker: {ticker}')
    cursor = db.get_db().cursor()
    cursor.execute('INSERT INTO portfolioStocks (portfolio_id, ticker) VALUES (%s, %s)', (portfolio_id, ticker))
    db.get_db().commit()
    response = make_response({'message': f'You added {ticker} to portfolio {portfolio_id}!'})
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

@user.route('/getUserPortfolio/<int:user_id>', methods=['GET'])
def get__user_portfolios(user_id):
    current_app.logger.info(f'GET /personalPortfolio/{user_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT portfolio_id FROM personalPortfolio WHERE user_id = %s', (user_id,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response