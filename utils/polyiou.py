from shapely.geometry import Polygon
import torch

class Point:
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y

def compare(a:Point,b:Point,c:Point):
    if a.x >= 0 and b.x < 0:
        return True
    if a.x == 0 and b.x == 0:
        return a.y > b.y
    det = (a.x - c.x) * (b.y - c.y) - (b.x - c.x) * (a.y - c.y)
    if det < 0:
        return True
    if det > 0:
        return False
    d1 = (a.x - c.x) * (a.x - c.x) + (a.y - c.y) * (a.y - c.y)
    d2 = (b.x - c.x) * (b.x - c.y) + (b.y - c.y) * (b.y - c.y)
    return d1 >= d2


def poly_iou_kernel(polygon1:Polygon, polygon2:Polygon):
    intersaction = polygon1.intersection(polygon2).area
    union = polygon1.union(polygon2).area
    ious = intersaction/union
    return ious

def sort(input:list):
    #compute center
    center = Point(0,0)
    for i in range(len(input)):
        center.x =center.x + input[i].x
        center.y += input[i].y
    #sort
    center.x = center.x / len(input)
    center.y = center.y / len(input)
    for i in range(len(input)-1):
        for j in range(len(input) - i - 1):
            if compare(input[j],input[j+1],center) == True:
                input[j],input[j+1] = input[j+1],input[j]
    return input

def poly_iou(poly1,poly2):
    p1 = []
    p2 = []

    for i in range(0,len(poly1),2):
        p1.append(Point(poly1[i],poly1[i+1]))

    for i in range(0,len(poly2),2):
        p2.append(Point(poly2[i],poly2[i+1]))
    poly1 = sort(p1)
    poly2 = sort(p2)

    p1 = []
    p2 = []

    for i in range(0, len(poly1)):
        p1.append((poly1[i].x,poly1[i].y))
    for i in range(0,len(poly2)):
        p2.append((poly2[i].x,poly2[i].y))

    polygon1 = Polygon(p1)
    polygon2 = Polygon(p2)
    ious = poly_iou_kernel(polygon1,polygon2)
    return ious


#poly1 = torch.Tensor([0,0,0,1,1,0,1,1])
#poly2 = torch.Tensor([0.5,0.5,1.5,0.5,1.5,1.5,0.5,1.5])
#iou = poly_iou(poly1,poly2)
#print(iou)
