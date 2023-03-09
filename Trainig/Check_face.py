import cv2 as cv
import numpy as np
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh

LEFT_EYE = []
RIGHT_EYE = []

with mp_face_mesh.FaceMesh(max_num_faces =1,
                           refine_landmarks =True,
                           min_detection_confidence =0.5,
                           min_tracking_confidence =0.5
) as face_mesh:
    while True:
        frame = cv.imread('elon_musk.jpg')
        img_h, img_w = frame.shape[:2]
        results = face_mesh.process(frame)
        if results.multi_face_landmarks:
            mesh_points = np.array([np.multiply([p.x, p.y], [img_w, img_h]).astype(int)
                                    for p in results.multi_face_landmarks[0].landmark])
            print(mesh_points)

        cv.imshow('Main', frame)

        key = cv.waitKey(1)
        if key == ord('q'):
            break

frame.release()
cv.destroyAllWindows()