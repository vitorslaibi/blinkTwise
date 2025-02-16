import math
import random
import time

import cv2 as cv
import mediapipe as mp
import numpy as np
import components

threshold = 3.8
session_st = time.time()
prompts = 0
alerts = 0
bpm = 0
settings_id = 0
last_alert = None

left_eye = [362, 382, 381, 380, 374, 373, 390,
            249, 263, 466, 388, 387, 386, 385, 384, 398]
right_eye = [33, 7, 163, 144, 145, 153, 154,
             155, 133, 173, 157, 158, 159, 160, 161, 246]
map_face_mesh = mp.solutions.face_mesh


def landmarksDetection(img, results, draw=False):
    img_height, img_width = img.shape[:2]
    mesh_coord = [(int(point.x * img_width), int(point.y * img_height))
                  for point in results.multi_face_landmarks[0].landmark]

    if draw:
        [cv.circle(img, p, 2, (255, 0, 0), -1) for p in mesh_coord]

    # returning the list of tuples for each landmark
    return mesh_coord


def fillPolyTrans(img, points, color, opacity):
    list_to_np_array = np.array(points, dtype=np.int32)
    overlay = img.copy()
    cv.fillPoly(overlay, [list_to_np_array], color)
    new_img = cv.addWeighted(overlay, opacity, img, 1 - opacity, 0)
    img = new_img

    return img


def euclaideanDistance(point, point1):
    x, y = point
    x1, y1 = point1
    distance = math.sqrt((x1 - x) ** 2 + (y1 - y) ** 2)
    return distance


def blinkRatio(landmarks, right_indices, left_indices):
    # Right eyes
    rh_right = landmarks[right_indices[0]]
    rh_left = landmarks[right_indices[8]]
    rv_top = landmarks[right_indices[12]]
    rv_bottom = landmarks[right_indices[4]]

    # draw lines on right eyes
    # cv.line(img, rh_right, rh_left, (255,255,255), 2)
    # cv.line(img, rv_top, rv_bottom, (255,255,255), 2)

    # LEFT_EYE
    lh_right = landmarks[left_indices[0]]
    lh_left = landmarks[left_indices[8]]
    lv_top = landmarks[left_indices[12]]
    lv_bottom = landmarks[left_indices[4]]

    # Finding Distance Right Eye
    rhDistance = euclaideanDistance(rh_right, rh_left)
    rvDistance = euclaideanDistance(rv_top, rv_bottom)

    # Finding Distance Left Eye
    lvDistance = euclaideanDistance(lv_top, lv_bottom)
    lhDistance = euclaideanDistance(lh_right, lh_left)

    # Finding ratio of LEFT and Right Eyes
    reRatio = rhDistance / rvDistance
    leRatio = lhDistance / lvDistance
    ratio = (reRatio + leRatio) / 2

    return ratio


# def updateDB(blink_count, eyes_closed_time, blink_interval_endtime):
#     connection = sqlite3.connect(dbLocation)
#     cursor = connection.cursor()
#     row = cursor.execute(
#         'SELECT * FROM session ORDER BY session_id DESC').fetchone()
#     cursor.execute('''INSERT INTO blink_records(start_time, end_time, session_id) VALUES (?, ?, ?)''',
#                    (eyes_closed_time - session_st, eyes_closed_time + blink_interval_endtime - session_st, row[0]))
#     session_et = time.time()
#     cursor.execute(
#         ''' UPDATE session SET end_time = ? ,total_blinks = ? , prompts_given = ?, alerts_given = ? WHERE total_blinks = ?''',
#         (session_et, blink_count, prompts, alerts, blink_count))
#     connection.commit()


def getSettings(cursor, settings_id):
    row = cursor.execute('''SELECT * FROM settings WHERE settings_id = ?''', settings_id)
    return row

def getThreshold(cursor, settings_id):
    settings_id = getSettings(cursor, settings_id)

    return 3.5


def setAlert(newAlert):
    global alert
    alert = newAlert


