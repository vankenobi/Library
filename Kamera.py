from pyzbar.pyzbar import decode
import cv2
import numpy as np

def barcodeReader(image, bgr):
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    barcodes = decode(gray_img)

    for decodedObject in barcodes:

        points = decodedObject.polygon
    
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)
        
    for bc in barcodes:
        
        cv2.putText(frame, bc.data.decode("utf-8") + " - " + bc.type, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    bgr, 2)
        if bc.data.decode("utf-8") is not None:
            return bc.data.decode("utf-8")
            
            
bgr = (8, 70, 208)
cap = cv2.VideoCapture(0)

while (True):

    ret, frame = cap.read()
    barcode = barcodeReader(frame, bgr)
    print(type(barcode)) 
    cv2.imshow('Barcode reader', frame)
    if barcode is not None:

        break
    code = cv2.waitKey(10)
    if code == ord('q') :
        break 