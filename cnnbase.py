import os
import zipfile
import numpy as np
import gdown
import cv2

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from tensorflow.keras.layers import RandomBrightness, RandomContrast
from tensorflow.keras.callbacks import EarlyStopping

from sklearn.metrics import classification_report, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import RandomFlip, RandomRotation, RandomBrightness

IMG_SIZE = 64
CHANNELS = 3 # RGB images


import shutil

def download_dataset(url, arquivo_zip="open_closed_hand.zip"):
    # se a pasta antiga já existir, deleta ela inteira para sumir com duplicatas
    pasta_destino = os.path.join(".", "open_closed_hand")
    if os.path.exists(pasta_destino):
        print("Limpando resíduos de datasets antigos...")
        shutil.rmtree(pasta_destino)

    gdown.download(
        url,
        arquivo_zip,
        fuzzy=True,
        quiet=False
    )
    zip_referencia = zipfile.ZipFile(arquivo_zip,'r')
    zip_referencia.extractall(".")
    zip_referencia.close()
    return pasta_destino

def extrair_atributos(caminho_imagem):
    img = cv2.imread(caminho_imagem)
    if img is None:
      return None
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img.astype('float32') / 255.0 # normaliza os pixel para valores entre [0, 1]
    return img

def carregar_dados(caminho_base):
    X = []
    y = []

    # hand = 0
    pasta_hand = os.path.join(caminho_base, "hand")
    for arquivo in os.listdir(pasta_hand):
        if arquivo.lower().endswith(('.png', '.jpg', '.jpeg')):
            caminho_completo = os.path.join(pasta_hand, arquivo)
            atributos = extrair_atributos(caminho_completo)
            if atributos is not None:
                X.append(atributos)
                y.append(0)

    # closed hand = 1
    pasta_closed_hand = os.path.join(caminho_base, "closed_hand")
    for arquivo in os.listdir(pasta_closed_hand):
        if arquivo.lower().endswith(('.png', '.jpg', '.jpeg')):
            caminho_completo = os.path.join(pasta_closed_hand, arquivo)
            atributos = extrair_atributos(caminho_completo)
            if atributos is not None:
                X.append(atributos)
                y.append(1)

    X = np.array(X)
    y = np.array(y)
    return X, y

def dividir_dados(X, y, porcentagem_teste, random_state):
  X_treino, X_teste, y_treino, y_teste = train_test_split(
      X,
      y,
      test_size=porcentagem_teste,
      stratify = y,
      random_state=random_state)
  return X_treino, X_teste, y_treino, y_teste


#softmax

def gerar_modelo():
    modelo = Sequential()

    # rotação horizontal por conta do dedão
    modelo.add(RandomFlip("horizontal", input_shape=(IMG_SIZE, IMG_SIZE, CHANNELS)))
    modelo.add(RandomRotation((-0.25, 0.25))) # giro de aproximadamente 30 graus no ângulo das mãos

    # bloco 1 - Mais simples e direto
    modelo.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
    modelo.add(MaxPooling2D((2, 2)))

    # bloco 2
    modelo.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
    modelo.add(MaxPooling2D((2, 2)))

    # vetorização e camada densa
    modelo.add(Flatten())
    modelo.add(Dense(64, activation='relu'))
    modelo.add(Dropout(0.3)) # evitar overfitting

    # saída (2 classes: hand = 0, closed_hand = 1)
    modelo.add(Dense(2, activation='softmax'))

    return modelo

def avaliacao(modelo, X_teste, y_teste):
    # obter previsões
    y_prob = modelo.predict(X_teste)
    y_pred = np.argmax(y_prob, axis=1)

    # imprimir Métricas (Precision, Recall, F1-Score)
    print("\n--- Relatório de Classificação ---")
    print(classification_report(y_teste, y_pred, target_names=['Hand', 'Closed Hand']))

    # matriz de Confusão Visual
    cm = confusion_matrix(y_teste, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Hand', 'Closed Hand'])

    # exibir o gráfico
    disp.plot(cmap=plt.cm.Blues)
    plt.title("Matriz de Confusão")
    plt.show()

dataset_url = "https://drive.google.com/file/d/1iprPrIJpMQBhgbvKMJkT0tMtbSyeppUC/view?usp=sharing"
base_dataset_path = download_dataset(dataset_url)
X, y = carregar_dados(base_dataset_path)

# separação dos dados
X_treino, X_teste, y_treino, y_teste = dividir_dados(X, y, 0.2, 25)

modelo = gerar_modelo()

opt_adam = Adam(learning_rate=0.0005)

modelo.compile(optimizer = opt_adam, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

modelo.fit(X_treino, y_treino, epochs=20, batch_size=32, shuffle=True, verbose=1, validation_split=0.2)
modelo.save('identify_open_hands.keras')
avaliacao(modelo, X_teste, y_teste)
