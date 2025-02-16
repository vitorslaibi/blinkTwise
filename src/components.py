import PySimpleGUI as ui


def prompt_window(title, msg):
    layout = [[ui.Text(msg)]]

    return ui.Window(title, layout, element_justification='center', finalize=True)


def prompt(title, msg):
    display = prompt_window(title, msg)
    while True:
        window, event, values = ui.read_all_windows()

        # Closes the user_home window on X
        if window == display and event in (ui.WIN_CLOSED, 'Cancel'):
            display.close()
            break


def login_screen():
    username = ""
    password = ""

    layout = [[ui.Text("User ID: ", pad=((0, 0), (0, 5)), font=('Arial', 14)),
               ui.Input(username)],
              [ui.Text("Password: ", pad=((0, 0), (0, 5)), font=('Arial', 14)),
               ui.Input(password)],
              [ui.Button("Submit", pad=((0, 50), (0, 10)), font=('Arial', 12)),
               ui.Button("Main Menu", pad=((0, 50), (0, 10)), font=('Arial', 12))]]

    return ui.Window('Login', layout, element_justification='center', finalize=True)


def register_screen():
    username = ""
    password = ""

    layout = [[ui.Text("Please Enter a User ID: ", pad=((0, 0), (0, 5)), font=('Arial', 14)),
               ui.Input(username)],
              [ui.Text("Please Enter a Password: ", pad=((0, 0), (0, 5)), font=('Arial', 14)),
               ui.Input(password)],
              [ui.Button("Register", pad=((0, 50), (0, 10)), font=('Arial', 12)),
               ui.Button("Go Back", pad=((0, 50), (0, 10)), font=('Arial', 12))]]

    return ui.Window('Register', layout, element_justification='center', finalize=True)


def settings():
    layout = [[ui.Text("Calibrate User"), ui.Button("Start Calibration")],
              [ui.Text("Disable Alarms"),
               ui.Button('', image_filename="../images/off_toggle.png", key="DISABLE ALARMS",
                         button_color=ui.theme_background_color(), border_width=0)],
              [ui.Text("Disable Activities"),
               ui.Button('', image_filename="../images/off_toggle.png", key="DISABLE ACTIVITIES",
                         button_color=ui.theme_background_color(), border_width=0)],
              [ui.Button("Cancel"), ui.Button("Save")]]

    return ui.Window('Settings', layout, finalize=True)


# This is the user homepage after successful login
def home():
    layout = [[ui.Image("../images/logo_light.png", subsample=3)],
              [ui.Text("Select a Primary Activity:", pad=((0, 0), (0, 0)), font=('Arial', 12)),
               ui.Radio("Reading", 1, font=('Arial', 12), default=False, key="Reading"),
               ui.Radio("Misc", 1, font=('Arial', 12), default=False, key="Primary Gaze"),
               ui.Radio("Interacting", 1, font=('Arial', 12), default=False, key="Conversational")],
              # ui.DropDown(values=["Reading", "Misc", "Interacting"], pad=((0, 25), (0, 0))),
              [ui.Button("Start Blink Analysis", pad=((0, 0), (25, 25)), font=('Arial', 12))],
              [ui.Button("Settings", pad=((0, 10), (25, 25)), font=('Arial', 12)),
               ui.Button("Help", pad=((0, 10), (25, 25)), font=('Arial', 12)),
               ui.Button("Logout", pad=((0, 0), (25, 25)), font=('Arial', 12))]]

    return ui.Window('BlinkTwise', layout, element_justification='center', finalize=True)
