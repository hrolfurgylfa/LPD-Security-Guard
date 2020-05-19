# Standard
import os
from time import sleep

# Community
import keyboard as keyboard_input
import pyautogui as keyboard_output
import pyperclip as clipboard


# Get the input list
officer_list = input("Insert the officer list\n>>>").split(";")


# Add the exit for safety
keyboard_input.add_hotkey("esc", lambda: exit())


# Input the list
keyboard_input.wait("space")

# Input the list length
keyboard_output.write(str(len(officer_list)))
keyboard_output.press("enter")
keyboard_output.press("tab")

# Input the names in the list
for name in officer_list:
    clipboard.copy(name)
    sleep(.1)
    keyboard_output.hotkey("ctrl", "v")
    keyboard_output.press("tab")