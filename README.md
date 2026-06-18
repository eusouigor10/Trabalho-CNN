# 🚦 Semáforo Inteligente com Visão Computacional (CNN)

Este projeto consiste em um protótipo de **Semáforo Inteligente** acionado por pedestres, desenvolvido como requisito para a disciplina de Inteligência Artificial (Ciência da Computação). 

O sistema utiliza uma **Rede Neural Convolucional (CNN)** treinada no Keras/TensorFlow para detectar o gesto de "mão aberta" em tempo real através de uma câmera, simulando a solicitação de travessia de um pedestre.

---

## 📂 Estrutura do Repositório

O projeto é composto por dois arquivos principais que devem permanecer na mesma pasta:  
* `aplicacao_modelo_cnn.py`: Script Python responsável pela captura de vídeo da webcam, processamento dos frames e execução da inferência da rede neural.  
* `identify_open_hands.keras`: Arquivo de modelo que contém a arquitetura e os pesos da CNN treinada.

---

## 🛠️ Pré-requisitos e Ambiente

Para garantir a compatibilidade das versões das bibliotecas (especialmente do TensorFlow), o projeto utiliza um ambiente virtual gerenciado pelo **Anaconda / Miniconda**.

### Requisitos de Software:
* [Miniconda](https://docs.anaconda.com/miniconda/) ou Anaconda instalado.
* [VS Code](https://code.visualstudio.com/) (ou qualquer terminal de sua preferência).
* Uma webcam conectada.

---

## 🚀 Passo a Passo para Execução

Siga as instruções abaixo no terminal do seu VS Code para configurar o ambiente e rodar o projeto:

### 1. Abrir o Terminal do Conda no VS Code  
Para que os comandos do `conda` funcionem, o terminal do VS Code precisa estar integrado ao Anaconda. Se o seu terminal padrão for o do Windows (CMD ou PowerShell) e não reconhecer os comandos:  
1. No VS Code, abra o comando de paletas usando o atalho `Ctrl + Shift + P`.  
2. Digite `Terminal: Select Default Profile` e pressione `Enter`.  
3. Escolha **Command Prompt (Conda)** ou **PowerShell (Conda)** na lista.  
4. Abra um novo terminal (`Ctrl + Shift + '`). Ele deverá iniciar mostrando `(base)` antes do caminho da pasta.  

### 2. Criar o Ambiente Virtual  
Com o terminal correto aberto, crie o ambiente dedicado para o projeto rodando:  
`conda create -n SEMAFORO python=3.11 -y` 

### 3. Ativar o Ambiente  
Sempre antes de instalar pacotes ou executar o script, ative o ambiente criado:  
`conda activate SEMAFORO`  
(O início da linha do seu terminal mudará de (base) para (SEMAFORO)).  

### 4. Instalar as Dependências
Com o ambiente ativo, instale as bibliotecas necessárias para rodar o projeto:  
`pip install tensorflow==2.20.0`     
`pip install opencv-python`  
`conda install -c anaconda pyserial -y`     
Esses comandos referem a instalação do: TensorFlow (v2.20.0), OpenCV para processamento de imagem, PySerial para integração com o hardware do Arduino, respectivamente.  

### 5. Executar a Aplicação  
Navegue até a pasta onde os arquivos do projeto estão salvos. Garanta que o script .py e o arquivo .keras estão juntos na mesma pasta e execute:  
`python aplicacao_modelo_cnn.py`
