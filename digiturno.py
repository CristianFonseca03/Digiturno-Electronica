import RPi.GPIO as GPIO
import time

led1 = [('g', 40), ('f', 38), ('a', 36), ('b', 32),
        ('e', 26), ('d', 24), ('c', 22)]
led2 = [('g', 19), ('f', 15), ('a', 13),
        ('b', 11), ('e', 7), ('d', 5), ('c', 3)]
numbers = [
    ('a', 'b', 'c', 'd', 'e', 'f'),
    ('b', 'c'),
    ('a', 'b', 'g', 'e', 'd'),
    ('a', 'b', 'g', 'c', 'd'),
    ('f', 'g', 'b', 'c'),
    ('a', 'f', 'g', 'c', 'd'),
    ('a', 'f', 'g', 'c', 'd', 'e'),
    ('a', 'b', 'c'),
    ('a', 'b', 'c', 'd', 'e', 'f', 'g'),
    ('a', 'b', 'c', 'd', 'f', 'g')
]

reset = 12
minus = 16
more = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(reset, GPIO.IN)
GPIO.setup(minus, GPIO.IN)
GPIO.setup(more, GPIO.IN)


def setupLed1():
    for port in led1:
        GPIO.setup(port[1], GPIO.OUT)


def setupLed2():
    for port in led2:
        GPIO.setup(port[1], GPIO.OUT)


def statusLed(port, status):
    GPIO.output(port, status)


def turnOnAllLeds():
    for led in led1:
        statusLed(led[1], True)
    for led in led2:
        statusLed(led[1], True)


def turnOffAllLeds():
    for led in led1:
        statusLed(led[1], False)
    for led in led2:
        statusLed(led[1], False)


def turnOffOneLed(led):
    for port in led:
        statusLed(port[1], False)


def createNumber(ledNumber, number):
    turnOffOneLed(ledNumber)
    for i in range(10):
        if number == i:
            for letter in numbers[i]:
                for led in ledNumber:
                    if led[0] == letter:
                        statusLed(led[1], True)


def createNumber2Leds(led1, led2, number):
    if number < 10:
        createNumber(led1, 0)
        createNumber(led2, number)
    else:
        decenas = number / 10
        unidades = number % 10
        createNumber(led1, decenas)
        createNumber(led2, unidades)


def titileoNumber2Leds(led1, led2, number):
    for i in range(3):
        turnOffAllLeds()
        time.sleep(.5)
        createNumber2Leds(led1, led2, number)


def digiTurno():
    contador = 0
    titileoNumber2Leds(led1, led2, contador)
    while True:
        if GPIO.input(reset):
            contador = 0
            print("-"*20+" RESET "+"-"*20)
            titileoNumber2Leds(led1, led2, contador)
            print("Numero actual = "+str(contador))
            time.sleep(.3)
        if GPIO.input(more):
            print("Numero actual = "+str(contador))
            createNumber2Leds(led1, led2, contador)
            time.sleep(.3)
            if contador < 99:
                contador += 1
            else:
                contador = 0
        if GPIO.input(minus):
            if contador == 0:
                contador = 99
            else:
                contador -= 1
            print("Numero actual = "+str(contador))
            createNumber2Leds(led1, led2, contador)
            time.sleep(.3)


def main():
    setupLed1()
    setupLed2()
    turnOffAllLeds()
    try:
        print("Presione un boton para continuar")
        digiTurno()
    except (KeyboardInterrupt, SystemExit):
        GPIO.cleanup()


if __name__ == "__main__":
    main()
