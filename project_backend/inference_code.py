import cv2
from ultralytics import YOLO
import os

class LicensePlateDetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
    
    def inference(self, image_path):
        image = cv2.imread(image_path)
        
        results = self.model(image)
        
        boxes = results[0].boxes 
        if boxes is None or len(boxes) == 0:
            print("No license plate detected.")
            return None, None
        
        highest_conf_box = None
        highest_conf_score = 0
        
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0] 
            confidence = box.conf[0]  
            cls = box.cls[0] 
            
            if int(cls) == 0: 
                cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(image, f'Licence plate {confidence:.2f}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                if confidence > highest_conf_score:
                    highest_conf_box = {'x1': int(x1), 'y1': int(y1), 'x2': int(x2), 'y2': int(y2), 'confidence': confidence}
                    highest_conf_score = confidence
        
        base, ext = os.path.splitext(image_path)
        output_path = f"{base}_output{ext}"
        success = cv2.imwrite(output_path, image)
        if success:
            print(f"Image saved successfully at {output_path}")
        else:
            print(f"Failed to save image at {output_path}. Please check the path or permissions.")
        
        # If a license plate was detected, crop it from the image
        if highest_conf_box is not None:
            x1, y1, x2, y2 = highest_conf_box['x1'], highest_conf_box['y1'], highest_conf_box['x2'], highest_conf_box['y2']
            cropped_plate = image[y1:y2, x1:x2]
            
            # Save the cropped image
            cropped_output_path = f"{base}_cropped_plate{ext}"
            success = cv2.imwrite(cropped_output_path, cropped_plate)
            if success:
                print(f"Cropped license plate saved successfully at {cropped_output_path}")
            else:
                print(f"Failed to save cropped license plate at {cropped_output_path}. Please check the path or permissions.")
            
            return highest_conf_box, cropped_plate
        else:
            return highest_conf_box, None

# # Example usage
# model_path = './best.pt'  # Specify the path to your YOLOv8 model
# detector = LicensePlateDetector(model_path)
# image_path = './uploadedpictures/SN66CMZ.jpg'       # Specify the path to the input image

# bbox, cropped_plate = detector.inference(image_path)
# print("Bounding box with highest confidence:", bbox)