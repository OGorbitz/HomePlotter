import json
import tkinter as tk
from SaePoint import SaePoint
from SaeLength import SaeLength


class PointManager(object):
    OriginPoint = SaePoint(0, 0)
    
    Points = []

    def Init():
        PointManager.Points.append(SaePoint(1,0))
        GUI.init()
    
    def Loop():
        GUI.loop()
    
    def AddPoint(point):
        PointManager.Points.append(point)
        GUI.updatePoints()
    def RemovePoint(index):
        PointManager.Points.pop(index)
        GUI.updatePoints()
    def PrintDistances():
        for p in PointManager.Points:
            d1 = PointManager.OriginPoint.distance(p)
            d2 = PointManager.BasisPoint.distance(p)
            print( "(" + SaeLength(p.x).__str__() + "," + SaeLength(p.y).__str__() + ") " + d1.__str__() + " | " + d2.__str__())

    def SavePoints():
        with open("plot.json", "w", encoding="utf-8") as f:
            json.dump(PointManager.Points, f, default=lambda o: o.encode(), ensure_ascii=False, indent=4)
            f.close()
    def LoadPoints():
        pts = []
        try:
            with open("plot.json", "r", encoding="utf-8") as f:
                pts = json.load(f)
                f.close()
        except:
            return

        PointManager.Points = []

        for pt in pts:
            PointManager.Points.append(SaePoint(pt["x"], pt["y"]))
        GUI.updatePoints()



