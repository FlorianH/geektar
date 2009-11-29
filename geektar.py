#!/usr/bin/env python
#
#      ___ ___ ___ _  _______ _   ___   
#     / __| __| __| |/ /_   _/_\ | _ \  
#    | (_ | _|| _|| ' <  | |/ _ \|   /  
#     \___|___|___|_|\_\ |_/_/ \_\_|_\ 
#
#
# Copyright (C) 2009 Florian Herlings (florianherlings.de)
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
# Version:      0.1
# Date:         29.11.2009
# Depends on:   PyGame, winsound

import winsound
import os
import sys
import pygame
from pygame import locals



console_ascii_logo = """\
      ___ ___ ___ _  _______ _   ___   
     / __| __| __| |/ /_   _/_\ | _ \  
    | (_ | _|| _|| ' <  | |/ _ \|   /  
     \___|___|___|_|\_\ |_/_/ \_\_|_\ 
   ------------------------------------
                                  v.01
  """




class Guitar(object):
  """ The Guitar class abstracts the whole functionality so
      it becomes relatively easy to use it.
      
      The basic functionality is that you pass a pygame joystick
      event to the "event" method and the method decides if it changes
      the guitars sound or waits for other input (like firing the
      trigger event).
  """


  def __init__(self):
    """ Sets the instances variables to 0. """
    self.button0 = 0
    self.button1 = 0
    self.button2 = 0
    self.button3 = 0
    self.button4 = 0
    self.trigger = 0
    self.freq = 0

  def event(self, e):
    self.trigger = 0
    
    if e.type == pygame.locals.JOYBUTTONDOWN:
      self.__dict__['button%s' % self.correct_button(e)] = 1

    elif e.type == pygame.locals.JOYBUTTONUP:
      self.__dict__['button%s' % self.correct_button(e)] = 0

    elif e.type == pygame.locals.JOYHATMOTION:
      if e.value[1] != 0:
        self.do_trigger(e)
  
  def correct_button(self, e):
    """ For some reason, the button 2 and 3 on the guitar
        hero controller are mixed up. Pass the ButtonUp
        or ButtonDown event to this method and it will fix
        it. This method always returns the number of the
        pressed button, not an event.
    """
    if e.button == 2:
      return 3
    elif e.button == 3:
      return 2
    else:
      return e.button
  
  def do_trigger(self, e):
  
    self.trigger = True
    
    if self.button0 == 1: self.button0 = 2
    if self.button1 == 1: self.button1 = 2
    if self.button2 == 1: self.button2 = 2
    if self.button3 == 1: self.button3 = 2
    if self.button4 == 1: self.button4 = 2   
    
    print self


  def update(self):
  
    self.freq = 0
    if self.button0 == 2: self.freq = self.freq + 110
    if self.button1 == 2: self.freq = self.freq + 146
    if self.button2 == 2: self.freq = self.freq + 196
    if self.button3 == 2: self.freq = self.freq + 246
    if self.button4 == 2: self.freq = self.freq + 329

    if self.trigger:
      self.freq += 20

    try:
      winsound.Beep(self.freq, 30)   
    except ValueError:
      self.freq = 0
    
    
  def __str__(self):
    """ The __str__ method is called whenever the class' instance is
        supposed to be printed to the console. It shows rather simple
        but at least somewhat visual representation of the instances
        current data and output.
    """
    return "  BUTTONS: [%i] [%i] [%i] [%i] [%i] | TRIGGER: (%i) | FREQ: %i" % (self.button0, self.button1, self.button2, self.button3, self.button4, self.trigger, self.freq)





if __name__ == "__main__":
  
  pygame.init()
  pygame.joystick.init() # main joystick device system
  
  print console_ascii_logo


  try:
    j = pygame.joystick.Joystick(0) # create a joystick instance
    j.init() # init instance
    print 'Enabled joystick: ' + j.get_name()
  except pygame.error:
    print 'no joystick found.'


  g = Guitar()

  while 1:
    for e in pygame.event.get():
      if e.type != pygame.locals.JOYAXISMOTION:
        g.event(e)
    g.update()
