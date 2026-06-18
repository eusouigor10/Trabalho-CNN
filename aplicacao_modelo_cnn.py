import numpy as np
import cv2
import tensorflow as tf
import serial
import time

# --- CONFIGURAÇÃO DA PORTA SERIAL DO ARDUINO ---
# IMPORTANTE: Mude 'COM3' para a porta real que aparecer na sua IDE do Arduino
try:
    arduino = serial.Serial('COM6', 9600, timeout=1)
    time.sleep(2) # Tempo para o Arduino resetar ao conectar
    print("Conexão com o Arduino estabelecida com sucesso!")
except (serial.SerialException, IndexError, Exception) as e:
    print("Não foi possível conectar ao Arduino. O script rodará apenas no modo simulação de vídeo.")
    arduino = None

IMG_SIZE = 64

modelo = tf.keras.models.load_model(
    "identify_open_hands.keras"
)

# abre webcam
camera = cv2.VideoCapture(0) # 0 para câmera do note e 1 para webcam

contador = 0
ultimo_envio = 0

while True:

    ret, frame = camera.read()

    contador += 1
    tempo_atual = time.time()

    if contador % 5 == 0:

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
            # 1. ENVIA O COMANDO PARA O ARDUINO SE ESTIVER CONECTADO
            if arduino and (tempo_atual - ultimo_envio > 4):
                arduino.write(b'P')
                arduino.flush()
                ultimo_envio = tempo_atual

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
if arduino:
    arduino.close()