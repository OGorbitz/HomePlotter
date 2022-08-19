import json
import tkinter as tk

from SaePoint import SaePoint
from SaeLength import SaeLength


class PointManager(object):
    OriginPoint = SaePoint(0, 0)
    
    Points = []

    # Initialize list of points
    def init():
        PointManager.Points.append(SaePoint(12,0))
    def AddPoint(point):
        PointManager.Points.append(point)
        PointManager.UpdatePoints()
    def RemovePoint(index):
        PointManager.Points.pop(index)
        PointManager.UpdatePoints()

    def PrintDistances():
        for p in PointManager.Points:
            d1 = PointManager.OriginPoint.distance(p)
            d2 = PointManager.BasisPoint.distance(p)
            print( "(" + SaeLength(p.x).__str__() + "," + SaeLength(p.y).__str__() + ") " + d1.__str__() + " | " + d2.__str__())

    # Save points in a .json file
    def SavePoints():
        with open("plot.json", "w", encoding="utf-8") as f:
            json.dump(PointManager.Points, f, default=lambda o: o.encode(), ensure_ascii=False, indent=4)
            f.close()
    # Load points from a .json file
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
        PointManager.UpdatePoints()
    # Update GUI when points are changed
    def UpdatePoints():
        from GUI import GUI
        GUI.updatePoints()

        