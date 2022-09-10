import os
import cv2
import pickle
import numpy as np
from PIL import Image
from tqdm import tqdm


# Get file paths
def train_model():
    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # image_dir = os.path.join(BASE_DIR, 'images')

    image_dir = 'images'

    face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    current_id = 0
    label_ids = {}
    y_labels = []
    x_train = []

    # Locate images
    for root, dirs, files in os.walk(image_dir):
        for file in tqdm(files):
            if file.endswith("png") or file.endswith("jpg") or file.endswith("jpeg") or file.endswith("JPG"):
                path = os.path.join(root, file)
                label = os.path.basename(root)  # root.replace(" ", "-")

                if label in label_ids:
                    pass
                else:
                    label_ids[label] = current_id
                    current_id += 1

                id_ = label_ids[label]
                pil_image = Image.open(path).convert("L")  # turns into grayscale
                image_array = np.array(pil_image, "uint8")  # turn into numpy array, former final_image
                faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)

                for (x, y, w, h) in faces:
                    roi = image_array[y:y + h, x:x + w]
                    x_train.append(roi)
                    y_labels.append(id_)

    with open("Persistence Files/labels.pickle", 'wb') as f:
        pickle.dump(label_ids, f)

    recognizer.train(x_train, np.array(y_labels))
    recognizer.save("trainer.yml")

