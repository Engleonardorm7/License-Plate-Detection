from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
from flask import Flask, send_from_directory
from inference_code import LicensePlateDetector
from ocr_models import detect_text_easyocr, detect_text_paddleocr

from take_pictures import take_photo
from vehicle import register_vehicle_entry, rename_and_move_photo, vehicle_exit


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


def get_db_connection():
    """
    Establishes a connection to the SQLite database.

    Returns:
        conn (sqlite3.Connection): A connection object to interact with the database.
    """
    conn=sqlite3.connect('database.db')
    conn.row_factory=sqlite3.Row
    return conn

#show image
@app.route('/images/plates/<path:plate>', methods=['GET'])
def serve_image(plate):
    """
    Serves an image of a vehicle's license plate from the 'plates' directory.

    Args:
        plate (str): The file name of the image to be served.

    Returns:
        Response: The image file corresponding to the license plate.
    """
    return send_from_directory('plates', plate)

#save vehicles
@app.route('/api/vehicle/<plate>', methods=['GET'])
def get_vehicle(plate):
    """
    Retrieves vehicle information from the database based on the license plate.

    Args:
        plate (str): The license plate of the vehicle to retrieve.

    Returns:
        Response: JSON object with vehicle details or an error message if not found.
    """
    conn=get_db_connection()
    vehicle = conn.execute('SELECT * FROM vehicles WHERE plate = ?', (plate,)).fetchone()
    conn.close()

    if vehicle is None:
        return jsonify({'error':'Vehicle not found'}), 404 
    
    image_path = vehicle['image_path'].replace('\\', '/')  
    vehicle_dict = dict(vehicle)
    vehicle_dict['image_path'] = image_path

    return jsonify(vehicle_dict)
    
# update the exit time
@app.route('/api/vehicle/<plate>/exit', methods=['POST'])
def update_exit_time(plate):
    """
    Updates the exit time and calculates the total cost for a vehicle based on its entry and exit times.

    Args:
        plate (str): The license plate of the vehicle to update.

    Returns:
        Response: JSON object with total time, total cost, and exit time.
    """
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

    conn.close()

    return jsonify({
        'total_time': total_time,
        'total_cost': total_cost,
        'end_time': end_time
    }), 200

# update the payment status
@app.route('/api/vehicle/<plate>/pay', methods=['POST'])
def update_payment_status(plate):
    """
    Updates the payment status of a vehicle to 'paid'.

    Args:
        plate (str): The license plate of the vehicle to update.

    Returns:
        Response: JSON message indicating payment success.
    """
    conn = get_db_connection()
    
    conn.execute('UPDATE vehicles SET status = ? WHERE plate = ?', ('paid', plate))
    conn.commit()
    conn.close()

    return jsonify({'message':'Payment successfull'}),200

    
@app.route('/input', methods=['POST'])
def take_photo_and_register():
    """
    Captures a photo, detects and recognizes the license plate from the image, 
    and registers the vehicle entry in the database.

    This function performs the following steps:
    1. Captures a photo using the `take_photo()` function.
    2. Detects the license plate using a YOLOv8 model for object detection.
    3. Crops the detected license plate and uses OCR to recognize the plate number.
    4. Renames and moves the photo based on the detected plate number to organize the dataset.
    5. Registers the vehicle entry in the database using the detected plate number.

    Returns:
        Response: A JSON response indicating the success or failure of the vehicle registration.
            - On success: JSON with a success message.
            - On failure: JSON with an error message.

    Raises:
        Exception: If any step in the process fails (e.g., photo capture, license plate detection, OCR, or database registration).
    """
    
    try:
        plate_number=0
        take_photo()

        # License plate detection - YOLOv8

        model_path = './best.pt'  # Specify the path to your YOLOv8 model
        detector = LicensePlateDetector(model_path)
        image_path = './uploadedpictures/photo.jpg'       # Specify the path to the input image

        bbox, cropped_plate = detector.inference(image_path)
        # print("Bounding box with highest confidence:", bbox)

        # # License plate recognition
        print('*'*50)

        plate_number=detect_text_easyocr('./uploadedpictures/photo_cropped_plate.jpg')
        #plate_number=detect_text_paddleocr('./uploadedpictures/photo_cropped_plate.jpg')
        print(plate_number)

        # change name of the photo to create the dataset
        rename_and_move_photo(plate_number)

        # To create the vehicle in the database
        result = register_vehicle_entry(plate_number)
        if result['success']:
            return jsonify({"message": result['message']}), 200
        else:
            return jsonify({"message": result['message']}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/vehicle_exit', methods=['POST'])
def exit():
    """
    Manages the vehicle exit process by capturing a photo, detecting the license plate, 
    and allowing the vehicle to exit if the plate is recognized and valid.

    This function performs the following steps:
    1. Captures a photo of the vehicle.
    2. Detects the license plate using a YOLOv8 model.
    3. Recognizes the license plate number using OCR.
    4. Allows the vehicle to exit if the license plate number is found in the database and criteria are met.

    Returns:
        Response: A JSON response indicating the success or failure of the vehicle exit process.
            - On success: JSON with exit result.
            - On failure: JSON with error message.

    Raises:
        Exception: If any step in the process fails (e.g., photo capture, license plate detection, OCR).
    """
    plate_number=0
    try:
        print('*'*50)
        take_photo()

        # License plate detection - YOLOv8

        model_path = './best.pt'  # Specify the path to your YOLOv8 model
        detector = LicensePlateDetector(model_path)
        image_path = './uploadedpictures/photo.jpg'       # Specify the path to the input image

        bbox, cropped_plate = detector.inference(image_path)
        # print("Bounding box with highest confidence:", bbox)

        # # License plate recognition
        print('*'*80)

        plate_number=detect_text_easyocr('./uploadedpictures/photo_cropped_plate.jpg')
        #plate_number=detect_text_paddleocr('./uploadedpictures/photo_cropped_plate.jpg')
        print(plate_number)

        # allow the vehicle to exit
        result = vehicle_exit(plate_number)

        if not result["success"]:
            return jsonify(result), 400  # Error response for client-side issues
        print('*'*80)
        return jsonify(result), 200  # Success response
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"success": False, "message": f"Unexpected error: {e}"}), 500

if __name__=='__main__':
    app.run(debug=True)

