import math, os, sys, re, svgwrite

from HTMLParser import HTMLParser

mm = 3.54
height = 250*mm
width  = 250*mm

##x1 = -47.498
##y1 = -5.08
##x2 = -43.18
##y2 = -19.304
##angle = math.radians(45)
##
##chord = math.sqrt(((x1-x2)*(x1-x2))+((y1-y2)*(y1-y2)))
##radius = (chord/math.sin(angle/2))
##print chord
##print radius
##
class wire:
    def __init__(self):
        self.x1 = 1.0
        self.x2 = 1.0
        self.y1 = 1.0
        self.y2 = 1.0
        self.width = 0.254
        self.layer = 20
        self.angle = 1.0
        self.type = ['line']

    def display(self):
        print self.x1, self.y1, self.x2, self.y2, self.width, self.layer, self.angle, self.type

class circle:
    def __init__(self):
        self.x = 1.0
        self.y = 1.0
        self.radius = 1.0
        self.width = 0.254
        self.layer = 20
        self.type = ['circle']

    def display(self):
        print self.x, self.y, self.radius, self.width, self.layer, self.type

class BrdParser(HTMLParser):
    pathData = []
    parseBoard = 1
    parsePlain = 1

    def handle_starttag(self, tag, attrs):
        if tag == "board":
            self.parseBoard = 1
        if tag == "plain":
            self.parsePlain = 1
        if (self.parseBoard + self.parsePlain) == 2:
            if tag == "wire":
                self.pathData.append(wire())
                for i in attrs:
                    if i[0] == 'x1':
                        self.pathData[-1].x1 = float(i[1])
                    if i[0] == 'x2':
                        self.pathData[-1].x2 = float(i[1])
                    if i[0] == 'y1':
                        self.pathData[-1].y1 = -1.0*float(i[1])
                    if i[0] == 'y2':
                        self.pathData[-1].y2 = -1.0*float(i[1])
                    if i[0] == 'width':
                        self.pathData[-1].width = float(i[1])
                    if i[0] == 'layer':
                        self.pathData[-1].layer = int(i[1])
                    if i[0] == 'curve':
                        self.pathData[-1].type[0] = 'curve'
                        self.pathData[-1].angle = float(i[1])
            if tag == "circle":
                self.pathData.append(circle())
                for i in attrs:
                    if i[0] == 'x':
                        self.pathData[-1].x = float(i[1])
                    if i[0] == 'y':
                        self.pathData[-1].y = -1.0*float(i[1])
                    if i[0] == 'radius':
                        self.pathData[-1].radius = float(i[1])
                    if i[0] == 'width':
                        self.pathData[-1].width = float(i[1])
                    if i[0] == 'layer':
                        self.pathData[-1].layer = int(i[1])

    def handle_endtag(self, tag):
        if tag == "plain":
            self.parsePlain = 0
                

##brdData = """<wire x1="-47.498" y1="-5.08" x2="-43.18" y2="-19.304" width="0.254" layer="20" curve="45"/>"""
##brdData = """<wire x1="0" y1="0" x2="3.81" y2="0" width="0.254" layer="16" curve="-180"/>"""
filename = sys.argv[1]
##filename = "border_only.brd"
layers = []

f = open(filename, 'r')   ## Open the file in question.
brdData = f.read()       ## Read the data into a holding structure.
f.close()                 ## Be a good resident of the OS and close the file.

parser = BrdParser()
parser.feed(brdData)
paths = []
print sys.argv
try:
    for i, arg in enumerate(sys.argv):
        if (i < 2):
            pass
        else:
            layers.append(int(arg))
except:
    pass

print layers
for i in parser.pathData:
   ## i.display()
    ##stroke_string = ['#' + hex(int(i.layer))[2:4] + '0000']
    if layers != []:
        if i.layer in layers:
            print "YES"
        if i.layer not in layers:
            continue
    stroke_string = ['#' + '{:02X}'.format(int(i.layer)) + '0000']
    ##print stroke_string       
    if i.type[0] == 'curve':
        chord = math.sqrt(((i.x1-i.x2)*(i.x1-i.x2))+((i.y1-i.y2)*(i.y1-i.y2)))
        angle = math.radians(i.angle)
        radius = (abs(chord/math.sin(angle/2)))/2
        newp = svgwrite.path.Path(fill = 'none', stroke_width = i.width*mm, stroke = stroke_string[0])
        newp.push('M', i.x1*mm, (i.y1*mm)+height)
        if i.angle < 0:
            newp.push_arc((i.x2*mm, (i.y2*mm)+height), 0, radius*mm, large_arc = False, angle_dir = '+', absolute = True)
        else:
            newp.push_arc((i.x2*mm, (i.y2*mm)+height), 0, radius*mm, large_arc = False, angle_dir = '-', absolute = True)
            
        paths.append(newp)

    elif i.type[0] == 'line':
        newp = svgwrite.path.Path(fill = 'none',stroke_width = i.width*mm, stroke = stroke_string[0])
        newp.push('M', i.x1*mm, (i.y1*mm)+height)
        newp.push('L', i.x2*mm, (i.y2*mm)+height)
        paths.append(newp)

    elif i.type[0] == 'circle':
        newp = svgwrite.shapes.Circle((i.x*mm, (i.y*mm)+height), i.radius*mm, fill = 'none',stroke_width = i.width*mm, stroke = stroke_string[0])
        paths.append(newp)


dwg = svgwrite.Drawing(filename[:-3]+'svg', profile='tiny', size = (width, height))
for i in paths:
    dwg.add(i)
dwg.save()

foo = input("Press enter key to quit.")
print foo

##
##
##scriptName = filename[:-4] + ".txt"
##with open(scriptName, 'w') as f:
##    for path in paths:
##        f.write(path)
##        f.write('\n')
