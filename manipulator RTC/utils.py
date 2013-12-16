#!/usr/bin/env python

from Tkinter import *
import csv
import sys
import math
import cmath

root = Tk()

class CanvasItem:
    canvas = None
    
    def make_binds(self):
        CanvasItem.canvas.tag_bind(self.id, '<1>', self.drag_start)
        CanvasItem.canvas.tag_bind(self.id, '<Button1-Motion>', self.dragging)
        CanvasItem.canvas.tag_bind(self.id, '<3>', self.rotate_start)
        CanvasItem.canvas.tag_bind(self.id, '<Button3-Motion>', self.rotating)
        CanvasItem.canvas.tag_bind(self.id, '<ButtonRelease-3>', self.save_angle)

    def drag_start(self, event):
        self.x = event.x
        self.y = event.y

        self.center = self.get_center()
        mouse_coordinates = "x = " + str((275 - self.center[1])*2) + ", y = " + str((275 - self.center[0])*2)
        self.canvas.delete("center")
        self.canvas.create_text(75,40,text = mouse_coordinates,tag = "center")

    def dragging(self, event):
        x1 = event.x
        y1 = event.y
        CanvasItem.canvas.move(self.id, x1-self.x, y1-self.y)
        self.x = x1
        self.y = y1

        self.center = self.get_center()
        mouse_coordinates = "x = " + str(int((275 - self.center[1] + 0.5)*2)) + ", y = " + str(int((275 - self.center[0]+0.5))*2)
        self.canvas.delete("center")
        self.canvas.create_text(75,40,text = mouse_coordinates,tag = "center")

    def rotate_start(self,event):
        self.vector = self.get_vector(event)
        self.center = self.get_center()
                
    def rotating(self,event):
        temp_vector = self.get_vector(event)/self.vector
        offset = complex(self.center[0],self.center[1])
        newxy = []
        self.relative_angle = cmath.phase(temp_vector)
        for i in range(0,len(self.coordsnow)-1,2):
            v = temp_vector * (complex(self.coordsnow[i], self.coordsnow[i+1]) - offset) + offset
            newxy.append(v.real)
            newxy.append(v.imag)

        CanvasItem.canvas.coords(self.id,*newxy)

    def get_vector(self,event):
        dx = CanvasItem.canvas.canvasx(event.x) - self.center[0]
        dy = CanvasItem.canvas.canvasy(event.y) - self.center[1]
        try:
            return complex(dx, dy) / abs(complex(dx, dy))
        except ZeroDivisionError:
            return 0.0 # cannot determine angle

    def get_area(self):
        self.coordsnow = CanvasItem.canvas.coords(self.id)
        polygon_area = 0
        polygon = self.coordsnow
        polygon.append(polygon[0])
        polygon.append(polygon[1])       

        for i in range(0,len(polygon)-3,2):
                polygon_area += polygon[i+2]*polygon[i+1]-polygon[i]*polygon[i+3]

        return abs(polygon_area/2)

    def get_center(self):
        polygon_center_x = 0
        polygon_center_y = 0
        polygon_area = self.get_area()
        polygon = self.coordsnow

        for i in range(0,len(polygon)-3,2):
                polygon_center_x += (polygon[i]+polygon[i+2])*(polygon[i]*polygon[i+3]-polygon[i+2]*polygon[i+1])
                polygon_center_y += (polygon[i+1]+polygon[i+3])*(polygon[i]*polygon[i+3]-polygon[i+2]*polygon[i+1])

        return round(polygon_center_x/(6*polygon_area),1),round(polygon_center_y/(6*polygon_area),1)

    def delete(self):
        CanvasItem.canvas.delete(self.id)

    def save_angle(self,event):
        self.angle += self.relative_angle
        self.relative_angle = 0

        if self.angle > 2*math.pi:
            self.angle = self.angle - 2*math.pi

        if self.angle < -2*math.pi:
            self.angle = self.angle + 2*math.pi

#        print math.degrees(self.angle)


    def get_angle(self):

        return math.degrees(self.angle)


class CanvasOval(CanvasItem):
    def __init__(self, x0, y0, x1, y1, **key):
        self.vector = None
        self.center = 0,0
        self.id = CanvasItem.canvas.create_oval(x0, y0, x1, y1,tag = "obj", activefill = "blue",**key)
        self.coordsnow = CanvasItem.canvas.coords(self.id)
        self.make_binds()
        
class CanvasRectangle(CanvasItem):
    def __init__(self, x, y, w, h, **key):
        self.vector = None
        self.relative_angle = 0
        self.angle = 0
        self.center = 0,0
        self.id = CanvasItem.canvas.create_polygon(x,y,x+w,y,x+w,y+h,x,y+h,tag = "obj", activefill = "blue",**key)
        self.coordsnow = CanvasItem.canvas.coords(self.id)
        self.make_binds()

class CanvasPolygon(CanvasItem):
    def __init__(self,*pos, **key):
        self.vector = None
        self.relative_angle = 0
        self.angle = 0
        self.center = 0,0        
        self.id = CanvasItem.canvas.create_polygon(*pos,tag = "obj",activefill = "blue", **key)
        self.coordsnow = CanvasItem.canvas.coords(self.id)
        self.make_binds()

