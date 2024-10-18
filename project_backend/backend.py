from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import datetime

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn=sqlite3.connect('database.db')
    conn.row_factory=sqlite3.Row
    return conn

@app.route('/api/vehicle/<plate>', methods=['GET'])
def get_vehicle(palte):
    conn=get_db_connection()
    vehicle = conn.execute('SELECT * FROM vehicles WHERE plate = ?', (plate,)).fetchone()
    conn.close()
    if vehicle is None:
        return jsonify({'error':'Vehicle not found'}), 404
    return jsonify(dict(vehicle))

@app.route('/api/vehicle', methods = ['POST'])
def add_vehicle():
    new_vehicle = request.json
    conn= get_db_connection()
    conn.execute('INSERT INTO VEHICLES (plate, image, entry_time) VALUES (?,?,?)', new_vehicle['plate'],new_vehicle['image'], new_vehicle['entry_time'])
    conn.commit()
    conn.close()
    return jsonify({'status':'success'}),201


@app.route('/api/vehicle/<plate>/exit', methods=['POST'])
def update_exit_time(plate):
    end_time=request.json['end_time']
    conn = get_db_connection

    vehicle=conn.execute('UPDATE vehicles SET end_time = ? WHERE plate = ?',(end_time,plate))
    conn.close()

    if vehicle is None:
        return jsonify({'error':'Vehicle not found'}), 404
    
    entri_time=datetime.strptime(vehicle['entry_time'], '%Y-%m-%d %H:%M:%S')
    exit_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    total_time= (exit_time-entri_time).total_secondes()/3600

    if total_time <= 3600:
        total_cost=2
    else:
        total_cost=total_time*2

    return jsonify({'total_time': total_time, 'total_cost':total_cost}), 200


if __name__=='__main__':
    app.run(debug=True)