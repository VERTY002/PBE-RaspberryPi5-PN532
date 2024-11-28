import gi
import threading
from primer_puzzle_adafruit import RfidReader # Import the class of the card reader
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject, Gdk

class GraphicPuzzle(Gtk.Window):

    def __init__(self):  # All the initializations
        super().__init__(title="Graphic NFC Lector")

        self.set_border_width(8)  # Select the border width
        self.rfid_reader = RfidReader()  # Initialize the lector

        # Create a box , set the orientation and the separation from the buttons
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        # Create a label
        self.label = Gtk.Label()
        self.label.set_size_request(500,100) # Label size
        # Size and color of the text
        self.label.set_markup('<span size="15000" foreground="white">Please, login with your university card</span>')
        self.label.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 1, 1))  # Blue background
        vbox.pack_start(self.label, True, True, 0) # Starts the label

        # Clear button
        clear_button = Gtk.Button.new_with_mnemonic("Clear")
        clear_button.connect("clicked", self.on_clear_clicked)
        vbox.pack_start(clear_button, True, True, 0)

        # Close button
        close_button = Gtk.Button.new_with_mnemonic("Close")
        close_button.connect("clicked", self.on_close_clicked)
        vbox.pack_start(close_button, True, True, 0)

        # Initializes the thread that reads the UID of the card
        self.start_uid_thread(handler = self.handle_uid_result)

    def start_uid_thread(self, handler):
        # Runs the lecture of the card read_uid from another thread
        thread = threading.Thread(target=self.read_uid,args=(handler,) ,daemon=True)
        thread.start()

    def read_uid(self,handler):
        # Calls the method that reads the card (from first_puzzle)
        uid = self.rfid_reader.read_uid()

        #If the card is found, the label is updated
        #This way it wont freeze when you press the clear button
        if uid:  # if UID is not null
            GObject.idle_add(handler, f"UID: {uid}", "red")
        else:  # if UID is null #hamos cambiado self.update_label por handler
            GObject.idle_add(handler , "NO NFC card detected in 10 seconds, the time has expired", "blue")

    def handle_uid_result(self,text,color):

        self.update_label(text,color)

    def update_label(self, text, color):
        # Updates the text and background of the label
        self.label.set_size_request(500,100)
        self.label.set_markup(f'<span size="15000" foreground="white">{text}</span>')
        if color == "red":
            self.label.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 0, 0, 1))
        else:
            self.label.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 1, 1))

    def on_clear_clicked(self, button):
        # Clearing the label and resetting the startup message
        self.label.set_size_request(500,100)
        self.label.set_markup('<span size="15000" foreground="white">Please, login with your university card</span>')
        self.label.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 1, 1))
        # Call the lecture process
        self.start_uid_thread(handler = self.handle_uid_result)

    def on_close_clicked(self, button):
        print("Closing application")
        Gtk.main_quit()

# Create the window and start the graphical interface
win = GraphicPuzzle()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
