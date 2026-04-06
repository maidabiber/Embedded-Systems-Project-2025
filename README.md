# SmartSecuritySystem

Ovaj projekat predstavlja rješenje za pametni sigurnosni sistem, razvijen u sklopu predmeta **Ugradbeni sistemi** na Elektrotehničkom fakultetu Sarajevo (2024/2025), tokom četvrtog semestra.

Sistem kombinuje hardversku kontrolu putem mikrokontrolera i daljinsko upravljanje putem **MQTT** protokola.

## Glavne Funkcionalnosti

- **Autentifikacija:** Unos šifre putem matrične tastature (4x4) uz vizuelni prikaz na 7-segmentnom displeju.
- **Monitoring Okruženja:** Kontinuirano praćenje temperature i vlažnosti vazduha.
- **Automatska Kontrola:** Aktivacija ventilatora na osnovu temperaturnih pragova.
- **Prilagodljivo Osvjetljenje:** Regulacija intenziteta LED diode putem PWM signala i potenciometra.
- **Pametna Detekcija:** Senzor pokreta aktivira zvučni alarm .
- **IoT Integracija:** Slanje podataka na MQTT broker i mogućnost daljinske deblokade sistema putem MQTTX aplikacije.

## Hardverska Konfiguracija

| Komponenta | Pinovi (GPIO) | Opis |
| :--- | :--- | :--- |
| **7-Segmentni Displej** | 4-14 | Multipleksirani prikaz (D1-D4 i A-G) |
| **Matrična Tastatura** | 0-3 (K), 21-27 (R) | Unos šifre uz PullDown otpornike |
| **DHT11 Senzor** | 15 | Senzor temperature i vlažnosti |
| **PIR Senzor** | 18 | Detekcija pokreta |
| **Buzzer** | 17 | Zvučni indikatori i alarm |
| **Ventilator** | 19 | Relej/Motor (Active-LOW) |
| **RGB/LED** | 16 (PWM), 20 | Osvjetljenje i indikacija vlage |
| **Potenciometar** | 28 (ADC) | Kontrola svjetlosti |
