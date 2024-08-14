from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

dataAnalyst = Blueprint('dataAnalyst', __name__)


@dataAnalyst.route('/dataAnalyst', methods=['GET'])
def get_all_dataAnalyst():
    current_app.logger.info('GET /dataAnalyst route')
    cursor = db.get_db().cursor()
    # the_query = '''
    # SELECT * 
    # FROM stock
    # '''
    cursor.execute('select * from stock')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# User story 1
@dataAnalyst.route('/user-metrics/<user_id>/metrics', methods=['GET'])
def get_user_metrics(user_id):
    current_app.logger.info('GET /user-metrics/{user_id}/metrics route')
    cursor = db.get_db().cursor()
    x = tuple(user_id)
    cursor.execute('SELECT * FROM users WHERE user_id = %s', int(user_id,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# User story 2
@dataAnalyst.route('/user-metrics/<user_id>/notifications-follows', methods=['GET'])
def get_user_metrics_notifications_follows(user_id):
    current_app.logger.info('GET /user-metrics/{user_id}/notifications-follows route')
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT * 
        FROM userMetrics um
        JOIN notifications n ON um.user_id = n.user_id
        JOIN follows f ON f.following_id = n.user_id
        WHERE um.user_id = ?
        ORDER BY likes, timeCreated
    ''', (user_id,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@dataAnalyst.route('/personal-portfolio/high-value', methods=['GET'])
def get_high_value_portfolios():
    current_app.logger.info('GET /personal-portfolio/high-value route')
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT *
        FROM personalPortfolio
        WHERE liquidated_Value > 20000 AND P_L >= (liquidated_Value * 0.15)
        ORDER BY P_L DESC
    ''')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@dataAnalyst.route('/users/<int:user_id>/ban', methods=['PUT'])
def ban_user(user_id):
    current_app.logger.info(f'PUT /users/{user_id}/ban route')
    cursor = db.get_db().cursor()
    cursor.execute('UPDATE users SET banned = true WHERE user_id = ?', (user_id,))
    db.get_db().commit()
    the_response = make_response({'message': 'User banned successfully'})
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
