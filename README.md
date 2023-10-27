<head>
  <h2 align="center">
    🐀 MouseTAS 🏃
  </h2>
  <h3 align="center">
    A simple script with a simple interface to allow quick and easy control of your mouse.
  </h3>
</head>

#### Note
If you just want to control your mouse, you're probably best of just using [AutoHotkey](https://www.autohotkey.com/).
But if for some reason it doesn't work, you don't want to use it or if your clicks aren't registering in some window, feel free to try this software, these are the reasons why it exists.

## 🤔 Demonstration
[[# TO DO]]

## 🔨 How It Works
MouseTAS controls your Mouse with simple commands to Move, Click and Wait.
Uses the *autoit*, *keyboard* and *PySimpleGUI* modules.

## 👨‍🏫 What You Need
Make sure you have Python and all [requirements](https://github.com/mavvos/MouseTAS/blob/main/requirements.txt) installed:
```
pip install -r requirements.txt
```

## 🗃 Export/Import
You can **Import** a saved command list from a text file. After that the data will appear in your Interface's Listbox.

To save your progress/command list, use the **Export** button. Commands are saved in a text file in a simple syntax:
```
Move To: ('100', '150')
Sleep for 1
Click
```
You can edit them on the text file itself.
#### Note
The only necessary aspect for a command line to be valid is: the line starts with the command's first letter and coordinates are separated by space, so a file with the following commands is similar to the previous example, if more cryptic while still being valid.
```
M100 150
S1
C
```

## ℹ About
MouseTAS was made to be used in creating Tool-Assisted speedruns. Although, the precision is not great, so the idea was abandoned. You could probably get more precise commands by messing with the mouse speed and finding a middle term with Moving, Sleeping and Clicking.

This software uses the [[# TO DO]] LICENSE.
