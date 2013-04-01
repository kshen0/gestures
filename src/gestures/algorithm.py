import cv2

#Computes the absolute grayscale difference given 3 successive images
#This detects "movements" in the video
def absdiff(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)