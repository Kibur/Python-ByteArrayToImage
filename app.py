__author__ = 'Kibur'

import os
import io
import sys
import Image
from gi.repository import Gtk
import hashlib
import base64

class UI:
    # Handlers
    def window_close(self, *args):
	try:
		os.remove(self.filename)

		print 'Removed "' + self.filename + '"'
	except OSError, ose: # No such file or directory
		pass

        Gtk.main_quit(args)

    def on_button_clicked(self, button):
	if self.filename is not 'void':
		os.remove(self.filename)

		print 'Removed "' + self.filename + '"'

		self.filename = 'void'

        textBuffer = self.txtInput.get_buffer()
	start, end = textBuffer.get_bounds()
	data = textBuffer.get_text(start, end, False)

	if data.startswith('0x'):
		data = data[2:]

	try:
		byteArray = bytearray.fromhex(data)
		bytesIO = io.BytesIO(byteArray)
        	image = Image.open(bytesIO)
		msgd5 = hashlib.md5(str(image)).digest()
		encoded = base64.b16encode(msgd5)

		self.filename = encoded + '.png'

		image.save(self.filename)

		print 'Temporary file "' + self.filename + '" created!'

		self.imgOutput.set_from_file(self.filename)
	except ValueError, ve:
		print 'Corrupt data or not an image'
	except IOError, ioe:
		print 'Corrupt data or not an image'
    # ---

    def connectHandlers(self):
        self.window.connect('delete-event', self.window_close)
        self.btnConvert.connect('clicked', self.on_button_clicked)

    def retreiveObjects(self):
        self.window = self.builder.get_object("window1")
        self.txtInput = self.builder.get_object('txtInput')
        self.btnConvert = self.builder.get_object('btnConvert')
        self.imgOutput = self.builder.get_object('imgOutput')

    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("view.glade")

        self.retreiveObjects()
        self.connectHandlers()

        self.window.show()

	self.filename = 'void'

if __name__ == "__main__":
    ui = UI()
    Gtk.main()
