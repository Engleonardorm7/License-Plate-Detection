from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
from flask import Flask, send_from_directory

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
# CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

def get_db_connection():
    conn=sqlite3.connect('database.db')
    conn.row_factory=sqlite3.Row
    return conn

@app.route('/images/plates/<path:plate>', methods=['GET'])
def serve_image(plate):
    return send_from_directory('plates', plate)


@app.route('/api/vehicle/<plate>', methods=['GET'])
def get_vehicle(plate):
    conn=get_db_connection()
    vehicle = conn.execute('SELECT * FROM vehicles WHERE plate = ?', (plate,)).fetchone()
    conn.close()

    if vehicle is None:
        return jsonify({'error':'Vehicle not found'}), 404 
    
    image_path = vehicle['image_path'].replace('\\', '/')  # Convertir a barras normales
    vehicle_dict = dict(vehicle)
    vehicle_dict['image_path'] = image_path

    return jsonify(vehicle_dict)
    
@app.route('/api/vehicle', methods = ['POST'])
def add_vehicle():
    new_vehicle = request.json
    conn= get_db_connection()

    conn.execute('INSERT INTO vehicles (plate, image, entry_time) VALUES (?, ?, ?)', (new_vehicle['plate'], new_vehicle['image'], new_vehicle['entry_time']))

    conn.commit()
    conn.close()
    return jsonify({'status':'success'}),201


@app.route('/api/vehicle/<plate>/exit', methods=['POST'])
def update_exit_time(plate):
    conn = get_db_connection()

    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    vehicle = conn.execute('SELECT * FROM vehicles WHERE plate = ?', (plate,)).fetchone()

    if vehicle is None:
        conn.close()
        return jsonify({'error': 'Vehicle not found'}), 404
    
    conn.execute('UPDATE vehicles SET end_time = ? WHERE plate = ?', (end_time, plate))
    conn.commit()

    #total cost
    entry_time = datetime.strptime(vehicle['entry_time'], '%Y-%m-%d %H:%M:%S')
    exit_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

    total_time = (exit_time - entry_time).total_seconds() / 3600

    total_cost = 2 if total_time <= 1 else total_time * 2

    if total_time <= 1:
        total_cost = 2
    else:
        total_cost = total_time * 2

    # conn.execute('UPDATE vehicles SET total_cost = ? WHERE plate = ?', (total_cost, plate))
    # conn.commit()
    conn.close()

    return jsonify({
        'total_time': total_time,
        'total_cost': total_cost,
        'end_time': end_time
    }), 200


@app.route('/api/vehicle/<plate>/pay', methods=['POST'])
def update_payment_status(plate):
    conn = get_db_connection()
    
    conn.execute('UPDATE vehicles SET status = ? WHERE plate = ?', ('payed', plate))
    conn.commit()
    conn.close()

    return jsonify({'message':'Payment successfull'}),200
    

# @app.route('/api/vehicle/<plate>/exit', methods=['POST'])
# def verify_exit(plate):
#     conn=get_db_connection()

#     vehicle = conn.execute('SELECT * FROM vehicles WHERE plate = ?', (plate,)).fetchone()

#     if vehicle is None:
#         conn.close()
#         return jsonify({'error': 'Vehicle not found'}), 404
    
#     vehicle_dict = dict(vehicle)

#     if vehicle_dict['status']=='payed':
#         conn.execute('DELETE FROM vehicles WHERE plate = ?',(plate,))
#         conn.commit()
#         conn.close()
#         return jsonify({'message': 'Thank you for your visit! Drive safely!'}), 200
#     else:
#         return jsonify({'error': 'Payment not completed, please go to the payment point'}), 403


if __name__=='__main__':
    app.run(debug=True)