import tkinter as tk
from SaePoint import SaePoint
from SaeLength import SaeLength


class PointManager(object):
    OriginPoint = SaePoint(0, 0)
    BasisPoint = SaePoint(0, 0)
    
    Points = []

    def Init():
        GUI.init()
    
    def Loop():
        GUI.loop()
    
    def AddPoint(point):
        PointManager.Points.append(point)
        GUI.updatePoints(PointManager.BasisPoint, PointManager.Points)
    def RemovePoint(index):
        PointManager.Points.pop(index)
        GUI.updatePoints(PointManager.BasisPoint, PointManager.Points)
    def PrintDistances():
        for p in PointManager.Points:
            d1 = PointManager.OriginPoint.distance(p)
            d2 = PointManager.BasisPoint.distance(p)
            print( "(" + SaeLength(p.x).__str__() + "," + SaeLength(p.y).__str__() + ") " + d1.__str__() + " | " + d2.__str__())


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
        cf.pack(side=tk.RIGHT, fill="both")

    def loop():
        GUI.window.mainloop()

    def deleteButton():
        i = GUI.pointList.curselection()[0] - 2

        #Only remove point if 0 or higher. Otherwise, it is the origin/basis point
        if i >= 0:
            PointManager.RemovePoint(i)

    def addButton():
        point = SaePoint(0,0)
        GUI.setInput(point)
        PointManager.AddPoint(point)

    def setInput(point: SaePoint):
        GUI.textXF.set(point.lx().feet())
        GUI.textXI.set(point.lx().inches())
        GUI.textYF.set(point.ly().feet())
        GUI.textYI.set(point.ly().inches())

    def checkInput(var = 0):
        if GUI.currIndex < -1:
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

        if GUI.currIndex == -1:
            PointManager.BasisPoint.x = ix
        else:
            PointManager.Points[GUI.currIndex].x = ix
            PointManager.Points[GUI.currIndex].y = iy
        GUI.updatePoints(PointManager.BasisPoint, PointManager.Points)

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

        if index == -1:
            GUI.setInput(PointManager.BasisPoint)
        if index >= 0:
            GUI.setInput(PointManager.Points[index])
        
    #Updates list and canvas with the given data
    def updatePoints(basisPoint, points):
        #Clear canvas
        GUI.canvas.delete("all")

        #Calculate maximum and minimum x or y value for proper scaling
        maxx = basisPoint.x
        minx = 0
        maxy = basisPoint.y
        miny = 0;
        for p in points:
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
        GUI.drawPoint(basisPoint.x, basisPoint.y, "B", "#aa0000", padding, scale)

        #Draw remaining points, using N to specify the point number
        n = 1
        for p in points:
            GUI.drawPoint(p.x, p.y, "P"+n.__str__(), padding=padding, scale=scale)
            n = n + 1
    
        #Update points in list        
        GUI.nameList.delete(0, tk.END)
        GUI.nameList.insert(0, ("BP"))

        GUI.pointListX.delete(0, tk.END)
        GUI.pointListX.insert(0, SaeLength(basisPoint.x).__str__())

        GUI.pointListY.delete(0, tk.END)
        GUI.pointListY.insert(0, SaeLength(basisPoint.y).__str__())

        GUI.distList1.delete(0, tk.END)
        GUI.distList1.insert(0, "D1")

        GUI.distList2.delete(0, tk.END)
        GUI.distList2.insert(0, "D2")

        n = 1
        for p in points:
            GUI.nameList.insert(n, "P" + n.__str__())
            GUI.pointListX.insert(n, SaeLength(p.x).__str__())
            GUI.pointListY.insert(n, SaeLength(p.y).__str__())
            GUI.distList1.insert(n, p.distance(PointManager.OriginPoint).__str__())
            GUI.distList2.insert(n, p.distance(PointManager.BasisPoint).__str__())
            n = n + 1

        
    #Draw a point using specified label text, color, and padding/scale
    def drawPoint(x, y, label = "", color = "#476042", padding = 0, scale = 1, pointSize = 3):
        x = x * scale + padding
        y = GUI.canvasSize - (y * scale + padding)
        x1, y1 = (x - pointSize), (y - pointSize)
        x2, y2 = (x + pointSize), (y + pointSize)
        GUI.canvas.create_oval(x1, y1, x2, y2, fill=color)
        GUI.canvas.create_text(x + 4, y, text = label, anchor=tk.W)