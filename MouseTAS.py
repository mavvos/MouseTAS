"""
Like AutoHotkey but for mouses,
allows clicks inside game windows.

Made by @mavvos on GitHub.
Repository: https://www.github.com/mavvos/MouseTAS/
"""
import re
import time
import autoit
import keyboard
import PySimpleGUI as sg


list_holder = []  # Hold user commands, same as Listbox
MOUSE_SPEED = 4
# Modules keyboard and PySimpleGUI use different mapping for special keys
HOTKEYS_KEYBOARD = {
    "Start": "F8",
    "Quit": "F9",
}
HOTKEYS_GUI = {
    "Quit": "F9:120",
    "Click": "z",
    "MousePos": "x",
    "MoveTo": "c",
    "Sleep": "v",
    "Delete": "b",
}
INFO = """
------------- How To -------------
Add values to X and Y to
be able to add a 'Move To'
command.

Add value to Seconds to be
able to add a 'Sleep for'
command.

-- Default Hotkeys --
    Start: F8
    Quit: F9
    Get MPosition: X
    Add Click: Z
    Add Move To: C
    Add Sleep: V
    Delete Last: B

-------------- About --------------
This application was made
by @mavvos on GitHub for
creating mouse-only
Tool-Assisted speedruns.

Find this application
and more about it at:

github.com/mavvos/MouseTAS
"""


def main():
    """Start here"""
    call_hotkeys()
    interface()


def interface():
    """Interface with PySimpleGUI"""

    sg.theme("DarkBlue3")
    layout = [
        [
            sg.Text("X", pad=(15, 0)),
            sg.Text("Y", pad=(25, 0)),
            sg.Text("Seconds"),
            sg.Button("ℹ", key="info", pad=(80, 0), size=1),
        ],
        [
            sg.InputText(size=4, key="X_input"),
            sg.InputText(size=4, key="Y_input", pad=(15, 0)),
            sg.InputText(size=4, key="S_input", pad=(5, 0)),
            sg.Text("Mouse Position: (0, 0)", pad=(10, 0), key="MouseText"),
        ],
        [
            sg.Button("Move"),
            sg.Button("Click"),
            sg.Button("Sleep"),
            sg.Button("Delete Last", key="Delete"),
            sg.Button("Export"),
            sg.Button("Import"),
        ],
        [sg.Listbox("", size=(60, 50), key="List")],
    ]

    window = sg.Window(
        "Mouse TASTool",
        layout,
        resizable=True,
        size=(380, 380),
        return_keyboard_events=True,
    )

    while True:
        event, values = window.read(70, timeout_key="GetPosition")
        if event in (sg.WIN_CLOSED, HOTKEYS_GUI["Quit"]):
            break

        if event == "info":
            sg.popup(
                INFO,
                title="INFO",
            )

        elif event == "GetPosition":
            # Continuously called on window.read timeout. Update mouse position
            window["MouseText"].Update(f"Mouse Position: {autoit.mouse_get_pos()}")

        elif event == HOTKEYS_GUI["MousePos"]:
            # On hotkey, add mouse position to X, Y
            window["X_input"].Update(autoit.mouse_get_pos()[0])
            window["Y_input"].Update(autoit.mouse_get_pos()[1])

        elif event in ("Move", HOTKEYS_GUI["MoveTo"]):
            # On click or hotkey, add current X, Y to command list as 'Move To'
            if len(values["X_input"]) > 0 and len(values["Y_input"]) > 0:
                moveto = f"Move To: {values['X_input'], values['Y_input']}"
                list_holder.append(moveto)
                window["List"].Update(list_holder)
                window["List"].Widget.yview_moveto(1)

        elif event in ("Click", HOTKEYS_GUI["Click"]):
            # On click or hotkey, add 'Click' to command list
            list_holder.append("Click")
            window["List"].Update(list_holder)
            window["List"].Widget.yview_moveto(1)

        elif event in ("Sleep", HOTKEYS_GUI["Sleep"]):
            # On click or hotkey, add current Seconds to command list as 'Sleep'
            if len(values["S_input"]) > 0:
                sleeper = f"Sleep for {values['S_input']}"
                list_holder.append(sleeper)
                window["List"].Update(list_holder)
                window["List"].Widget.yview_moveto(1)

        elif event in ("Delete", HOTKEYS_GUI["Delete"]):
            # On click or hotkey, delete last command from command list
            if len(list_holder) > 0:
                list_holder.pop()
                window["List"].Update(list_holder)
                window["List"].Widget.yview_moveto(1)

        elif event == "Export":
            # Export current command list saved as .txt file
            file_save = sg.popup_get_file(
                "",
                default_path="My_Mouse_Recording",
                save_as=True,
                no_window=True,
                file_types=(("All TXT Files", "*.txt"), ("All Files", "*.*")),
            )
            if file_save != "":
                with open(file_save, "w") as file:
                    for line in list_holder:
                        file.write(f"{line}\n")

        elif event == "Import":
            # Import .txt file to command list
            file_import = sg.popup_get_file(
                "",
                no_window=True,
                file_types=(("All TXT Files", "*.txt"), ("All Files", "*.*")),
            )
            if file_import != "":
                list_holder.clear()
                with open(file_import, "r") as file:
                    for line in file:
                        list_holder.append(line)
                window["List"].Update(list_holder)


def call_hotkeys():
    """Setup keyboard hotkeys"""
    keyboard.add_hotkey(HOTKEYS_KEYBOARD["Start"], start)
    keyboard.add_hotkey(HOTKEYS_KEYBOARD["Quit"], lambda: print("Stopping"))


def start():
    """Start enacting commands from list_holder"""
    for command in list_holder:
        if command[0] == "M":  # Move
            coords = re.findall(r"\d+", command)
            autoit.mouse_move(int(coords[0]), int(coords[1]), speed=MOUSE_SPEED)
        elif command[0] == "C":  # Click
            autoit.mouse_click()
        elif command[0] == "S":  # Sleep
            timing = re.findall(r"\d+", command)
            time.sleep(int(timing[0]))


if __name__ == "__main__":
    main()
