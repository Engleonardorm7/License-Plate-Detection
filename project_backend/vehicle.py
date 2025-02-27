import sqlite3
import os
import datetime
import shutil

def register_vehicle_entry(plate):
    """
    Registers a vehicle's entry into the database.

    Parameters:
        plate (str): The license plate of the vehicle.

    Returns:
        dict: A dictionary indicating success or failure, along with a message.
    """
    image_name = f"{plate}.jpg"
    image_path = os.path.join('./plates', image_name)

    if not os.path.exists(image_path):
        #print(f"Error: Image {image_name} not found.")
        return False

    entry_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('./database.db')
    image_path = os.path.join('/plates', image_name)
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
        vehicle = conn.execute('SELECT * FROM vehicles WHERE plate = ?',(plate,)).fetchone()
        if vehicle:
            #print(f'Vehicle with plate {plate} is already registered')
            return {"success": False, "message": "Vehicle already registered"}
        
        conn.execute('INSERT INTO vehicles (plate, image_path, entry_time, status) VALUES (?, ?, ?, ?)', 
                     (plate, image_path, entry_time,'inside'))
        conn.commit()
        #print(f"Vehicle {plate} Registered")
        return {"success": True, "message": f"Vehicle Registered"}
    except sqlite3.Error as e:
        #print(f"Error registering vehicle: {e}")
        return {"success": False, "message": f"Error registering vehicle: {e}"}
    finally:
        conn.close()


def vehicle_exit(plate_number):
    """
    Handles the exit process for a vehicle.

    Parameters:
        plate_number (str): The license plate of the vehicle.

    Returns:
        dict: A dictionary indicating success or failure, along with a message.
    """
    conn= sqlite3.connect('./database.db')
    try:
        vehicle = conn.execute('SELECT * FROM vehicles WHERE plate = ?',(plate_number,)).fetchone()

        if vehicle is None:
            #print(f'Error: Vehicle not found')
            return {"success": False, "message": "Vehicle not found"}
        if vehicle[5] != 'paid':
            #print(f'Error: Payment not completed yet, please go to the payment point')
            return {"success": False, "message": "Payment not completed yet"}
        else:
            conn.execute('DELETE FROM vehicles WHERE plate = ?',(plate_number,))
            conn.commit()
            conn.close()
            return {"success": True, "message": "Thank you for your visit! Drive safely!"}
    except sqlite3.Error as e:
        #print(f"Error during vehicle exit: {e}")
        return {"success": False, "message": f"Database error: {e}"}


def rename_and_move_photo(plate_number):
    """
    Renames and moves a photo to the appropriate folder.

    Parameters:
        plate_number (str): The license plate of the vehicle.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    # Define the current path and new destination
    current_path = "./uploadedpictures/photo.jpg"
    new_folder = "./plates"
    new_file_name = f"{plate_number}.jpg"
    new_path = os.path.join(new_folder, new_file_name)

    # Ensure the destination folder exists
    os.makedirs(new_folder, exist_ok=True)

    # Check if the source file exists
    if not os.path.exists(current_path):
        print(f"Error: File {current_path} does not exist.")
        return False

    # Move and rename the file
    shutil.move(current_path, new_path)
    #print(f"Photo renamed and moved to {new_path}")
    return True

