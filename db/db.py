import sqlite3


def create_database():
    connection = sqlite3.connect('../db/blink_records.db')
    cursor = connection.cursor()

    # Build database
    cursor.execute('''CREATE TABLE IF NOT EXISTS system_settings(
                      system_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                      alertness_threshold DECIMAL(3, 3) NOT NULL,
                      alarm_default BOOLEAN,
                      allow_alarm_disable BOOLEAN
                  )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS settings(
                      settings_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                      blink_threshold DECIMAL(2, 3) NOT NULL,
                      alert_min DECIMAL(3, 3),
                      alert_max DECIMAL(3, 3),
                      system_mode INTEGER,
                      FOREIGN KEY (system_mode) REFERENCES system_settings(system_id)
                  )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS user_profile(
                      user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                      username VARCHAR(32) NOT NULL,
                      age INTEGER(3),
                      settings_id INTEGER,
                      FOREIGN KEY (settings_id) REFERENCES settings(settings_id)
                  )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS session(
                      session_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER NOT NULL,
                      begin_time TIMESTAMP,
                      end_time TIMESTAMP,
                      total_blinks INTEGER,
                      prompts_given INTEGER,
                      alerts_given INTEGER,
                      FOREIGN KEY (user_id) REFERENCES user_profile(user_id)
                  )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS blink_records(
                      blink_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                      start_time TIMESTAMP NOT NULL,
                      end_time TIMESTAMP,
                      session_id INTEGER NOT NULL,
                      FOREIGN KEY (session_id) REFERENCES session(session_id)
                  )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS prompt_type(
                      type_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                      display_name VARCHAR(32) NOT NULL
                  )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS user_prompts(
                      prompt_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                      display_name VARCHAR(32) NOT NULL,
                      description VARCHAR(256),
                      activation_threshold DECIMAL(3,3) NOT NULL,
                      prompt_type INTEGER NOT NULL,
                      action_required BOOLEAN,
                      FOREIGN KEY (prompt_type) REFERENCES prompt_type(type_id)
                  )''')

    # Create default settings
    cursor.executemany('''INSERT INTO settings VALUES (?, ?, ?, ?, ?)''',
                       [(0, 3, -1, -1, "calibration"),
                        (1, 3.5, 1.4, 14.4, "reading"),
                        (2, 5, 8, 21.0, "gaze"),
                        (3, 2.3, 10.5, 32.5, "conversational")])

    connection.commit()
    connection.close()
