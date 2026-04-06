from machine import Pin,ADC,PWM
import time
import network
from umqtt.robust import MQTTClient
import ujson
from machine import Pin
import dht
import time
from time import sleep
import utime
sistem_aktiviran = True
ventilator = Pin(19, Pin.OUT)
ventilator.value(1)
previous_state = 0
# Uspostavljanje WiFI konekcije
nic = network.WLAN(network.STA_IF)
nic.active(True)
nic.connect('Lab220', 'lab220lozinka')

while not nic.isconnected():
    print("Čekam konekciju ...")
    time.sleep(5)

print("WLAN konekcija uspostavljena")
ipaddr = nic.ifconfig()[0]

print("Mrežne postavke:")
print(nic.ifconfig())
pir = Pin(18, Pin.IN)
pot = ADC(28)
ledica = PWM(16)
dht_sensor = dht.DHT11(Pin(15))
ledica.duty_u16(0)
bijelaLampica=Pin(20,Pin.OUT)
bijelaLampica.value(0)
ledica.freq(5000)
t1 = Pin(0, Pin.IN, Pin.PULL_DOWN)
blokirano = False
D1 = Pin(4, Pin.OUT)
D2 = Pin(5, Pin.OUT)
D3 = Pin(6, Pin.OUT)
D4 = Pin(7, Pin.OUT)

A = Pin(8, Pin.OUT)
B = Pin(9, Pin.OUT)
C = Pin(10, Pin.OUT)
D = Pin(11, Pin.OUT)
E = Pin(12, Pin.OUT)
F = Pin(13, Pin.OUT)
G = Pin(14, Pin.OUT)
DP = Pin(15, Pin.OUT)

kolona1 = Pin(0, Pin.OUT)
kolona2 = Pin(1, Pin.OUT)
kolona3 = Pin(2, Pin.OUT)
kolona4 = Pin(3, Pin.OUT)

red1 = Pin(21, Pin.IN, Pin.PULL_DOWN)
red2 = Pin(22, Pin.IN, Pin.PULL_DOWN)
red3 = Pin(26, Pin.IN, Pin.PULL_DOWN)
red4 = Pin(27, Pin.IN, Pin.PULL_DOWN)


def led2(brojac2, k1):
    A.on()
    B.on()
    C.on()
    D.on()
    E.on()
    F.on()
    G.on()
    for i in range(0, 50, 10):
        B.off()
        C.off()
        D1.off()
        D4.on()
        time.sleep_ms(2)
        D1.on()
        D2.off()
        time.sleep_ms(2)
        D2.on()
        D3.off()
        time.sleep_ms(2)
        D3.on()
        D4.off()
        time.sleep_ms(2)
        D4.on()
        B.off()
        C.off()
        time.sleep_ms(200)


def led(brojac1):
    if brojac1 == 0:
        A.off()
        B.off()
        C.off()
        D.off()
        E.off()
        F.off()
        G.on()

    elif brojac1 == 1:
        A.on()
        B.off()
        C.off()
        D.on()
        E.on()
        F.on()
        G.on()

    elif brojac1 == 2:
        A.off()
        B.off()
        C.on()
        D.off()
        E.off()
        F.on()
        G.off()

    elif brojac1 == 3:
        A.off()
        B.off()
        C.off()
        D.off()
        E.on()
        F.on()
        G.off()

    elif brojac1 == 4:
        A.on()
        B.off()
        C.off()
        D.on()
        E.on()
        F.off()
        G.off()

    elif brojac1 == 5:
        A.off()
        B.on()
        C.off()
        D.off()
        E.on()
        F.off()
        G.off()

    elif brojac1 == 6:
        A.off()
        B.on()
        C.off()
        D.off()
        E.off()
        F.off()
        G.off()

    elif brojac1 == 7:
        A.off()
        B.off()
        C.off()
        D.on()
        E.on()
        F.on()
        G.on()

    elif brojac1 == 8:
        A.off()
        B.off()
        C.off()
        D.off()
        E.off()
        F.off()
        G.off()

    elif brojac1 == 9:
        A.off()
        B.off()
        C.off()
        D.off()
        E.on()
        F.off()
        G.off()

    elif brojac1 == 10:
        A.off()
        B.off()
        C.off()
        D.off()
        E.off()
        F.off()
        G.on()

# Start the main loop
k = [0, 0, 0, 0]
b = [0, 0, 0, 0]
ispravno = False
ispravni = [2, 3, 5, 8]
pozicije = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
brojac = 0

brojpogresnihpokusaja = 0
DP.on()

