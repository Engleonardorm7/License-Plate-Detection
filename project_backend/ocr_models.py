from paddleocr import PaddleOCR, draw_ocr
import easyocr
import cv2

# Pre trained PaddleOCR
ocr = PaddleOCR(lang='en') 

# Fine tuned EasyOCR
reader_ft = easyocr.Reader(['en'], 
                        gpu=True,
                        quantize=True,
                        model_storage_directory='EasyOCR/model',
                        user_network_directory='EasyOCR/user_network',
                        recog_network='best_accuracy')

def remove_special_char(text):
    return ''.join(c for c in text if c.isalnum())

def detect_text_paddleocr(image_path):    
    image = cv2.imread(image_path)
    
    ''' Image Processing 
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gaussian_blur = cv2.GaussianBlur(image,(7,7),sigmaX=2)
    sharp_image = cv2.addWeighted(image,8.5,gaussian_blur,-6.5,0)'''

    # Pre-trained model from PaddleOCR
    results = ocr.ocr(image, det=False, cls=False)

    detected_text = ''
    
    if (len(results) == (0 or None)) or (results[0] == None):
        print("The model couldn't detect any word.")
    else: 
        detected_text = remove_special_char(results[0][0][0])

    return detected_text

def detect_text_easyocr(image_path):    
    image = cv2.imread(image_path)
    
    ''' Image Processing 
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gaussian_blur = cv2.GaussianBlur(image,(7,7),sigmaX=2)
    sharp_image = cv2.addWeighted(image,8.5,gaussian_blur,-6.5,0) '''

    # Fine tuned EasyOCR Model
    results = reader_ft.recognize(image)

    detected_text = ''

    if len(results) == 0:
        print("The model couldn't detect any word.")
    elif len(results) == 2:
        if results[0][2] > results[1][2]:
            detected_text = results[0][1]
        else:
            detected_text = results[1][1]
    else: 
        for i in range(len(results)):
            string_part = results[i][1]
            detected_text = detected_text + string_part

    return detected_text