class GUI(object):
    window: tk.Tk
    canvas: tk.Canvas
    nameList: tk.Listbox
    pointList: tk.Listbox
    distList1: tk.Listbox
    distList2: tk.Listbox

    deleteButton: tk.Button
    canvasSize = 500
    currIndex = -2
    textError = tk.StringVar
    textXF = tk.StringVar
    textXI = tk.StringVar
    textYF = tk.StringVar
    textYI = tk.StringVar

    entryXF = tk.Entry
    entryXI = tk.Entry
    entryYF = tk.Entry
    entryYI = tk.Entry

    def init():
        GUI.window = tk.Tk()

        GUI.window.title = "Home Plotter"
        GUI.window.wm_resizable(False, False)

        GUI.window.bind("<Return>", GUI.checkInput)

        df = tk.LabelFrame(GUI.window, text="Layout")
        
        GUI.canvas = tk.Canvas(df, width = GUI.canvasSize, height=GUI.canvasSize)
        GUI.canvas.pack(expand = tk.YES, fill = tk.BOTH)

        cf = tk.LabelFrame(GUI.window, text="Set Points", width = 250, height=500)

        bframe = tk.Frame(cf, padx=10, pady=10)
        bframe.pack()

        GUI.textXF = tk.StringVar()
        GUI.textXI = tk.StringVar()
        GUI.textYF = tk.StringVar()
        GUI.textYI = tk.StringVar()
        GUI.textError = tk.StringVar()

        tk.Label(bframe, text="X:").grid(column=0,row=0)
        GUI.entryXF = tk.Entry(bframe, textvariable=GUI.textXF, width=5)
        GUI.entryXF.grid(column=1, row=0)
        tk.Label(bframe, text="ft").grid(column=2, row=0)
        GUI.entryXI = tk.Entry(bframe, textvariable=GUI.textXI, width=5)
        GUI.entryXI.grid(column=3, row=0)
        tk.Label(bframe, text="in").grid(column=4, row=0)

        tk.Label(bframe, text="Y:").grid(column=0,row=1)
        GUI.entryYF = tk.Entry(bframe, textvariable=GUI.textYF, width=5)
        GUI.entryYF.grid(column=1, row=1)
        tk.Label(bframe, text="ft").grid(column=2, row=1)
        GUI.entryYI = tk.Entry(bframe, textvariable=GUI.textYI, width=5)
        GUI.entryYI.grid(column=3, row=1)
        tk.Label(bframe, text="in").grid(column=4, row=1)

        tk.Button(bframe, command=GUI.checkInput, text="Update Point").grid(column=0, row=2, columnspan=5)

        tk.Label(bframe, textvariable=GUI.textError, fg="#ff0000").grid(column=0, row=3, columnspan=5)

        pframe = tk.Frame(cf)
        pframe.pack()

        GUI.nameList = tk.Listbox(pframe, width=3)
        GUI.nameList.bind('<<ListboxSelect>>', GUI.pointSelected)
        GUI.nameList.grid(column=0,row=0)

        GUI.pointListX = tk.Listbox(pframe, selectmode=tk.SINGLE, width=5)
        GUI.pointListX.bind('<<ListboxSelect>>', GUI.pointSelected)
        GUI.pointListX.grid(column=1,row=0)

        GUI.pointListY = tk.Listbox(pframe, selectmode=tk.SINGLE, width=5)
        GUI.pointListY.bind('<<ListboxSelect>>', GUI.pointSelected)
        GUI.pointListY.grid(column=2,row=0)

        GUI.distList1 = tk.Listbox(pframe, width=10)
        GUI.distList1.bind('<<ListboxSelect>>', GUI.pointSelected)
        GUI.distList1.grid(column=3,row=0)
        GUI.distList2 = tk.Listbox(pframe, width=10)
        GUI.distList2.bind('<<ListboxSelect>>', GUI.pointSelected)
        GUI.distList2.grid(column=4,row=0)

        adframe = tk.Frame(cf)
        adframe.pack()

        GUI.deleteButton = tk.Button(adframe, text="Delete Point", command=GUI.deleteButton, state=tk.DISABLED)
        GUI.deleteButton.grid(column=0,row=0)
        tk.Button(adframe, text="Add Point", command=GUI.addButton, state=tk.NORMAL).grid(column=1,row=0)

        df.pack(side=tk.LEFT)

        tk.Button(cf, text="Save", command=PointManager.SavePoints, justify=tk.LEFT).pack()
        tk.Button(cf, text="Load", command=PointManager.LoadPoints, justify=tk.RIGHT).pack()
        cf.pack(side=tk.RIGHT, fill="both")

    def loop():
        GUI.window.mainloop()

    def deleteButton():
        i = GUI.currIndex

        #Only remove point if 0 or higher. Otherwise, it is the origin/basis point
        if i >= 0:
            PointManager.RemovePoint(i)

    def addButton():
        point = SaePoint(0,0)
        PointManager.AddPoint(point)
        GUI.setInput(point)
        GUI.currIndex = PointManager.Points.__len__() - 1

    def setInput(point: SaePoint):
        GUI.textXF.set(point.lx().feet())
        GUI.textXI.set(point.lx().inches())
        GUI.textYF.set(point.ly().feet())
        GUI.textYI.set(point.ly().inches())

    def checkInput(var = 0):
        if GUI.currIndex < 0:
            return
        
        ix = 0
        iy = 0
        try:
            ix += 12 * int(GUI.textXF.get())
        except:
            GUI.textError = "Invalid feet for X"
            return
        try:
            ix += int(GUI.textXI.get())
        except:
            GUI.textError = "Invalid inches for X"
            return
        try:
            iy += 12 * int(GUI.textYF.get())
        except:
            GUI.textError = "Invalid feet for Y"
            return
        try:
            iy += int(GUI.textYI.get())
        except:
            GUI.textError = "Invalid inches for Y"
            return

        GUI.textError = ""

        PointManager.Points[GUI.currIndex].x = ix
        PointManager.Points[GUI.currIndex].y = iy

        GUI.updatePoints()

    def pointSelected(event):
        sel = GUI.nameList.curselection()
        if not sel:
            sel = GUI.pointListX.curselection()
        if not sel:
            sel = GUI.pointListY.curselection()
        if not sel:
            sel = GUI.distList1.curselection()
        if not sel:
            sel = GUI.distList2.curselection()
        if not sel:
            return
        index = sel[0] - 1
        GUI.currIndex = index
        
        if index < 0:
            GUI.deleteButton["state"] = tk.DISABLED
        else:
            GUI.deleteButton["state"] = tk.NORMAL
        if index < -1:
            GUI.entryXF["state"] = tk.DISABLED
            GUI.entryXI["state"] = tk.DISABLED
            GUI.entryYF["state"] = tk.DISABLED
            GUI.entryYI["state"] = tk.DISABLED
        else:
            GUI.entryXF["state"] = tk.NORMAL
            GUI.entryXI["state"] = tk.NORMAL
            GUI.entryYF["state"] = tk.NORMAL
            GUI.entryYI["state"] = tk.NORMAL

        GUI.setInput(PointManager.Points[index])
        
    #Updates list and canvas with the given data
    def updatePoints():
        #Clear canvas
        GUI.canvas.delete("all")

        #Calculate maximum and minimum x or y value for proper scaling
        maxx = PointManager.Points[0].x
        minx = 0
        maxy = PointManager.Points[0].y
        miny = 0;
        for p in PointManager.Points:
            if p.x > maxx:
                maxx = p.x
            if p.y > maxy:
                maxy = p.y
            if p.x < minx:
                minx = p.x
            if p.y < miny:
                miny = p.y

        #Calculate size of area after padding and scale factor
        padding = 50
        paddedsize = GUI.canvasSize - padding * 2
        scale = paddedsize / max(max(maxx - minx, maxy - miny), 1)

        #Draw origin and base point
        GUI.drawPoint(0, 0, "O", "#0000aa", padding, scale)
        GUI.drawPoint(PointManager.Points[0].x, PointManager.Points[0].y, "B", "#aa0000", padding, scale)

        #Draw remaining points, using N to specify the point number
        n = -1
        for p in PointManager.Points:
            n = n + 1
            if n == 0:
                continue
            GUI.drawPoint(p.x, p.y, "P"+n.__str__(), padding=padding, scale=scale)
    
        #Add values for top of list
        GUI.nameList.delete(0, tk.END)
        GUI.nameList.insert(0, ("P#"))
        GUI.nameList.insert(1, ("B"))

        GUI.pointListX.delete(0, tk.END)
        GUI.pointListX.insert(0, "X")
        GUI.pointListX.insert(1, SaeLength(PointManager.Points[0].x).__str__())

        GUI.pointListY.delete(0, tk.END)
        GUI.pointListY.insert(0, "Y")
        GUI.pointListY.insert(1, SaeLength(PointManager.Points[0].y).__str__())

        GUI.distList1.delete(0, tk.END)
        GUI.distList1.insert(0, "D1")
        GUI.distList1.insert(1, PointManager.Points[0].distance(PointManager.OriginPoint).__str__())

        GUI.distList2.delete(0, tk.END)
        GUI.distList2.insert(0, "D2")
        GUI.distList2.insert(1, "-")

        #Update points in list        
        n = -1
        for p in PointManager.Points:
            n = n + 1
            if n == 0:
                continue
            GUI.nameList.insert(n + 1, "P" + n.__str__())
            GUI.pointListX.insert(n + 1, SaeLength(p.x).__str__())
            GUI.pointListY.insert(n + 1, SaeLength(p.y).__str__())
            GUI.distList1.insert(n + 1, p.distance(PointManager.OriginPoint).__str__())
            GUI.distList2.insert(n + 1, p.distance(PointManager.Points[0]).__str__())


        
    #Draw a point using specified label text, color, and padding/scale
    def drawPoint(x, y, label = "", color = "#476042", padding = 0, scale = 1, pointSize = 3):
        x = x * scale + padding
        y = GUI.canvasSize - (y * scale + padding)
        x1, y1 = (x - pointSize), (y - pointSize)
        x2, y2 = (x + pointSize), (y + pointSize)
        GUI.canvas.create_oval(x1, y1, x2, y2, fill=color)
        GUI.canvas.create_text(x + 4, y, text = label, anchor=tk.W)