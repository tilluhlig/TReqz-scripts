from pylatexenc.latexencode import utf8tolatex
import xml.etree.ElementTree as ET
import Requirements
import sys


def cleanXhtml(text:str):
	if not Requirements.xmlHelper.xml_utils.stringIsWellFormedXml(text):
		return text

	text=text.strip()
	xmlTree = ET.fromstring(text)
	cleanedHtml = ET.tostring(xmlTree, encoding='utf8', method='text')
	text = cleanedHtml.decode("utf-8")
	return text
		
def tex_escape(text):
	"""
		:param text: a plain text message
		:return: the message escaped to appear correctly in LaTeX
	"""
	return utf8tolatex(text)

def startCommandlinePrint(text):
	sys.stdout.write(text)
	sys.stdout.flush()

def endCommandlinePrint():
	print("")

def commandlinePrint(text):
	# remove old data
	sys.stdout.write("".ljust(len(text), "\x08"))
	
	# print new text
	sys.stdout.write(text)
	sys.stdout.flush()

def fillLeftWithZeros(text:str, newLength:int):
	return text.zfill(newLength)