buzzer = Pin(17, Pin.OUT)
def alarm_za_vlagu():
    for _ in range(10):
        buzzer.value(1)
        sleep(0.4)
        buzzer.value(0)
        sleep(0.2)

# Funkcija za ton uspjeha (dva kratka beepa)
def success_tone():
    for _ in range(2):
        buzzer.value(1)
        sleep(0.1)
        buzzer.value(0)
        sleep(0.1)

# Funkcija za ton greške (tri spora beepa)
def error_tone():
    for _ in range(3):
        buzzer.value(1)
        sleep(0.3)
        buzzer.value(0)
        sleep(0.3)


def sub(topic, msg):
    # Added debug prints
   
    try:
        parsed = ujson.loads(msg)
        led_status = parsed.get("led") # Renamed 'led' to 'led_status' to avoid conflict with led() function
        stanje = parsed.get("stanje")
        print(f"Parsirani podaci: led_status={led_status}, stanje={stanje}")

        global blokirano
        global brojpogresnihpokusaja
        global brojac

        if topic == b'lab/odgovor':
            if stanje == "Da":
                blokirano = False
                brojpogresnihpokusaja = 0
                brojac = 0
                print("Odblokirano komandom sa MQTT")
           
           
    except ValueError as e:
        print(f"!!! GREŠKA PARSIRANJA JSON-a na temi '{topic.decode()}': '{msg.decode()}' - {e}")
    except Exception as e:
        print(f"Opća greška u sub funkciji: {e}")

# Uspostavljanje konekcije sa MQTT brokerom
mqtt_conn = MQTTClient(client_id='mqttx_fa819b76', server='195.130.59.221', user='', password='', port=1883)
mqtt_conn.set_callback(sub)
mqtt_conn.connect()
mqtt_conn.subscribe(b"lab/led")
mqtt_conn.subscribe(b"lab/odgovor")
mqtt_conn.subscribe(b"lab/vent")
mqtt_conn.subscribe(b"lab/ventilator")


