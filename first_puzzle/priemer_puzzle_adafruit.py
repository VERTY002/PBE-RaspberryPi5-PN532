from adafruit_pn532.i2c import PN532_I2C
import board
import busio
import binascii  
import time 

class RfidReader:

    def __init__(self):
        # ii2c bus inizialization
        i2c = busio.I2C(board.SCL, board.SDA)

        # initialize the lector Pn532 with i2c
        self.pn532 = PN532_I2C(i2c, debug=False)

        # set up the PN532 so it can read NFC cards
        self.pn532.SAM_configuration()
        print("\f")
        print("PN532 initialized and ready.")

    def read_uid(self):
        print("Waiting for an NFC object...")

        # try to read the card for 10 seg
        start_time = time.time()
        while (time.time() - start_time) < 10:  
            uid = self.pn532.read_passive_target(timeout=0.5)  # waiting time between reads

            if uid:
                # convert binary to hex
                uid_hex = binascii.hexlify(uid).decode("utf-8").upper()
                return uid_hex  # uid_hex is a string

            time.sleep(0.1)  # little pause in order to not overload the procesor

        print("NO NFT card detected in 10 seconds, the time has expired")
        return None

if __name__ == "__main__":

    rf = RfidReader()
    uid = rf.read_uid()

    if uid:  # if the UID is not null or None, shows the UID
        print("An NFT device (card/keychain) was found")
        print(f"Respective UID: {uid}")