def main(cursor, cam, settings):
    frame_count = 0
    distance_count = 0

    eyes_closed = False
    fonts = cv.FONT_HERSHEY_COMPLEX
    blink_count = 0

    user_id = random.randint(1, 1000)
    session_st = time.time()

    global last_alert
    last_alert = session_st
    cursor.execute('''INSERT INTO session(user_id,begin_time,total_blinks) VALUES (?, ?, ?)''',
                   (user_id, session_st, blink_count))

    with map_face_mesh.FaceMesh(min_detection_confidence=.5, min_tracking_confidence=.5) as face_mesh:
        st = time.time()
        et = 0
        eyes_closed_time = 0
        eyes_closed_endtime = 0
        blink_interval_time = 0
        blink_interval_endtime = 0

        while (True):
            alert_interval = 10
            # frame_count += 1
            accept, frame = cam.read()

            if not accept:
                break

            rgb_frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
            results = face_mesh.process(rgb_frame)

            if results.multi_face_landmarks:
                mesh_coords = landmarksDetection(frame, results, True)
                frame = fillPolyTrans(
                    frame, [mesh_coords[p] for p in right_eye], (255, 255, 0), opacity=.6)
                frame = fillPolyTrans(
                    frame, [mesh_coords[p] for p in left_eye], (255, 255, 0), opacity=.6)
                distance = blinkRatio(mesh_coords, right_eye, left_eye)

                if settings[1] < distance:
                    if not eyes_closed:
                        eyes_closed = True
                        blink_count += 1
                        eyes_closed_time = time.time()
                        blink_interval_endtime = time.time() - blink_interval_time
                        row = cursor.execute(
                            'SELECT * FROM session ORDER BY session_id DESC').fetchone()
                        cursor.execute(
                            '''INSERT INTO blink_records(start_time, end_time, session_id) VALUES (?, ?, ?)''',
                            (eyes_closed_time - session_st, eyes_closed_time + blink_interval_endtime - session_st,
                             row[0]))
                        session_et = time.time()
                        cursor.execute(
                            ''' UPDATE session SET end_time = ? ,total_blinks = ? , prompts_given = ?, alerts_given = ? WHERE begin_time = ?''',
                            (session_et, blink_count, prompts, alerts, session_st))

                else:
                    if eyes_closed:
                        eyes_closed_endtime = time.time() - eyes_closed_time
                        blink_interval_time = time.time()
                    eyes_closed = False

            # Show Blink Count
            et = time.time() - st
            if et != 0:
                global bpm
                bpm = (blink_count / et) * 60
            else:
                bpm = 0
            # cv.putText(frame,f'FPS: {round(fps,1)}',(50, 50), fonts, 1.0, (0, 255, 255), 2, cv.LINE_4)
            cv.putText(frame, f'Blink Count: {blink_count}',
                       (50, 50), fonts, 1.0, (0, 255, 255), 2, cv.LINE_4)
            cv.putText(frame, f'Closed time: {eyes_closed_endtime}',
                       (50, 100), fonts, 1.0, (0, 255, 255), 2, cv.LINE_4)
            cv.putText(frame, f'Interval time: {blink_interval_endtime}', (
                50, 150), fonts, 1.0, (0, 255, 255), 2, cv.LINE_4)
            cv.putText(
                frame, f'Blinks Per Minute: {bpm}', (50, 200), fonts, 1.0, (0, 255, 255), 2, cv.LINE_4)
            if last_alert + alert_interval < time.time():
                last_alert = time.time()
                if bpm < settings[2] > -1:
                    components.prompt("Alert", "BPM is lower than recommended for your activity!\nWe recommend taking a break")
                if bpm > settings[3] > -1:
                    components.prompt("Alert", "BPM is higher than recommended for your activity!\nWe recommend taking a break")

            cv.imshow('Camera', frame)

            if cv.waitKey(5) & 0xFF == 27:
                cv.destroyAllWindows()
                cam.release()
                time.sleep(3)
                break
