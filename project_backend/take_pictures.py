import cv2
import os

def take_photo():
    """
    Captures a photo using the default camera and saves it to the 'uploadedpictures' folder.

    This function initializes the camera, captures a single frame, and saves it as 'photo.jpg' 
    in the specified output folder. If the folder does not exist, it is created automatically. 
    The camera is released after the operation.

    Returns:
        None

    Raises:
        Prints error messages if the camera cannot be accessed or the frame cannot be captured.
    """
    # Create the output folder if it doesn't exist
    output_folder = "uploadedpictures"
    os.makedirs(output_folder, exist_ok=True)

    # Initialize the camera
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Error: Could not access the camera.")
        return

    ret, frame = camera.read()
    if not ret:
        print("Error: Could not capture the frame.")
        
    output_path = os.path.join(output_folder, "photo.jpg")
    cv2.imwrite(output_path, frame)
    print(f"Photo saved at {output_path}")


    # Release the camera
    camera.release()
    print("Camera released.")

