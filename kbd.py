#!/usr/bin/env python3
import time
import random
import sys
from pynput.keyboard import Controller
from pynput.keyboard import Key

keyboard = Controller()  # Create the controller

def type_string_with_delay(string):
    for character in string:  # Loop over each character in the string
        keyboard.type(character)  # Type the character
        delay = random.uniform(0, .1)  # Generate a random number between 0 and 10
        time.sleep(delay)  # Sleep for the amount of seconds generated
    keyboard.type('\n')

type_string_with_delay(sys.argv[1])
