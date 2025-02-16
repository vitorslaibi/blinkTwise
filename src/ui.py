import PySimpleGUI as ui
import detector
import cv2 as cv
import sqlite3
import components
import db.db as database_creator
from os.path import exists
# import connect_four
# import tic_tac_toe


ui.theme("Reddit")
ui.theme_button_color("#68349C")
size = (400, 400)

dbLocation = '../db/blink_records.db'
connection = None

def welcome_page():
    layout = [[ui.Image("../images/logo_light.png", subsample=3)],
              [ui.Text("Welcome!", pad=((0, 0), (0, 25)), font=('Arial', 18))],
              [  # ui.Text("Existing User", pad=((25, 0), (0, 5))),
                  ui.Button("Login", pad=((0, 50), (0, 10)), font=('Arial', 12)),
                  # ui.Text("New User", pad=((25, 0), (0, 5))),
                  ui.Button("Create Account", pad=((225, 0), (0, 10)), font=('Arial', 12))]]

    return ui.Window('Welcome', layout, element_justification='center', finalize=True)


# This Ui menu is more of a testing ground, making sure things work
def start_menu():
    layout = [[ui.Image("../images/logo_light.png", subsample=3)],
              [ui.Button("Start"), ui.Button("Connect 4"),
               ui.Button("Tic-Tac-Toe")],
              [ui.Button("Settings"), ui.Button("Test Alarm")],
              [ui.Text("Choose a config: "),
               ui.DropDown(values=["Student", "Placeholder", "Placeholder"], default_value="Student", readonly=True)]]

    return ui.Window('BlinkTwise', layout, element_justification='center', finalize=True)


def alarm_window():
    layout = [[ui.Text("Are you still there?")],
              [ui.Button('End'), ui.Button('Continue')]]

    return ui.Window('Alarm Dialog', layout, element_justification='center', finalize=True)


def main():
    disable_alarms = False
    disable_activities = False

    start = welcome_page()
    register = None
    login = None
    settings = None
    profile = None
    if exists(dbLocation):
        global connection
        connection = sqlite3.connect(dbLocation)
        print("Loaded From memory")
    else:
        print("Created DB")
        database_creator.create_database()
        connection = sqlite3.connect(dbLocation)
    cursor = connection.cursor()

    while True:
        window, event, values = ui.read_all_windows()

        if window == start:
            if event == ui.WIN_CLOSED:
                start.close()
                break

            if event == "Login":
                start.hide()
                login = components.login_screen()

            if event == "Create Account":
                start.hide()
                register = components.register_screen()

        if window == profile:
            if event == "Start Blink Analysis":
                if (values["Primary Gaze"] or values["Reading"] or values["Conversational"]):
                    profile.minimize()
                    cam = cv.VideoCapture(0)
                    if values["Primary Gaze"]:
                        detector.main(cursor, cam,
                                      cursor.execute('''SELECT * FROM settings WHERE system_mode = "gaze"''').fetchone())
                    if values["Reading"]:
                        detector.main(cursor, cam,
                                      cursor.execute('''SELECT * FROM settings WHERE system_mode = "reading"''').fetchone())
                    if values["Conversational"]:
                        detector.main(cursor, cam, cursor.execute(
                            '''SELECT * FROM settings WHERE system_mode = "conversational"''').fetchone())
                else:
                    components.prompt("Error", "Please select a system mode to configure the detector")

            if event == ui.WIN_CLOSED:
                start.close()
                break

                # Open settings and hide the main menu
            if event == 'Settings':
                settings = components.settings()

            if event == "Help":
                components.prompt("Help",
                                  "\n To end your session and return to the home page: click 'Logout'."
                                  "\n To begin blink analysis: click 'Start Blink Analysis'."
                                  "\n To open the settings menu: click 'Settings'"
                                  "\n You must select a primary activity in order to begin blink analysis."
                                  "\n Primary Activity Examples:"
                                  "\n 'Reading' indicates that you are mostly reading information and not conversing "
                                  "with anyone or watching videos."
                                  "\n 'Misc' indicates your are engaging in miscellaneous activities including reading, "
                                  "watching videos, or just relaxing."
                                  "\n 'Interacting' indicates that you are engaging in verbal conversation.")

            if event == "Logout":
                profile.close()
                start.un_hide()

        if window == settings:
            if event in (ui.WIN_CLOSED, 'Cancel'):
                settings.close()
            # Toggle for Disable Alarms (does not save option on exit)
            if event == "DISABLE ALARMS":
                disable_alarms = not disable_alarms
                if disable_alarms:
                    settings["DISABLE ALARMS"].update(
                        image_filename="../images/on_toggle.png")
                else:
                    settings["DISABLE ALARMS"].update(
                        image_filename="../images/off_toggle.png")

            # Toggle for Disable Activities (does not save option on exit)
            if event == 'DISABLE ACTIVITIES':
                disable_activities = not disable_activities
                if disable_activities:
                    settings["DISABLE ACTIVITIES"].update(
                        image_filename="../images/on_toggle.png")
                else:
                    settings["DISABLE ACTIVITIES"].update(
                        image_filename="../images/off_toggle.png")

            if event == "Start Calibration":
                cam = cv.VideoCapture(0)
                detector.main(cursor, cam, cursor.execute('''SELECT * FROM settings WHERE system_mode = "calibration"''').fetchone())

        if window == register and event in ("Register", "Go Back"):
            register.close()
            start.un_hide()

        if event == "Submit":
            login.close()
            # add code to verify username and password in db
            profile = components.home()

        if event == "Main Menu":
            login.close()
            start.un_hide()

    connection.commit()
    connection.close()
    start.close()


if __name__ == '__main__':
    main()
