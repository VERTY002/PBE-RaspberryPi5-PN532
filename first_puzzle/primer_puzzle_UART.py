#imports from the pn532pi libraries 
from pn532pi import Pn532I2c #class Pn532I2C to controll the comunicaction via I2C
from pn532pi import Pn532Hsu #to controll the communication via UART
from pn532pi import Pn532, pn532 
import binascii #to convert binary data to haxadecimal data

class RfidReader:     

	def __init__(self):

		#initialize the lector
		PN532_HSU = Pn532Hsu(Pn532Hsu.RPI_MINI_UART) #I also tried with RPI_PL011
		self.nfc = Pn532(PN532_HSU)
		self.nfc.begin() #stars the communication with the PN532 reader
		self.nfc.SAMConfig() #configures the PN532 so it can read a NFT modules
		print("\f")
		print("PN532 initialized and ready.")
	
	def read_uid(self):

		print("Waiting for a NFT target...")
		#success returns a boolean and uid is the UID binary value of the target
		success, uid = self.nfc.readPassiveTargetID(pn532.PN532_MIFARE_ISO14443A_106KBPS)
		if success:

			#convert the uid (binary) to hex and then tu upper letters
			uid_hex= binascii.hexlify(uid).decode("utf-8").upper()
			return uid_hex #uid_hex is a string
		else:

			print("NO NFT card detected, the time has expired")
			return None #the program ends here

if __name__ == "__main__":

	rf = RfidReader()
	uid = rf.read_uid()

	if (uid):  #if uid is not null or None the UID is shown

		print("An NFT device (card/keychain) was found")
		print(f"Respective UID: {uid}")
