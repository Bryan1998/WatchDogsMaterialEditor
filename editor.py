import re, zlib
import xml.etree.ElementTree as ET
from tkinter import *; from tkinter import filedialog

def byteswap(s):
    s = re.findall('..', s)
    h = ''.join(list(reversed(s)))
    return hex(int('0x' + h, 16))

def crc32b(s):
    h = format(zlib.crc32(bytes(s, 'utf-8')), 'x')
    return byteswap(h)

def readxml(f):
    tree = ET.parse(f)
    root = tree.getroot()
    parameters = [[],[]]
    for parameter in root.findall('parameter'):
        name = parameter.get('name')
        type = parameter.get('type')
        parameters[0].append([crc32b(name)])
        parameters[1].append([crc32b(type)])
    return parameters[0]

def readmat(filename):
    global shader
    with open(filename, mode='rb') as file:
        file.seek(0x48)
        name = file.read(0x17).rstrip(b'\0').decode('ascii', errors='ignore')
        name = re.sub(r'[^\w=]', '', name)
    with open(filename, mode='rb') as file:
        file.seek(0x60)
        shader = file.read(0x1B).rstrip(b'\0').decode('ascii', errors='ignore')
        shader = re.sub(r'[^\w=]', '', shader)
    return [name, shader]

def btn():
    global matfile, matfolder
    matfile = filedialog.askopenfilename(initialdir = ".", title = "Select file", filetypes = (("Watch Dogs Material File", ".material.bin"),))
    matfolder = filedialog.askdirectory(initialdir = ".", title = "Select directory")

window = Tk()

btn_mat = Button(window, text="Open Files", command=btn)
btn_mat.grid(column=0, row=0)

window.mainloop()

print(readmat(matfile))
print(readxml(matfolder + '/' + shader + '.xml'))
