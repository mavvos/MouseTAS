"""
Like AutoHotkeys but simpler and allows clicks inside game windows.

Made for TASing mouse-only games,
    by @mavvos on GitHub.
"""
import re
import time
import autoit
import keyboard
import PySimpleGUI as sg

# Holds user inputs added to Listbox
list_holder = []


def main():
    call_hotkeys()
    interface()


def interface():
    sg.theme("DarkBlue3")
    layout = [
        [
            sg.Text("X", pad=(15, 0)),
            sg.Text("Y", pad=(15, 0)),
            sg.Text("Seconds"),
            sg.Text("Mouse:LCTRL, Start:F8, Stop:F9"),
        ],
        [
            sg.InputText(size=4),
            sg.InputText(size=4),
            sg.InputText(size=4),
            sg.Text("Position: (0, 0)", pad=(28, 0), key="MouseText"),
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
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        elif event == "Move":
            if len(values[0]) > 0 and len(values[1]) > 0:
                moveto = f"Move To: {values[0], values[1]}"
                list_holder.append(moveto)
                window["List"].Update(list_holder)

        elif event == "Sleep":
            if len(values[2]) > 0:
                sleeper = f"Sleep for {values[2]}"
                list_holder.append(sleeper)
                window["List"].Update(list_holder)

        elif event == "Click":
            list_holder.append("Click")
            window["List"].Update(list_holder)

        elif event == "Delete":
            if len(list_holder) > 0:
                list_holder.pop()
                window["List"].Update(list_holder)

        elif event == "Control_L:17":
            window["MouseText"].Update(f"Position: {autoit.mouse_get_pos()}")

        elif event == "Export":
            file_save = sg.popup_get_file(
                "",
                default_path="My_Mouse_Record",
                save_as=True,
                no_window=True,
                file_types=(("All TXT Files", "*.txt"), ("All Files", "*.*")),
            )
            if file_save != "":
                with open(file_save, "w") as file:
                    for line in list_holder:
                        file.write(f"{line}\n")

        elif event == "Import":
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
    """Setup default hotkeys"""
    keyboard.add_hotkey("f8", start)
    keyboard.add_hotkey("f9", lambda: print("Stopping"))


def start():
    """Start enacting commands from list_holder"""
    for command in list_holder:
        if command[0] == "M":  # Move
            coords = re.findall(r"\d+", command)
            autoit.mouse_move(int(coords[0]), int(coords[1]))
        elif command[0] == "C":  # Click
            autoit.mouse_click()
        elif command[0] == "S":  # Sleep
            timing = re.findall(r"\d+", command)
            time.sleep(int(timing[0]))


if __name__ == "__main__":
    main()
