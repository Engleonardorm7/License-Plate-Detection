import sqlite3
import os
import datetime
import shutil

def register_vehicle_entry(plate):
    image_name = f"{plate}.jpg"
    image_path = os.path.join('plates', image_name)

    if not os.path.exists(image_path):
        print(f"Error: Image {image_name} not found.")
        return False

    entry_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('database.db')

    try:
        
        conn.execute('''
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plate TEXT NOT NULL,
            image_path TEXT NOT NULL,
            entry_time TEXT NOT NULL,
            end_time TEXT,
            status TEXT
        )
        ''')

        conn.execute('INSERT INTO vehicles (plate, image_path, entry_time, status) VALUES (?, ?, ?, ?)', 
                     (plate, image_path, entry_time,'inside'))
        conn.commit()
        print(f"Vehicle {plate} Registered")
        return True
    except sqlite3.Error as e:
        print(f"Error registering vehicle: {e}")
        return False
    finally:
        conn.close()




def vehicle_exit(plate_number):
    conn= sqlite3.connect('database.db')
    try:
        vehicle = conn.execute('SELECT * FROM vehicles WHERE plate = ?',(plate_number,)).fetchone()

        if vehicle is None:
            print(f'Error: Vehicle not found')
            return False
        if vehicle[5] != 'payed':
            print(f'Error: Payment not completed yet, please go to the payment point')
            return False
        else:
            conn.execute('DELETE FROM vehicles WHERE plate = ?',(plate_number,))
            conn.commit()
            conn.close()
            print(f'Thank you for your visit! Drive safely!')
    except sqlite3.Error as e:
        print(f"Error during vehicle exit: {e}")
        return False
 ###############################################################################
'''
Inputs: plate number, and store the picture of the plates in the folder plates and store them with the plate number, e.g. SN66CMZ.jpg
'''
plate_number = 'SL593LM'
'SN66CMZ'


# To create the vehicle in the database
register_vehicle_entry(plate_number)


# Allows the vehicle to exit and delete its information
# vehicle_exit(plate_number)