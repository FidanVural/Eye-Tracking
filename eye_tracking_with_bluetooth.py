# ÇDTP

import cv2
import numpy as np
import dlib
import time
import serial

ser = serial.Serial("COM8",9600,timeout =1)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")



def get_gaze_ratio(eye_points,landmarks):
    # GAZE DETECTION
    
    eye_region = np.array([(landmarks.part(eye_points[0]).x, landmarks.part(eye_points[0]).y),
                           (landmarks.part(eye_points[1]).x, landmarks.part(eye_points[1]).y),
                           (landmarks.part(eye_points[2]).x, landmarks.part(eye_points[2]).y),
                           (landmarks.part(eye_points[3]).x, landmarks.part(eye_points[3]).y),
                           (landmarks.part(eye_points[4]).x, landmarks.part(eye_points[4]).y),
                           (landmarks.part(eye_points[5]).x, landmarks.part(eye_points[5]).y)], np.int32)

    min_x = np.min(eye_region[:, 0])
    max_x = np.max(eye_region[:, 0])
    min_y = np.min(eye_region[:, 1])
    max_y = np.max(eye_region[:, 1])
    
    h, w, _ = frame.shape 
    mask = np.zeros((h, w), np.uint8)
    
    cv2.polylines(mask, [eye_region], True, 255, 2)
    cv2.fillPoly(mask, [eye_region], 255) # fill the area -> white
    eyeImage = cv2.bitwise_and(gray, gray, mask=mask)
    
    # göz kısmını resimden kırptık.
    cropedEye = eyeImage[min_y:max_y, min_x:max_x]
    
    # THRESHOLD
    _, threshold_eye = cv2.threshold(cropedEye, 75, 255, cv2.THRESH_BINARY)

    
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(threshold_eye.astype(np.float32), cv2.MORPH_OPEN, kernel)
    
    cv2.imshow("Threshold eye", opening)
    
    t_h, t_w = threshold_eye.shape
    
    trash = cv2.resize(threshold_eye, None, fx=7, fy=7)
    cv2.imshow("EYE ",trash)
    
    right_side_threshold = threshold_eye[0: t_h, 0: int(t_w / 2)]
    right_side_white = cv2.countNonZero(right_side_threshold)
    
    left_side_threshold = threshold_eye[0: t_h,int(t_w / 2): t_w]
    left_side_white = cv2.countNonZero(left_side_threshold)
    
    upper_side_threshold = threshold_eye[0: int(t_h/2), 0: t_w]
    upper_side_white = cv2.countNonZero(upper_side_threshold)
    
    down_side_threshold = threshold_eye[int(t_h/2): t_h, 0: t_w]
    down_side_white = cv2.countNonZero(down_side_threshold)
    
    pos = ""
    #print("Right: ", right_side_white)
    #print("left: ", left_side_white)
    #print("Up: ", upper_side_white)
    #print("Down: ", down_side_white)
    #print("\n")
    
    
    arr = []
    arr.append(right_side_white)
    arr.append(left_side_white)
    arr.append(upper_side_white)
    arr.append(down_side_white)
    
    temp = min(arr)
    index = arr.index(temp)
    
    hor_1_threshold = threshold_eye[0: t_h, 0: int(t_w/3)]
    hor_1_white = cv2.countNonZero(hor_1_threshold)
    
    hor_2_threshold = threshold_eye[0: t_h, int(t_w/3): int(t_w/3)+int(t_w/3)]
    hor_2_white = cv2.countNonZero(hor_2_threshold)
    
    hor_3_threshold = threshold_eye[0: t_h, int(t_w/3)+int(t_w/3): t_w]
    hor_3_white = cv2.countNonZero(hor_3_threshold)
    #print("Hor2white: ", hor_2_white)
                                   

    #print(hor_1_white, hor_2_white, hor_3_white)

    if (hor_2_white < hor_1_white) and (hor_2_white < hor_3_white) and (hor_2_white < 30):
        pos = "CENTER"
    elif (right_side_white <= 15) and (left_side_white <= 15) and (upper_side_white <= 15) and (down_side_white <= 15):
        pos = "DOWN"
    elif index == 0:
        pos = "RIGHT"
    elif index == 1:
        pos = "LEFT"
    elif index == 2:
        pos = "UP"
    
    
    return pos


def most_frequent(arr):
    return max(set(arr), key = arr.count)

prev_frame_time = 0
new_frame_time = 0

count = 0
pos_arr = []

while True:

    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    new_frame = np.zeros((500, 500, 3), np.uint8)

    faces = detector(gray)
    for face in faces:
        
        landmarks = predictor(gray, face)
        
        points_left = [36,37,38,39,40,41]
        points_right = [42,43,44,45,46,47]

        count += 1
        pos = get_gaze_ratio(points_left, landmarks)
        #pos = get_gaze_ratio(points_right, landmarks)q
        pos_arr.append(pos)
        
        new_frame_time = time.time()

        fps = 1/(new_frame_time-prev_frame_time)
        prev_frame_time = new_frame_time

        fps = int(fps)
        #print("FPS: ", fps)
            
        if count == 20:
            end_pos = most_frequent(pos_arr)
            cv2.putText(frame, end_pos, (100, 200), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 4)
            print(end_pos)
            count = 0
            pos_arr = []
            
            if(ser.isOpen()==False):
                ser.open()
            if (end_pos == 'UP'):
                ser.write(b'u')
            elif (end_pos == 'DOWN'): 
                ser.write(b'd')
            elif (end_pos == 'LEFT'): 
                ser.write(b'l')
            elif (end_pos == 'RIGHT'): 
                ser.write(b'r')
            elif (end_pos == 'CENTER'): 
                ser.write(b'c')
            #ser.close()
    
    cv2.imshow("Frame", frame)
    #cv2.imshow("Nwe Frame", new_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
       break
    
cap.release()
cv2.destroyAllWindows()








