import cv2
import os
from pop_ups import employee_already_exist_message, collect_finished_message


def collect_photos(id, cam, cascade):
    count = 0

    nameID = str(id)
    path = 'images/' + nameID

    isExist = os.path.exists(path)

    if isExist:
        employee_already_exist_message()
        return
    else:
        os.makedirs(path)

    while True:
        r, f = cam.read()
        faces = cascade.detectMultiScale(f, 1.3, 3)

        # Display Text
        cv2.putText(f, 'Photos Collected: ' + str(count) + '/1000', (7, 445),
                    cv2.FONT_HERSHEY_TRIPLEX, 0.7, (64, 127, 57), 2)

        for x, y, w, h in faces:
            count = count + 1
            name = './images/' + nameID + '/' + str(count) + '.png'
            cv2.imwrite(name, f[y:y + h, x:x + w])
            cv2.rectangle(f, (x, y), (x + w, y + h), (0, 255, 0), 3)

        cv2.imshow('Collect Employee Photos', f)
        cv2.waitKey(1)

        if count > 1000:
            collect_finished_message()
            cv2.destroyAllWindows()
            break
