import cv2 as cv
import numpy as np
import mediapipe as mp






#카메라 회전 함수
def Rotate(src, degrees):
    if degrees == 90:
        dst = cv.transpose(src)
        dst = cv.flip(dst, 1)

    elif degrees == 180:
        dst = cv.flip(src, -1)

    elif degrees == 270:
        dst = cv.transpose(src)
        dst = cv.flip(dst, 0)
    else:
        dst = null
    return dst

def Flip(src, direction):
    # 0: 상하 반전, 1: 좌우반전
    dst = cv.flip(src, direction)
    return dst


cam = cv.VideoCapture(0)

#카메라 이미지 해상도 얻기
width = cam.get(cv.CAP_PROP_FRAME_WIDTH)
height = cam.get(cv.CAP_PROP_FRAME_HEIGHT)
print ('size = [%f, %f]\n' % (width, height))

#윈도우 생성 및 사이즈 변경
#cv.namedWindow('Main')
#cv.resizeWindow('Main', 1280, 720)


#회전 윈도우 생성
#cv.namedWindow('CAM_RotateWindow')


mp_face_mesh = mp.solutions.face_mesh

LEFT_EYE = [362,382,381,380,374,373,390,249,263,466,388,387,386,385,384,398]
RIGHT_EYE = [ 33,7,163,144,145,153,154,155,133,173,157,158,159,160,161,246 ]
LEFT_IRIS = [474,475,476,477 ]
RIGHT_IRIS = [469,470,471,472 ]
FACE_HEAD_POSE_LACNMARKS = [1, 33, 61, 199, 291, 263]






with mp_face_mesh.FaceMesh(max_num_faces =1,
                           refine_landmarks =True,
                           min_detection_confidence =0.5,
                           min_tracking_confidence =0.5
) as face_mesh:
    while True:
        if cam.get(cv.CAP_PROP_POS_FRAMES) == cam.get(cv.CAP_PROP_FRAME_COUNT):
            cam.set(cv.CAP_PROP_POS_FRAMES, 0)
        ret, frame = cam.read()
        if not ret:
            break
        img_h, img_w = frame.shape[:2]
        results = face_mesh.process(frame)
        if results.multi_face_landmarks:
            mesh_points = np.array([np.multiply([p.x, p.y], [img_w, img_h]).astype(int)
                                 for p in results.multi_face_landmarks[0].landmark])

            #face_mesh 전부 표시하기 색(B,G,R)
            for pt in mesh_points:
                #cv.circle(img, center,radius,color,thicknex,lineType)
                cv.circle(frame, pt, 1, (255,255,255), -1, cv.LINE_AA)

            print(mesh_points)

            #아이라인
            cv.polylines(frame, [mesh_points[LEFT_EYE]], True, (0, 255, 0), 2, cv.LINE_AA)
            cv.polylines(frame, [mesh_points[RIGHT_EYE]], True, (0, 255, 0), 2, cv.LINE_AA)

            #눈동자 마름모
            # cv.polylines(frame, [mesh_points[LEFT_IRIS]], True, (0, 0, 255), 2, cv.LINE_AA)
            # cv.polylines(frame, [mesh_points[RIGHT_IRIS]], True, (0, 0, 255), 2, cv.LINE_AA)

            #눈동자 원형
            (l_cx, l_cy), l_radius = cv.minEnclosingCircle(mesh_points[LEFT_IRIS])
            (r_cx, r_cy), r_radius = cv.minEnclosingCircle(mesh_points[RIGHT_IRIS])
            center_left = np.array([l_cx, l_cy], dtype=np.int32)
            center_right = np.array([r_cx, r_cy], dtype=np.int32)
            cv.circle(frame, center_left, int(l_radius), (0, 0, 255), 2, cv.LINE_AA)
            cv.circle(frame, center_right, int(r_radius), (0, 0, 255), 2, cv.LINE_AA)

            # face_direction
            face_2d = []
            face_3d = []

            for idx, lm in enumerate(results.multi_face_landmarks[0].landmark):
                if idx in FACE_HEAD_POSE_LACNMARKS:
                    if idx == 1:
                        nose_2d = (lm.x*img_w,lm.y*img_h)
                        nose_3d = (lm.x*img_w,lm.y*img_h, lm.z*3000)

                    x,y = int(lm.x * img_w), int(lm.y * img_h)

                    face_2d.append([x,y])
                    face_3d.append([x, y,lm.z])

            face_2d = np.array(face_2d, dtype=np.float64)
            face_3d = np.array(face_3d, dtype=np.float64)

            focal_len = 1 * img_w

            camera_mat = np.array([[focal_len, 0, img_h/2],
                                  [0, focal_len, img_w/2],
                                  [0,0,1]])

            dist_mat = np.zeros((4,1), dtype = np.float64)

            success, rot_vec, trans_vec = cv.solvePnP(face_3d, face_2d, camera_mat, dist_mat)

            rot_mat, jac = cv.Rodrigues(rot_vec)
            angles, mtxR, mtxQ, Qx, Qy, Qz = cv.RQDecomp3x3(rot_mat)
            x = angles[0] * 360
            y = angles[1] * 360
            z = angles[2] * 360

            #nose+3d_projection, jacobian = cv.projectionPoints(nose_3d, rot_vec, trans_vec, camera_mat, dist_mat)

            p1 = (int(nose_2d[0]), int(nose_2d[1]))
            p2 = (int(nose_2d[0]+y*10), int(nose_2d[1] -x * 10))

            cv.line(frame,p1,p2,(255,255,0),3)



        # 이미지를 회전시켜서 img로 돌려받음
        img = Rotate(frame, 90)  # 뒷면90 or 180 or 앞면270

        # 이미지를 반전시켜 img2로 돌려받음
        img2 = Flip(frame, 1)

        #원래 이미지 표시
        cv.imshow('Main', frame)

        # 회전된 이미지 표시
        #cv.imshow('CAM_RotateWindow', img)

        #반전된 이미지 표시
        #cv.imshow('CAM_FlipWindow', img2)

        #윈도우 크기 늘리기/줄이기
        dst2 = cv.resize(frame, dsize=(720, 480), interpolation=cv.INTER_AREA)
        cv.imshow('CAM_Window2', dst2)

        key = cv.waitKey(1)
        if key == ord('q'):
            break

frame.release()
#메인 윈도우 제거
cv.destroyAllWindows()
#회전 원도우 제거
#cv.destroyWindow('CAM_RotateWindow')
