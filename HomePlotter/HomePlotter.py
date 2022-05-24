from PointManager import PointManager
from SaePoint import SaePoint


PointManager.Init()
PointManager.BasisPoint = SaePoint(144, 0)
PointManager.AddPoint(SaePoint(12,0))
PointManager.AddPoint(SaePoint(0,12))
PointManager.AddPoint(SaePoint(12,12))


PointManager.Loop()