print("Konekcija sa MQTT brokerom uspostavljena")
while True:
    mqtt_conn.check_msg()

    if blokirano:
        greska_msg = ujson.dumps({"greska": "Lozinka je 3 puta unesena pogresno! Potvrdite da ste to Vi kako bi odobrili ponovni unos."})
        mqtt_conn.publish(b'lab/led', greska_msg)
        print("Zabranjen unos!!")
        for j in range(200):
            D4.on()
            led(b[0])
            D1.off()
            time.sleep_ms(2)
            D1.on()
            led(b[1])
            D2.off()
            time.sleep_ms(2)
            D2.on()
            led(b[2])
            D3.off()
            time.sleep_ms(2)
            D3.on()
            led(b[3])
            D4.off()
            time.sleep_ms(2)
        b = [0, 0, 0, 0]

        kolona1.value(0)
        kolona2.value(0)
        kolona3.value(1)
        kolona3.value(0)

        if red4.value() == 1:
            print("Reset preko tastera #")
            blokirano = False
            brojpogresnihpokusaja = 0
            brojac = 0
            time.sleep_ms(500) # Debounce
        else:
            continue

    if k[0] == 10:
        for j in range(0, 5):
            D4.on()
            led(k[0])
            D1.off()
            time.sleep_ms(2)
            D1.on()
            led(k[1])
            D2.off()
            time.sleep_ms(2)
            D2.on()
            led(k[2])
            D3.off()
            time.sleep_ms(2)
            D3.on()
            led(k[3])
            D4.off()
            time.sleep_ms(2)
            D1.on()
            D2.on()
            D3.on()
            D4.on()
            time.sleep_ms(500)
        error_tone()
        k = [0, 0, 0, 0]

    D4.on()
    led(k[0])
    D1.off()
    time.sleep_ms(2)
    D1.on()
    led(k[1])
    D2.off()
    time.sleep_ms(2)
    D2.on()
    led(k[2])
    D3.off()
    time.sleep_ms(2)
    D3.on()
    led(k[3])
    D4.off()
    time.sleep_ms(2)

    if brojac == 4:
        brojac = 0

    for i in range(0, 16, 4):
        kolona1.value(pozicije[i])
        kolona2.value(pozicije[i + 1])
        kolona3.value(pozicije[i + 2])
        kolona3.value(pozicije[i + 3])

        if red1.value() == 1:
           
            led(i // 4 + 1)
            k[brojac] = (i // 4 + 1)
            brojac += 1
            time.sleep_ms(200)

        elif red2.value() == 1:
           
            led(4 + i // 4)
            k.insert(brojac, (i // 4 + 4))
            brojac += 1
            time.sleep_ms(200)

        elif red3.value() == 1:
           
            led(7 + i // 4)
            k.insert(brojac, (i // 4 + 7))
            brojac += 1
            time.sleep_ms(200)

        elif red4.value() == 1:
           
            if kolona2.value() == 1:
                led(0)
                k.insert(brojac, 0)
                brojac += 1
                time.sleep_ms(200)

            elif kolona3.value() == 1:
                for j in range(0, 4):
                    if k[j] != ispravni[j]:
                       
                        k[0] = 10
                        k[1] = 10
                        k[2] = 10
                        k[3] = 10
                        brojpogresnihpokusaja += 1
                        break
                brojac = 0
                if j == 3:
                    brojpogresnihpokusaja = 0
                    k = [0, 0, 0, 0]
                    led2(10, ispravni)
                    DP.on()
                    ispravno = True
    if ispravno and not blokirano:
        success_tone()
    mqtt_conn.check_msg()

    while ispravno and not blokirano:
        mqtt_conn.check_msg()
        current_state = pir.value()

        kolona1.value(0)
        kolona2.value(0)
        kolona3.value(1) # taster #
        kolona3.value(0)

        if red4.value() == 1:
           
            mqtt_conn.publish(b'lab/deaktivacija', ujson.dumps({"status": "Taraba pritisnuta tokom aktivnog sistema – omogućavamo unos za deaktivaciju"}))
            novi_pin = []
            brojac_novog_pina = 0
            time.sleep_ms(500)

            # Omogućavamo unos 4 cifre
            while brojac_novog_pina < 4:
                for i in range(0, 16, 4):
                    kolona1.value(pozicije[i])
                    kolona2.value(pozicije[i + 1])
                    kolona3.value(pozicije[i + 2])
                    kolona3.value(pozicije[i + 3])

                    if red1.value() == 1:
                        cifra = (i // 4 + 1)
                        led(cifra)
                        novi_pin.append(cifra)
                        brojac_novog_pina += 1
                        time.sleep_ms(200)

                    elif red2.value() == 1:
                        cifra = (i // 4 + 4)
                        led(cifra)
                        novi_pin.append(cifra)
                        brojac_novog_pina += 1
                        time.sleep_ms(200)

                    elif red3.value() == 1:
                        cifra = (i // 4 + 7)
                        led(cifra)
                        novi_pin.append(cifra)
                        brojac_novog_pina += 1
                        time.sleep_ms(200)

                    elif red4.value() == 1 and kolona2.value() == 1:
                        led(0)
                        novi_pin.append(0)
                        brojac_novog_pina += 1
                        time.sleep_ms(200)

            print("Uneseni PIN za deaktivaciju:", novi_pin)

            # Provjera PIN-a
            if novi_pin == ispravni:
               
               
                blokirano = False
                brojpogresnihpokusaja = 0
           
                ledica.duty_u16(0)
                ispravno = False
                brojac = 0
                k = [0, 0, 0, 0]
                success_tone()
                break
           
            else:
               
           
                error_tone()
                time.sleep(1)

        procitano = pot.read_u16()
        ledica.duty_u16(procitano)
        if current_state == 1 and previous_state == 0:
            print("Pokret DETEKTOVAN -> Palim alarm!")
            for _ in range(5):  # alarm traje ~5 sekundi (5x1s)
                buzzer.value(1)
                utime.sleep(0.5)
                buzzer.value(0)
                utime.sleep(0.5)
        elif current_state == 0 and previous_state == 1:
            print("Pokret PRESTAO -> Gasim alarm.")
            previous_state = current_state
        utime.sleep(0.1)
       
        try:
            dht_sensor.measure()
            temperatura = dht_sensor.temperature()
            vlaga = dht_sensor.humidity()
            if temperatura > 27:
                ventilator.value(0)
                greska_msg = ujson.dumps({"greska": "Temperatura je iznad 27 stepeni.Palimo ventilator!"})
                mqtt_conn.publish(b'lab/ventilator', greska_msg)
                mqtt_conn.publish(b'lab/led', ujson.dumps({ "temperature": temperatura, "humidity": vlaga }))
               
            else:
              ventilator.value(1)
              print("Temperatura:", temperatura, "°C")
              print("Vlaga:", vlaga, "%")

            if vlaga > 31:
                print("Vlažnost je iznad 33, palimo lampicu")
                bijelaLampica.value(1)
            else:
                bijelaLampica.value(0)
             

        except OSError as e:
            print("Greška u čitanju sa senzora:", e)
           
        time.sleep(0.5)

    if brojpogresnihpokusaja == 3:
        blokirano = True