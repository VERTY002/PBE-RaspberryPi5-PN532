
#primer programa per part del client 
#actualment no funciona com hauria de funcionar, no hem pogut comprobar el correcte funcionament del codi ja que té 
#errors i no es connecta amb el servidor entre altres coses.


import sys  
import threading
import gi
import json
import requests
from i2clcd import i2clcd
from primer_puzzle_adafruit import RfidReader
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib

class CourseManager(Gtk.Grid):

	# Inicialitzador de la classe
	def __init__(self):
    	super().__init__()
    	self.set_size_request(-1, 20)
    	self.userName = None
    	self.uid = None
    	self.create_button()
    	self.create_entry()
    	self.lcd = i2clcd(1,0x27,20)  # Inicialitza la pantalla LCD
    	self.login()

	# Crea el botó de logout
	def create_button(self):
    	self.button = Gtk.Button(label='Logout')
    	self.attach(self.button, 1, 0, 1, 1)
    	estil = self.button.get_style_context()
    	estil.add_class("button_style")
    	self.button.connect("clicked", lambda button: self.login())
    
	# Crea el camp d'entrada de text
	def create_entry(self):
    	self.entry = Gtk.Entry()
    	self.entry.set_placeholder_text("Enter your query:")
    	self.entry.connect("activate", lambda entry: self.metodeThread(uid=self.uid))
    	self.attach(self.entry, 0, 0, 1, 1)

	# Procediment de login
	def login(self):
    	print("login...")
    	self.label = Gtk.Label(label="apropi la targeta")
    	self.attach(self.label, 0, 1, 1, 1)
    	self.label.show()

    	# Llegeix la targeta RFID
    	self.reader = RfidReader()
    	self.uid = self.reader.read_uid()
    	print(self.uid)
    	self.label.set_text(self.uid)

    	# Fa una sol·licitud al servidor amb el UID
    	url = "http://10.42.0.230:8080/server.php/uid"
    	headers = {'uid': self.uid}
    	response = requests.get(url, headers=headers)
   	 
    	if response.status_code == 200:
        	self.userName = response.text.strip()
        	self.lcd.clear() 
        	self.lcd.print(self.userName)
    	else:
        	self.userName = None
        	print("Error: no s'ha pogut obtenir el nom d'usuari del servidor")

    	if self.userName is not None:
        	print(self.userName[0])  
    	else:
        	print("No s'ha obtingut un nom d'usuari vàlid.")

    	self.label.destroy()
    	self.show_all()

	# Creem un fil per consultar el servidor de manera concurrent
	def metodeThread(self, uid):
    	text = self.entry.get_text()
    	thread = threading.Thread(target=self.consultarServer, args=(text, uid))  # Passa el text i el UID
    	thread.start()
    
	# Consulta al servidor
	def consultarServer(self, text, uid):
    	request = text
    	self.req = request.split("?")[0]
    	url = "http://10.42.0.230:8080/server.php/{}".format(request)
    	headers = {'uid': uid}
    	try:
        	response = requests.get(url, headers=headers)
        	print("STATUS: {}, url: {}".format(response.status_code, url))
        	if response.status_code == 200:
            	result = response.text
            	GLib.idle_add(self.update_ui, result)
        	else:
            	print("Error en la respota: ", response.status_code)
    	except requests.exceptions.RequestException as e:
        	print(f"Error en la solicitud: {e}")

	# Actualitza la interfície d'usuari amb els resultats de la consulta
	def update_ui(self, result):
    	try:
        	matriu = json.loads(result)
    	except json.decoder.JSONDecodeError as e:
        	print("Error al decodificar JSON:", e)
        	return
   	 
    	for widget in self.get_children():
        	if widget is not self.entry and widget is not self.button:
            	widget.destroy()

    	if self.req == 'marks':
        	labels = ['subject', 'name', 'mark']
    	elif self.req == 'timetables':
        	labels = ['day', 'hour', 'subject', 'room']
    	elif self.req == 'tasks':
        	labels = ['date', 'subject', 'name']
        
    	win.__init__()

    	for row, person in enumerate(matriu):
        	for col, key in enumerate(labels):
            	if row == 0:
                	label = Gtk.Label(label=key)
                	estil = label.get_style_context()
                	estil.add_class("personalitzar")
                	self.attach(label, col, 3, 1, 1)
            	value = person[key]
            	label = Gtk.Label(label=value)
            	estil = label.get_style_context()
            	estil.add_class("personalitzar")
            	self.attach(label, col, row + 5, 1, 1)
            	label.set_hexpand(True)
    	win.show_all()

class MyWindow(Gtk.Window):
	# Inicialitzador de la finestra principal
	def __init__(self):
    	super().__init__(title='Course Manager')
    	self.set_default_size(800, 500)
    	self.connect("destroy", Gtk.main_quit)

# main
if __name__ == '__main__':
	win = MyWindow()
	win.__init__()
	win.show_all()
	course_manager = CourseManager()
	css_provider = Gtk.CssProvider()
	css_provider.load_from_path("style.css")

	win.add(course_manager)
	screen = Gdk.Screen.get_default()
	style_context = Gtk.StyleContext()
	style_context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
	Gtk.main()

