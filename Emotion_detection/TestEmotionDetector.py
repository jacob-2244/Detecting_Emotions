import cv2
import numpy as np
from keras.models import model_from_json


emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

# load json and create model
json_file = open('model/emotion_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
emotion_model = model_from_json(loaded_model_json)

# load weights into new model
emotion_model.load_weights("model/emotion_model.h5")
print("Loaded model from disk")

# start the webcam feed
cap = cv2.VideoCapture(0)

# pass here your video path
# you may download one from here : https://www.pexels.com/video/three-girls-laughing-5273028/
# cap = cv2.VideoCapture("C:\\Users\\TECHNIFI\\Downloads\\happy.mp4")

while True:
    # Find haar cascade to draw bounding box around face
    ret, frame = cap.read()
    frame = cv2.resize(frame, (1280, 720))
    if not ret:
        break
    face_detector = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces available on camera
    num_faces = face_detector.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

    # take each face available on the camera and Preprocess it
    for (x, y, w, h) in num_faces:
        cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (0, 255, 0), 4)
        roi_gray_frame = gray_frame[y:y + h, x:x + w]
        cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)

        # predict the emotions
        emotion_prediction = emotion_model.predict(cropped_img)
        maxindex = int(np.argmax(emotion_prediction))
        cv2.putText(frame, emotion_dict[maxindex], (x+5, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    cv2.imshow('Emotion Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

#
# import cv2
# import numpy as np
# from keras.models import model_from_json
# import tensorflow as tf
#
# # Optimize TensorFlow performance
# physical_devices = tf.config.list_physical_devices('GPU')
# if physical_devices:
#     tf.config.experimental.set_memory_growth(physical_devices[0], True)
#
# emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
#
# # load json and create model
# json_file = open('model/emotion_model.json', 'r')
# loaded_model_json = json_file.read()
# json_file.close()
# emotion_model = model_from_json(loaded_model_json)
#
# # load weights into new model
# emotion_model.load_weights("model/emotion_model.h5")
# print("Loaded model from disk")
#
# # Prepare model for faster inference
# emotion_model.make_predict_function()  # This is important for model inference performance
#
# # start the webcam feed
# cap = cv2.VideoCapture(0)
#
# # Load face detector only once
# face_detector = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
#
# while True:
#     # Find haar cascade to draw bounding box around face
#     ret, frame = cap.read()
#     if not ret:
#         break
#
#     frame = cv2.resize(frame, (1280, 720))
#     gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#
#     # detect faces available on camera
#     num_faces = face_detector.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)
#
#     # take each face available on the camera and Preprocess it
#     for (x, y, w, h) in num_faces:
#         cv2.rectangle(frame, (x, y - 50), (x + w, y + h + 10), (0, 255, 0), 4)
#         roi_gray_frame = gray_frame[y:y + h, x:x + w]
#
#         # Preprocess image for the model
#         try:
#             cropped_img = cv2.resize(roi_gray_frame, (48, 48))
#             normalized_img = cropped_img / 255.0  # Normalize pixel values
#             reshaped_img = np.expand_dims(np.expand_dims(normalized_img, -1), 0)
#
#             # predict the emotions
#             emotion_prediction = emotion_model.predict(reshaped_img, verbose=0)  # Turn off verbose output
#             maxindex = int(np.argmax(emotion_prediction))
#             confidence = float(emotion_prediction[0][maxindex])
#
#             # Display emotion and confidence
#             emotion_label = f"{emotion_dict[maxindex]} ({confidence:.2f})"
#             cv2.putText(frame, emotion_label, (x + 5, y - 20),
#                         cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
#         except Exception as e:
#             print(f"Error processing face: {e}")
#
#     # Display FPS
#     cv2.putText(frame, f"Press 'q' to quit", (10, 30),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
#
#     cv2.imshow('Emotion Detection', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# cap.release()
# cv2.destroyAllWindows()
