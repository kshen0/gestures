import cv, cv2
from webcam import Webcam

WIN_NAME = 'Hand Detection'

def main():
	c = 0
	camera = Webcam()
	cv2.namedWindow(WIN_NAME, cv2.CV_WINDOW_AUTOSIZE)

	# Get frame from webcam
	frame = camera.get_frame()
	size = (frame.shape[0], frame.shape[1])

	# Convert to IPLImage type
	#frame = make_iplimage(frame)

	# Create hsv stuff 
	src = cv.CreateImage(size, 8, 3)
	hsv_image = cv.CreateImage(size, 8, 3)
	hsv_np = camera.get_frame()
	hsv_mask = cv.CreateImage(size, 8, 1)
	hsv_np = camera.get_frame()
	hsv_mask_np = camera.get_frame()
	hsv_min = cv.Scalar(0, 30, 80, 0)
	hsv_max = cv.Scalar(20, 150, 255, 0)

	while c != 27:
		# get source image
		#src = make_iplimage(camera.get_frame()) 
		src = camera.get_frame()

		# show source image in window
		#cv2.namedWindow("Source", cv2.CV_WINDOW_AUTOSIZE)
		#cv2.imshow("Source", src)

		# get hsv image
		cv2.cvtColor(src, cv.CV_BGR2HSV, hsv_np)
		# show hsv image in window
		#cv2.namedWindow("hsv-img", cv2.CV_WINDOW_AUTOSIZE)
		#cv2.imshow("hsv-imag", hsv_np)

		# get hsv mask
		#cv2.inRange(hsv_np, hsv_min, hsv_max, hsv_mask_np)
		output = cv2.inRange(hsv_np, hsv_min, hsv_max)
		# show hsv image in window
		cv2.namedWindow("hsv-mask", cv2.CV_WINDOW_AUTOSIZE)
		cv2.imshow("hsv-mask", output)

		c = cv.WaitKey(10)

	cv2.destroyAllWindows()

def make_iplimage(frame):
	"""Given a numpy array, return an equivalent iplimage"""
	size = (frame.shape[0], frame.shape[1])
	bitmap = cv.CreateImageHeader((size[1], size[0]), 
		cv.IPL_DEPTH_8U, 3)
	cv.SetData(bitmap, frame.tostring(), frame.dtype.itemsize * 3 * size[1])
	return bitmap







if __name__ == "__main__":
	main()