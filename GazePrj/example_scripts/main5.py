import mediapipe as mp
import numpy as np
import cv2 as cv

LEFT_EYE = [ 362,382,381,380,374,373,390,249,263,466,388,387,386,385,384,398 ]
RIGHT_EYE = [ 33,7,163,144,145,153,154,155,133,173,157,158,159,160,161,246 ]

LEFT_IRIS = [ 474,475,476,477 ]
RIGHT_IRIS = [ 469,470,471,472 ]


mp_face_mesh = mp.solutions.face_mesh
capture = cv.VideoCapture('sample_vid.mp4')

with mp_face_mesh.FaceMesh(max_num_faces = 1,
                           refine_landmarks=True,
                           min_detection_confidence = 0.5,
                           min_tracking_confidence = 0.5
) as face_mesh:

    while True:
        if capture.get(cv.CAP_PROP_POS_FRAMES) == capture.get(cv.CAP_PROP_FRAME_COUNT):
            capture.set(cv.CAP_PROP_POS_FRAMES, 0)
        ret, frame = capture.read()
        if not ret:
            break
        #frame = cv.imread('elon_musk.jpg')
        img_h, img_w = frame.shape[:2]
        results = face_mesh.process(frame)
        if results.multi_face_landmarks:
            mesh_points = np.array([np.multiply([p.x, p.y], [img_w, img_h]).astype(int)
                                    for p in results.multi_face_landmarks[0].landmark])
            #print(mesh_points)

            cv.polylines(frame, [mesh_points[LEFT_EYE]], True, (0,255,0), 2, cv.LINE_AA)
            cv.polylines(frame, [mesh_points[RIGHT_EYE]], True, (0,255,0),2, cv.LINE_AA)

            cv.polylines(frame, [mesh_points[LEFT_IRIS]], True, (0,0,255),2, cv.LINE_AA)
            cv.polylines(frame, [mesh_points[RIGHT_IRIS]], True, (0,0,255),2, cv.LINE_AA)

        cv.imshow('Main',frame)
        key = cv.waitKey(1)
        if( key == ord('q')):
            break

capture.release()
cv.destroyAllWindows()