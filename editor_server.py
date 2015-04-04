#!/usr/bin/python
# -*- coding: utf-8 -*- 
'''
http://www.acmesystems.it/python_httpserver
'''
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import re
from PIL import ImageFont, Image, ImageDraw
import textwrap


PORT_NUMBER = 8080


def myDynamicFunc(values):
	from urlparse import urlparse, parse_qs
	
	# from API
	query_components = parse_qs(urlparse(values).query)
	TEXT = query_components.get('text')[0].decode('utf-8')

	# editor
	font = ImageFont.truetype("fonts/centry.ttf", 36, encoding='unic')
	imagePath = "template.jpg"
	imgFile = Image.open(imagePath)
	draw = ImageDraw.Draw(imgFile)
	from_top, h = 100, 30
	lines = textwrap.wrap(TEXT, width = 35)
	y_text = h
	for line in lines:
	    width, height = font.getsize(line)
	    draw.text((20, y_text + from_top), line, (0,0,0), font = font)
	    y_text += (height + 22)

	imgFile.save("result.jpg")


	return { 
		"image": 'http://localhost' + ':'+ str(PORT_NUMBER) + sep + 'result.jpg', 
		"path": values
	}


#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		if self.path == "/":
			self.path = "/index.html"

		try:
			#Check the file extension required and
			#set the right mime type

			sendReply = False
			dynamic = False

			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True
			if None != re.search('.php', self.path):
				mimetype='application/json'
				# mimetype='text/html'
				dynamic = True

			if sendReply == True:
				#Open the static file requested and send it
				f = open(curdir + sep + self.path) 
				self.send_response(200)
				self.send_header('Content-type', mimetype)
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
			elif dynamic == True:
				self.send_response(200)
				self.send_header('Content-type', mimetype)
				self.end_headers()
				self.wfile.write(myDynamicFunc(self.path))
			return


		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()