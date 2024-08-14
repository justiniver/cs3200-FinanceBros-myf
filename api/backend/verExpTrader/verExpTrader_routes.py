from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

experienced_trader = Blueprint('experienced_trader', __name__)

# User Story 1
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
