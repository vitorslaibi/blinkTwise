import cv2
import mediapipe as mp
import math

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Landmark indices for left and right eyes
LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]

def euclidean_distance(point1, point2):
    """Calculate the Euclidean distance between two points."""
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def blink_ratio(landmarks, right_indices, left_indices):
    """Calculate the blink ratio based on eye landmarks."""
    # Right eye horizontal and vertical distances
    rh_right = landmarks[right_indices[0]]
    rh_left = landmarks[right_indices[8]]
    rv_top = landmarks[right_indices[12]]
    rv_bottom = landmarks[right_indices[4]]

    rh_distance = euclidean_distance(rh_right, rh_left)
    rv_distance = euclidean_distance(rv_top, rv_bottom)

    # Left eye horizontal and vertical distances
    lh_right = landmarks[left_indices[0]]
    lh_left = landmarks[left_indices[8]]
    lv_top = landmarks[left_indices[12]]
    lv_bottom = landmarks[left_indices[4]]

    lh_distance = euclidean_distance(lh_right, lh_left)
    lv_distance = euclidean_distance(lv_top, lv_bottom)

    # Calculate blink ratio
    re_ratio = rh_distance / rv_distance
    le_ratio = lh_distance / lv_distance
    ratio = (re_ratio + le_ratio) / 2

    return ratio

def detect_blinks(camera, session_id, db, Session):
    """Detect blinks in real-time using the webcam."""
    session = Session.query.get(session_id)
    blink_count = session.total_blinks
    eyes_closed = False

    while True:
        success, frame = camera.read()
        if not success:
            break

        # Process frame with MediaPipe Face Mesh
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            landmarks = [(int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])) 
                         for lm in results.multi_face_landmarks[0].landmark]
            
            # Calculate blink ratio
            ratio = blink_ratio(landmarks, RIGHT_EYE, LEFT_EYE)
            if ratio > 3.8:  # Threshold for closed eyes
                if not eyes_closed:
                    blink_count += 1
                    eyes_closed = True
            else:
                eyes_closed = False

            # Update blink count in the database
            session.total_blinks = blink_count
            db.session.commit()

            # Display blink count on the frame
            cv2.putText(frame, f"Blinks: {blink_count}", (10, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the frame
        cv2.imshow('Blink Detection', frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()