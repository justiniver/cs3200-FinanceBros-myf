from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

experienced_trader = Blueprint('experienced_trader', __name__)

# User story #1
@experienced_trader.route('/notifications', methods=['POST'])
def send_trade_notifications():
    current_app.logger.info('POST /notifications route')
    notification_data = request.json

    notification_text = notification_data.get('text')
    user_id = notification_data.get('user_id')
    time_created = notification_data.get('timeCreated')

    query = '''INSERT INTO notifications (text, timeCreated, user_id)
               VALUES (%s, %s, %s)'''
    data = (notification_text, time_created, user_id)

    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    return jsonify({'message': 'Notification sent successfully'}), 201

@experienced_trader.route('/notifications/<int:user_id>', methods=['GET'])
def get_notifications(user_id):
    current_app.logger.info(f'GET /notifications/{user_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM notifications WHERE user_id = %s ORDER BY timeCreated DESC', (user_id,))
    
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@experienced_trader.route('/notifications/detail/<int:notification_id>', methods=['GET'])
def get_notification_detail(notification_id):
    current_app.logger.info(f'GET /notifications/detail/{notification_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM notifications WHERE id = %s', (notification_id,))
    
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@experienced_trader.route('/stocks/<int:user_id>', methods=['GET'])
def get_traded_stocks(user_id):
    current_app.logger.info(f'GET /stocks/{user_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT s.* FROM stocks s JOIN notifications n ON s.stock_id = n.stock_id WHERE n.user_id = %s', (user_id,))
    
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
