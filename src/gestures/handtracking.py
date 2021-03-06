#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""-------------------------------------------------------------------------
    Implemented bounding boxes for contours, refactored input and debugging code,
    and translated comments from Spanish to English.

    modifier: Gaby Moreno Cesar
    contact: morengab@gmail.com
    last update: 04/23/2013

    Control de cursor, click derecho e izquierdo, mediante procesamiento de imágenes.

    author:   Yeison Cardona
    contact:    yeison.eng@gmail.com 
    first release:  12/11/2012
    last release: 22/11/2012

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
-------------------------------------------------------------------------"""

import pickle, time, os

try: 
    import numpy as np
    from numpy import sqrt, arccos, rad2deg
except:
    print "need Numpy for Python!!."
    exit()

try: import cv2
except:
    print "need OpenCV for Python!!."
    exit()

if not cv2.__version__ >= "2.4":
    print "OpenCV version to old!!."
    print "need version >= 2.4."
    exit()


class HandTracking:
    def __init__(self):
        self.debugMode = False
        
        #Bounding boxes for motion tracking
        self.boundingBoxes = []

        #Data dictionary
        self.Data = {
            "angles less 90" : 0,
            "cursor" : (0, 0),
            "hulls" : 0,
            "defects" : 0,
            "fingers": 0,
            "fingers history": [0],
            "area": 0,
            "diff vector": (0, 0),
            "max distance": 0
        }

        #Previous update
        self.lastData = self.Data

        #Load filter variables
        #If changed during execution these will update in sliders
        try:  self.Vars = pickle.load(open(".config", "r"))
        except:
            print "Config file («.config») not found."
            exit()


    def run(self, im):
        """Filters and processes image to detect skin"""

        im = cv2.flip(im, 1)
        self.imOrig = im.copy()
        self.imNoFilters = im.copy()

        #Clear bounding boxes 
        self.boundingBoxes = []

        #Smoothing
        im = cv2.blur(im, (self.Vars["smooth"], self.Vars["smooth"]))
        
        #Filter the skin
        filter_ = self.filter_skin(im)
 
        #Erode filter
        filter_ = cv2.erode(filter_,
                            cv2.getStructuringElement(
                                cv2.MORPH_ELLIPSE,
                                (self.Vars["erode"], self.Vars["erode"])))           
        
        #Dilate filter
        filter_ = cv2.dilate(filter_,
                             cv2.getStructuringElement(
                                cv2.MORPH_ELLIPSE,
                                (self.Vars["dilate"], self.Vars["dilate"])))
        
        
        #Show black and white image (result after skin filtering)
        if self.debugMode: cv2.imshow("Filter Skin", filter_)
        
        #Find contours
        contours, hierarchy = cv2.findContours(
                                filter_,
                                cv2.RETR_LIST,
                                cv2.CHAIN_APPROX_NONE)

        if self.debugMode: cv2.imshow("Filter Skin", filter_)

        #Eliminate spots with areas below a certain threshold
        allIdex = []
        for index in range(len(contours)):
            area = cv2.contourArea(contours[index])
            if area < 5e3: allIdex.append(index)
        allIdex.sort(reverse=True)
        for index in allIdex: contours.pop(index)

        #Stop processing if there are no contours
        if len(contours) == 0: return
        
        allIdex = []
        index_ = 0
        
        #Process each contour (ex: hand, face)
        for cnt in contours:
            self.Data["area"] = cv2.contourArea(cnt)
            
            tempIm = im.copy()
            tempIm = cv2.subtract(tempIm, im)
            
            #Finds the bounding box of the hull
            hull = cv2.convexHull(cnt)
            bounding = cv2.boundingRect(hull)
            self.boundingBoxes.append(bounding)
            
            # Draws pink bounding boxes
            cx = bounding[0]
            cy = bounding[1]
            rect_w = bounding[2]
            rect_h = bounding[3]

            p0 = tuple((cx, cy))
            p1 = tuple((cx+rect_w, cy))
            p2 = tuple((cx+rect_w, cy+rect_h))
            p3 = tuple((cx, cy+rect_h))

            cv2.line(tempIm, p0, p1, (255, 0, 255), 5)
            cv2.line(tempIm, p1, p2, [255, 0, 255], 5)
            cv2.line(tempIm, p2, p3, [255, 0, 255], 5)
            cv2.line(tempIm, p3, p0, [255, 0, 255], 5)

            #Finds convexities (finger detection)
            hull = cv2.convexHull(cnt)
            self.last = None
            self.Data["hulls"] = 0
            for hu in hull:
                if self.last == None: 
                    cv2.circle(tempIm, tuple(hu[0]), 10, (0,0,255), 5)
                else:
                    distance = self.distance(self.last, tuple(hu[0]))
                    #Eliminates points too close to each other
                    if distance > 40: 
                        self.Data["hulls"] += 1
                        #Draws red circles
                        cv2.circle(tempIm, tuple(hu[0]), 10, (0,0,255), 5)
                self.last = tuple(hu[0])
            
            #Find convex hulls, will help with finger detection
            angles = []
            hull = cv2.convexHull(cnt,returnPoints = False)
            defects = cv2.convexityDefects(cnt,hull)
            
            if defects == None: return
                
            self.Data["defects"] = 0
            for i in range(defects.shape[0]):
                s,e,f,d = defects[i,0]
                if d > 1000 :
                    start = tuple(cnt[s][0])
                    end = tuple(cnt[e][0])
                    far = tuple(cnt[f][0])
                    self.Data["defects"] += 1
                    #Defects marked with yellow points
                    cv2.circle(tempIm,far,5,[0,255,255],-1) 
                    #Draws lines between convexities and defects
                    cv2.line(tempIm, start, far, [255, 0, 0], 5) 
                    cv2.line(tempIm, far, end, [255, 0, 0], 5)
                    #Obtain the angles that form anterior lines
                    angles.append(self.angle(far, start, end))

            #Filter angles less than 90 degrees
            b = filter(lambda a:a<90, angles)
            
            #Assume angles less than 90 deg indicate a finger
            self.Data["angles less 90"] = len(b)
            self.Data["fingers"] = len(b) + 1
            
            #Save finger history
            self.Data["fingers history"].append(len(b) + 1)            
            
            if len(self.Data["fingers history"]) > 10: 
                self.Data["fingers history"].pop(0)   

            self.imOrig = cv2.add(self.imOrig, tempIm)

            index_ += 1
        
        #Fill skin areas with green color
        cv2.drawContours(self.imOrig,contours,-1,(64,255,85),-1)

        #Visualize data
        self.debug()
        if self.debugMode: cv2.imshow("\"Hulk\" Mode", self.imOrig)
     

    #----------------------------------------------------------------------
    # Bounding Box Helpers
    #   
    def getBoundingMidpoints(self, img):
        """Returns array of bounding box midpoints"""
        
        #Process image
        self.run(img)

        #Process bounding boxes
        midpoints = []
        for box in self.boundingBoxes: 
            cx = box[0]
            cy = box[1]
            rect_w = box[2]
            rect_h = box[3]

            mx = cx + rect_w/2
            my = cy + rect_h/2

            midpoints.append((mx, my))
        
        return midpoints


    def update_dir_data(self, dir):
        """Updates debugging data for direction vector"""
        if not dir: 
            return 
        diff = dir[0]
        dist = dir[1]
        self.Data["diff vector"] = "(%d, %d)" % (diff[0], diff[1])
        self.Data["max distance"] = "%d" % dist


    #----------------------------------------------------------------------
    # Processing Helpers
    #
    def distance(self, cent1, cent2):
        """Returns the distance between two points"""
        x = abs(cent1[0] - cent2[0])
        y = abs(cent1[1] - cent2[1])
        d = sqrt(x**2+y**2)
        return d
    
    
    def angle(self, cent, rect1, rect2):
        """Returns the angle between three points"""
        v1 = (rect1[0] - cent[0], rect1[1] - cent[1])
        v2 = (rect2[0] - cent[0], rect2[1] - cent[1])
        dist = lambda a:sqrt(a[0] ** 2 + a[1] ** 2)
        angle = arccos(
            (sum(map(lambda a, b:a*b, v1, v2))) / (dist(v1) * dist(v2)))
        angle = abs(rad2deg(angle))
        return angle
        
    
    def filter_skin(self, im):
        """Apply a skin filter"""
        UPPER = np.array([
            self.Vars["upper"], 
            self.Vars["filterUpS"], 
            self.Vars["filterUpV"]], 
            np.uint8)
        LOWER = np.array([
            self.Vars["lower"], 
            self.Vars["filterDownS"], 
            self.Vars["filterDownV"]], np.uint8)
        hsv_im = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
        filter_im = cv2.inRange(hsv_im, LOWER, UPPER)
        return filter_im


    #----------------------------------------------------------------------
    # Debugging Helpers
    #
    def toggle_debug(self):
        self.debugMode = not self.debugMode

        if (self.debugMode):
            #Filter and trackbar windows
            cv2.namedWindow("Filters")
            cv2.createTrackbar("erode", "Filters", 
                                self.Vars["erode"], 255, self.onChange_erode)
            cv2.createTrackbar("dilate", "Filters", 
                                self.Vars["dilate"], 255, self.onChange_dilate)
            cv2.createTrackbar("smooth", "Filters", 
                                self.Vars["smooth"], 255, self.onChange_smooth)
            
            cv2.namedWindow("HSV Filters")        
            cv2.createTrackbar("upper", "HSV Filters", 
                                self.Vars["upper"], 255, self.onChange_upper)
            cv2.createTrackbar("filterUpS", "HSV Filters", 
                                self.Vars["filterUpS"], 255, self.onChange_fuS)
            cv2.createTrackbar("filterUpV", "HSV Filters", 
                                self.Vars["filterUpV"], 255, self.onChange_fuV)        
            cv2.createTrackbar("lower", "HSV Filters", 
                                self.Vars["lower"], 255, self.onChange_lower)   
            cv2.createTrackbar("filterDownS", "HSV Filters", 
                                self.Vars["filterDownS"], 255, self.onChange_fdS)
            cv2.createTrackbar("filterDownV", "HSV Filters", 
                                self.Vars["filterDownV"], 255, self.onChange_fdV)

            #Add text
            self.addText = lambda image, text, point: cv2.putText(
                                image, 
                                text, 
                                point, 
                                cv2.FONT_HERSHEY_PLAIN, 
                                1.0,
                                (255,255,255))

        else: 
            cv2.destroyWindow("Filters")
            cv2.destroyWindow("HSV Filters")
            cv2.destroyWindow("Filter Skin")
            cv2.destroyWindow("\"Hulk\" Mode")


    def debug(self):
        """Print debug feedback on window if debug mode on"""
        yPos = 10
        if self.debugMode: self.addText(self.imOrig, "Debug", (yPos, 20))
        pos = 50
        for key in self.Data.keys():
            if self.debugMode: 
                self.addText(
                    self.imOrig, 
                    (key+": "+str(self.Data[key])), 
                    (yPos, pos))
            pos += 20

     
    def onChange_fuS(self, value):
        self.Vars["filterUpS"] = value
        pickle.dump(self.Vars, open(".config", "w"))
        
    
    def onChange_fdS(self, value):
        self.Vars["filterDownS"] = value
        pickle.dump(self.Vars, open(".config", "w"))
        

    def onChange_fuV(self, value):
        self.Vars["filterUpV"] = value
        pickle.dump(self.Vars, open(".config", "w"))
        

    def onChange_fdV(self, value):
        self.Vars["filterDownV"] = value
        pickle.dump(self.Vars, open(".config", "w"))
        

    def onChange_upper(self, value):
        self.Vars["upper"] = value
        pickle.dump(self.Vars, open(".config", "w"))
    

    def onChange_lower(self, value):
        self.Vars["lower"] = value
        pickle.dump(self.Vars, open(".config", "w"))
    

    def onChange_erode(self, value):
        self.Vars["erode"] = value + 1
        pickle.dump(self.Vars, open(".config", "w"))
    

    def onChange_dilate(self, value):
        self.Vars["dilate"] = value + 1
        pickle.dump(self.Vars, open(".config", "w"))
    

    def onChange_smooth(self, value):
        self.Vars["smooth"] = value + 1
        pickle.dump(self.Vars, open(".config", "w"))
