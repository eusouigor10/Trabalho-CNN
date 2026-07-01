#include <Servo.h>
Servo servoMotor;

// configuração de Pinos
const int pinoVermelho = 2; 
const int pinoAmarelo = 3;
const int pinoVerde = 4;
const int pinoServo = 5;
const int pinoPot = A0;

// variáveis de Controle
int potencia;
int pausa;
int pausaDividida;
unsigned long tempoAnterior = 0;
int estado = 0; 

void setup() {
  Serial.begin(9600); // comunicação com o Python
  servoMotor.attach(pinoServo);
  servoMotor.write(0);

  pinMode(pinoVermelho, OUTPUT);
  pinMode(pinoAmarelo, OUTPUT);
  pinMode(pinoVerde, OUTPUT);
}

void loop() {
  unsigned long agora = millis();
  
  // leitura do potenciômetro e cálculo do tempo padrão
  potencia = 749;
  
  if(potencia < 150) pausa = 1000;
  else if(potencia < 300) pausa = 2000;
  else if(potencia < 450) pausa = 3000;
  else if(potencia < 600) pausa = 4000;
  else if(potencia < 750) pausa = 5000;
  else if(potencia <= 900) pausa = 6000;
  else pausa = 7000;

  pausaDividida = pausa / 3;
   
  // lógica da porta serial
  if (Serial.available() > 0) {
    char caractereRecebido = Serial.read();
    
    // se receber 'P' do Python, estiver no verde
    if (caractereRecebido == 'P' && estado == 1) {
      estado = 2;          // pula para o amarelo por segurança
      tempoAnterior = agora; // reseta o tempo para o amarelo durar o tempo exato
    }
  }

  // máquina de estados
  switch(estado) {
    case 0: // VERMELHO
      digitalWrite(pinoVermelho, HIGH);
      digitalWrite(pinoAmarelo, LOW);
      digitalWrite(pinoVerde, LOW);
      servoMotor.write(0); 

      if (agora - tempoAnterior >= pausa) {
        tempoAnterior = agora;
        estado = 1; // vai abrir
      }
      break;

    case 1: // VERDE
      digitalWrite(pinoVermelho, LOW);
      digitalWrite(pinoAmarelo, LOW);
      digitalWrite(pinoVerde, HIGH);
      servoMotor.write(90); 

      if (agora - tempoAnterior >= pausa) {
        tempoAnterior = agora;
        estado = 2; // vai começar a fechar
      }
      break;

    case 2: // AMARELO
      digitalWrite(pinoVermelho, LOW);
      digitalWrite(pinoAmarelo, HIGH);
      digitalWrite(pinoVerde, LOW);
      servoMotor.write(0); 

      if (agora - tempoAnterior >= pausaDividida) {
        tempoAnterior = agora;
        estado = 0; // fechou
      }
      break;
  }
}