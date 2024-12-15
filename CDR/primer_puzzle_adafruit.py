from adafruit_pn532.i2c import PN532_I2C
import board
import busio
import binascii
import time

class RfidReader:
    def __init__(self):
        # Inicializaciï¿½n del bus I2C
        i2c = busio.I2C(board.SCL, board.SDA)

        # Inicializar el lector PN532 con I2C
        self.pn532 = PN532_I2C(i2c, debug=False)

        # Configurar el PN532 para leer tarjetas NFC
        self.pn532.SAM_configuration()
        #print("\f")
        #print("PN532 initialized and ready: waiting for an NFC object...")

    def read_uid(self):
        #print("Waiting for an NFC object...")

        # Intentar leer la tarjeta durante 10 segundos
        start_time = time.time()
        while (time.time() - start_time) < 10:  
            uid = self.pn532.read_passive_target(timeout=0.5)

            if uid:
                #print("Card detected!")
                # Convertir el UID de binario a hexadecimal
                uid_hex = binascii.hexlify(uid).decode("utf-8").upper()
                #print(f"UID: {uid_hex}")
                return uid_hex  # Retornar el UID como string

            time.sleep(0.1)  

        #print("NO NFC card detected in 10 seconds, the time has expired")
        return None
