import numpy as np
import cv2
import tensorflow as tf

IMG_SIZE = 64

modelo = tf.keras.models.load_model(
    "identify_open_hands.keras"
)

# abre webcam
camera = cv2.VideoCapture(0) # 0 para câmera do note e 1 para webcam

contador = 0

while True:

    ret, frame = camera.read()

    contador += 1

    if contador % 10 == 0:

        img = cv2.resize(
            frame,
            (IMG_SIZE, IMG_SIZE)
        )

        img = img.astype(
            "float32"
        ) / 255.0

        img = np.expand_dims(
            img,
            axis=0
        )

        pred = modelo.predict(
            img,
            verbose=0
        )[0]

        classe = np.argmax(pred)

        print("\nProbabilidades:")
        print("Open hand:", pred[0])
        print("No open hand:", pred[1])

        pred = np.max(pred)

        if classe == 0:
            texto = f"OPEN HAND ({pred:.2f})"

        else:
            texto = f"NO OPEN HAND ({pred:.2f})"

        cv2.putText(
            frame,
            texto,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.imshow(
            "Open hand classification",
            frame
        )

        # ESC para sair
        if cv2.waitKey(1) & 0xFF == 27:
            break

camera.release()
cv2.destroyAllWindows()