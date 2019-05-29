import machine
import time
from tinkerlib import Buzzer

buzzer = Buzzer(machine.Pin(16))
quarter_note = 100

buzzer.tone(2637, quarter_note)
buzzer.tone(2637, quarter_note)
time.sleep_ms(quarter_note)
buzzer.tone(2637, quarter_note)
time.sleep_ms(quarter_note)
buzzer.tone(2093, quarter_note)
buzzer.tone(2637, quarter_note)
time.sleep_ms(quarter_note)
buzzer.tone(3136, quarter_note)
time.sleep_ms(quarter_note)
time.sleep_ms(quarter_note)
time.sleep_ms(quarter_note)
buzzer.tone(1568, quarter_note)
time.sleep_ms(quarter_note)
time.sleep_ms(quarter_note)
time.sleep_ms(quarter_note)
buzzer.noTone()
