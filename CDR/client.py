import threading
import gi
import json
import requests
import time
from primer_puzzle_adafruit import RfidReader
from i2clcd import i2clcd
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Pango, Gdk

class CourseManager(Gtk.Window):
    def __init__(self):
        super().__init__(title="Course Manager")
        self.server = "10.42.0.1" #change if rquired
        self.port = "8080"
        self.timer = None
        self.inactivity_timeout = 50  # 50 seconds inactivity timeout
        self.lcd = i2clcd(1,0x27,20)
        self.lcd.init()
        self.rfid_reader = RfidReader()
        self.uid = None

        #aply css to app
        self.apply_css()
        
        # Window configuration
        self.set_border_width(10)
        self.set_default_size(700, 600)
        self.connect("destroy", self.on_destroy)

        # Main container: using Gtk.Stack to switch between screens
        self.stack = Gtk.Stack()
        self.add(self.stack)

        # Login screen

        self.login_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.login_box.get_style_context().add_class("login-box") 
        self.stack.add_named(self.login_box, "login")

        self.login_label = Gtk.Label(label="PLEASE, LOGIN WITH YOUR UNIVERSITY CARD")
        self.login_label.get_style_context().add_class("login-label")
        self.login_box.pack_start(self.login_label, True, True, 0)

        # Query screen
        self.query_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.query_box.get_style_context().add_class("query-box")  
        self.stack.add_named(self.query_box, "query")

        self.welcome_label = Gtk.Label(label="Welcome")
        self.welcome_label.get_style_context().add_class("welcome-label")
        self.query_box.pack_start(self.welcome_label, False, False, 0)

        self.query_entry = Gtk.Entry()
        self.query_entry.set_placeholder_text("Enter your query")
        self.query_entry.get_style_context().add_class("query-entry")
        self.query_entry.connect("activate", self.on_query)
        self.query_box.pack_start(self.query_entry, False, False, 0)

        self.logout_button = Gtk.Button(label="Logout")
        self.logout_button.get_style_context().add_class("logout-button")
        self.logout_button.connect("clicked", self.on_logout)
        self.query_box.pack_start(self.logout_button, False, False, 0)

        # Initially show login screen
        self.stack.set_visible_child_name("login")

        # Start RFID reader thread
        self.reader_thread = threading.Thread(target=self.read_uid_thread, daemon=True)
        self.reader_thread.start()

        self.show_all()

    def apply_css(self):

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("styles.css")  # CCS file route

        # Apply CSS to the default screen
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(
            screen,
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def read_uid_thread(self):
        while True:
            uid = self.rfid_reader.read_uid()
            if uid:
                GLib.idle_add(self.authenticate_user, uid)
                
            time.sleep(0.1)

    def authenticate_user(self, uid):
        # Construct the URL to query students table with the specific UID
        self.uid = uid
        url = f"http://{self.server}:{self.port}/server.php/students?uid={uid}"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            user_data = response.json()
            
            if user_data and isinstance(user_data, list) and len(user_data) > 0:
                
                name = user_data[0].get('name', 'Unknown')
                self.current_name = name  # Store the name for later use
                self.update_welcome_screen(name)
            else:
                self.update_login_label("User not found !!TRY AGAIN", "red")
        except requests.exceptions.RequestException as e:
            self.update_login_label(f"Connection error: {str(e)}", "red")
        except ValueError:
            self.update_login_label("Invalid server response", "red")

    def update_welcome_screen(self, name, is_error=False):
        # Default welcome message with name
        welcome_message = f"Hello {name} !!! It's always nice to see you again :)"
        
        if is_error:
            self.welcome_label.set_markup(f'<span foreground="red">Incorrect query. Please try again.</span>')
        else:
            self.welcome_label.set_text(welcome_message)
        
        self.stack.set_visible_child_name("query")
        self.start_inactivity_timer()

    def update_login_label(self, text, color="red"):
        self.login_label.set_markup(f'<span foreground="{color}">{text}</span>')

    def on_query(self, widget):
        query_text = self.query_entry.get_text().strip()
        if query_text:
            url = f"http://{self.server}:{self.port}/server.php/{self.uid}/{query_text}"
            threading.Thread(target=self.perform_query, args=(url,)).start()
        else:
            self.update_welcome_label("Query is empty!", "red")

    
    def perform_query(self, url):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            result = response.json()
            GLib.idle_add(self.on_response, result)
        except requests.exceptions.RequestException as e:
            GLib.idle_add(self.on_response, None)

    def on_response(self, result):

        if hasattr(self, "treeview"):
            self.treeview.destroy()

        # Check if result is None or empty/invalid
        if not result or not isinstance(result, list):
            # Update the welcome label with an error message
            self.update_welcome_screen(self.current_name, is_error=True)
            return

        # If result is valid, create the table and restore welcome message
        keys = list(result[0].keys())
        if not keys:
            self.update_welcome_screen(self.current_name, is_error=True)
            return

        # Restore welcome message
        self.update_welcome_screen(self.current_name)

        # Create table as before
        self.liststore = Gtk.ListStore(*[str] * len(keys))

        for item in result:
            row = [str(item.get(key, "")) for key in keys]
            self.liststore.append(row)

        self.treeview = Gtk.TreeView(model=self.liststore)

        for i, column_title in enumerate(keys):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            column.set_resizable(True)
            column.set_alignment(0.5)
            self.treeview.append_column(column)

        self.treeview.modify_font(Pango.FontDescription("Arial 12"))
        self.treeview.set_rules_hint(True)

        self.query_box.pack_start(self.treeview, True, True, 0)
        self.query_box.show_all()

    def on_logout(self, button):

        self.stop_timer() 
        self.lcd.clear()
        # Reset the UID
        self.uid = None
        # Reset the current name
        self.current_name = None
        # Remove the treeview if it exists
        if hasattr(self, "treeview"):
            self.treeview.destroy()
            del self.treeview
        # Remove the liststore if it exists
        if hasattr(self, "liststore"):
            del self.liststore
        # Reset query 
        self.query_entry.set_text("")
        # Switch back to login screen
        self.stack.set_visible_child_name("login")
        self.login_label.set_text("PLEASE, LOGIN WITH YOUR UNIVERSITY CARD")
        self.welcome_label.set_text("")
        

    def start_inactivity_timer(self):
        self.stop_timer()
        self.timer = GLib.timeout_add_seconds(self.inactivity_timeout, self.on_timeout)

    def on_timeout(self):
        self.on_logout(None)
        self.stop_timer()

    def stop_timer(self):
        if self.timer:
            GLib.source_remove(self.timer)
            self.timer = None

    def on_destroy(self, widget):
        Gtk.main_quit()

def main():
    app = CourseManager()
    Gtk.main()

if __name__ == "__main__":
    main()