class CanvasTriangle(CanvasItem):
    def __init__(self, x, y, r, color):
        self.vector = None
        self.center = 0,0
        self.id = CanvasItem.canvas.create_polygon(str(x)+'c', str(y-r*SQRT3)+'c', str(x-r)+'c', str(y)+'c',
                                                   str(x+r)+'c', str(y)+'c', fill=color,activefill = "blue",tag = "obj")
        self.coordsnow = CanvasItem.canvas.coords(self.id)
        self.make_binds()

class CanvasText(CanvasItem):
    def __init__(self, *pos, **key):
        self.vector = None
        self.center = 0,0
        self.id = CanvasItem.canvas.create_text(*pos,tag = "obj", **key)
        self.coordsnow = CanvasItem.canvas.coords(self.id)
        self.make_binds()
       

class CanvasCircleNumber(CanvasItem):
    def __init__(self, x, y, num, session):
        s = session + str(num)
        self.circle = CanvasItem.canvas.create_oval('%fc' % (x-0.7), '%fc' % (y-0.7), '%fc' % (x+0.7), '%fc' % (y+0.7),
                                                    width=2, outline='red', fill='#FFFFF0', tag=s)
        self.number = CanvasItem.canvas.create_text(str(x)+'c', str(y)+'c', text=str(num),
                                                    font=('Helvetica', '14', 'bold'), tag=s)
        CanvasItem.canvas.tag_bind(s, '<1>', self.drag_start)
        CanvasItem.canvas.tag_bind(s, '<Button1-Motion>', self.dragging)

    def dragging(self, event):
        x1 = event.x
        y1 = event.y
        CanvasItem.canvas.move(self.circle, x1-self.x, y1-self.y)
        CanvasItem.canvas.move(self.number, x1-self.x, y1-self.y)
        self.x = x1
        self.y = y1

class Model_list:

    obj = None
    initial_pos = None
    
    def __init__(self):
        self.obj = []
        self.initial_pos = []

    def add_model(self,model_object):
        self.obj.append(model_object)
        self.initial_pos.append(model_object.get_center())

    def del_model():
        pass

    def return_obj(self):
        return self.obj

    def return_initial_pos(self):
        return self.obj
    
class Data:
    def __init__(self):
        self.coords = None
        self.type = None
        self.f = open("obj_list.csv",'wt')
    def save(self,model_list):

        try:
            writer = csv.writer(self.f)
            for i in range(len(model_list)):
                tmp = model_list[i].canvas.coords(model_list[i].id)
                self.type = model_list[i].canvas.gettags(model_list[i].id)
                self.coords = [int(round(n)) for n in tmp]
                self.coords.append(self.type)
                writer.writerow(self.coords)
                   
        finally:
            self.f.close()

    def load(self):
        pass

    def get(self):
        pass
#        for i in range(len(model_list)):
#            self

class Orochi_Canvas:

    canvas = None

    def __init__(self,):

        self.canvas.bind('<Motion>',self.oncanvas_move)
        
        self.canvas.create_rectangle(200,200,200+20,200+50,fill = "blue")
        self.canvas.create_rectangle(10, 10, 540, 510)
        self.canvas.create_arc(25+10,25+10,515,515,start = -70, extent = 320, fill = 'palegreen')

        self.canvas.create_rectangle(240-90/2+25+10,240+90/2+25+10,240+90/2+25+10,240+25+10,fill = 'khaki')
        Orochi_Canvas.canvas.create_arc(240-90/2+25+10,240+90/2+25+10,240+90/2+25+10,240-90/2+25+10,start = 0, extent = 180, fill = 'khaki')

        self.canvas.create_line(275,10,275,510)
        self.canvas.create_line(10,275,540,275)

        for i in range(-300,300,50):
                self.canvas.create_line(275-5,275-i,275+5,275-i)
                self.canvas.create_text(275+5+10,275-i+5,text = i*2)

        for i in range(-300,300,50):
                self.canvas.create_line(275-i,275-5,275-i,275+5)
                self.canvas.create_text(275-i+5,275+5+10,text = i*2)

        self.canvas.bind()
        
        self.canvas.create_line(275,275,275,275-50,arrow = 'last', fill = 'blue')
        self.canvas.create_line(275,275,275-50,275,arrow = 'last', fill = 'blue')
        self.canvas.create_text(275+7,275-50+20,text = 'x')
        self.canvas.create_text(275-50+20,275-7,text = 'y')

        self.canvas.create_text(75,25,text = "Center of Gravity")

        pass
    
    def oncanvas_move(self,event):
        self.canvas.delete("text")
        mouse_coordinates = str((275-event.y)*2) + "," + str((275-event.x)*2)
        self.canvas.create_text(event.x + 30,event.y -10,text = mouse_coordinates,tag="text")

        
class test():
        

    canvasgroup = Canvas(root, width = 550, height = 520)
    model_list = Model_list()
    data = Data()
    CanvasItem.canvas = canvasgroup
    Orochi_Canvas.canvas = canvasgroup
    orochi_canvas = Orochi_Canvas()

    for i in range(20):
        model_list.add_model(CanvasRectangle(30, 50 + i*10, 20,5, fill="red", width=0))

    model_list.add_model(CanvasPolygon(50.0, 50.0, 150.0, 50.0, 150.0, 150.0, 50.0, 150.0,100.0,100.0, fill="red", width=0))
    
    data.save(model_list.obj)

    
    canvasgroup.pack(expand = True,padx=5, pady=5, side=LEFT)
    root.mainloop()

if __name__ == "__main__":
    test()

