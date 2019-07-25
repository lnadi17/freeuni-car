import cv2
import numpy as np

dir = 'images/'
imnum = '6'
img_name = dir + 'img' + imnum + '.png'
img = cv2.imread(img_name)
lines = []

def get_average_line(rows, cols):
	br = lines[0][0]
	kr = (lines[0][1] - lines[0][0]) / cols

	bg = lines[1][0]
	kg = (lines[1][1] - lines[1][0]) / cols

	alpha = (kr + kg) / (1 - kr * kg)
	k_avg = (np.sqrt(1 + alpha * alpha) - 1) / alpha

	intersection_x = (bg - br) / (kr - kg)
	intersection_y = kr * intersection_x + br
	b_avg = intersection_y - k_avg * intersection_x

	dy = 1

	xrf = (intersection_y + dy - br) / kr
	xgf = (intersection_y + dy - bg) / kg
	xbf = (intersection_y + dy - b_avg) / k_avg

	if ((xbf < xrf and xbf < xgf) or (xbf > xrf and xbf > xgf) ):
		k_avg = - 1 /k_avg
		b_avg = intersection_y - k_avg * intersection_x

	y0 = int(b_avg)
	y1 = int(k_avg * cols + b_avg)

	return y0, y1

def nothing(x):
	pass

# Approximates polygon but has upper limit of corner count
def approx_poly(contour, max_corners, epsilon):
	approx = cv2.approxPolyDP(contour, epsilon*cv2.arcLength(contour, True), True)
	if (len(approx) > 4):
		return approx_poly(contour, max_corners, epsilon - 0.005)
	return approx

def draw_line_on_image(img, contours, shape, color):
	mask = np.zeros(shape)
	max_area = 0
	approx = None

	for cnt in contours:
		area = cv2.contourArea(cnt)
		
		if (area > 400 and area > max_area):
			# Draw simplified contours on mask
			approx = approx_poly(cnt, 4, 0.01)
			max_area = area

	if (approx is not None):
		cv2.drawContours(mask, [approx], 0, (255, 255, 255), thickness=cv2.FILLED)
		# Approximate line
		rows, cols = mask.shape[:2]
		[vx, vy, x, y] = cv2.fitLine(approx, cv2.DIST_HUBER, 0, 0.01, 0.01)
		lefty = int((-x * vy / vx) + y)
		righty = int(((cols - x) * vy / vx ) + y)
		cv2.line(img, (0, lefty), (cols - 1, righty), color, 2)
		lines.append([lefty, righty])

	cv2.imshow("cont", mask)

# cv2.namedWindow("RED")
# cv2.createTrackbar("R-L-H", "RED", 0, 180, nothing)
# cv2.createTrackbar("R-L-S", "RED", 0, 255, nothing)
# cv2.createTrackbar("R-L-V", "RED", 97, 255, nothing)
# cv2.createTrackbar("R-U-H", "RED", 24, 180, nothing)
# cv2.createTrackbar("R-U-S", "RED", 255, 255, nothing)
# cv2.createTrackbar("R-U-V", "RED", 180, 255, nothing)

# cv2.namedWindow("GREEN")
# cv2.createTrackbar("G-L-H", "GREEN", 55, 180, nothing)
# cv2.createTrackbar("G-L-S", "GREEN", 121, 255, nothing)
# cv2.createTrackbar("G-L-V", "GREEN", 49, 255, nothing)
# cv2.createTrackbar("G-U-H", "GREEN", 97, 180, nothing)
# cv2.createTrackbar("G-U-S", "GREEN", 255, 255, nothing)
# cv2.createTrackbar("G-U-V", "GREEN", 204, 255, nothing)

for i in range(1, 30):
	imnum = str(i)
	img_name = dir + 'img' + imnum + '.png'
	
	while True:
		img = cv2.imread(img_name)
		hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

		# r_l_h = cv2.getTrackbarPos("R-L-H", "RED")
		# r_l_s = cv2.getTrackbarPos("R-L-S", "RED")
		# r_l_v = cv2.getTrackbarPos("R-L-V", "RED")
		# r_u_h = cv2.getTrackbarPos("R-U-H", "RED")
		# r_u_s = cv2.getTrackbarPos("R-U-S", "RED")
		# r_u_v = cv2.getTrackbarPos("R-U-V", "RED")

		# g_l_h = cv2.getTrackbarPos("G-L-H", "GREEN")
		# g_l_s = cv2.getTrackbarPos("G-L-S", "GREEN")
		# g_l_v = cv2.getTrackbarPos("G-L-V", "GREEN")
		# g_u_h = cv2.getTrackbarPos("G-U-H", "GREEN")
		# g_u_s = cv2.getTrackbarPos("G-U-S", "GREEN")
		# g_u_v = cv2.getTrackbarPos("G-U-V", "GREEN")

		r_l_h = 0
		r_l_s = 0
		r_l_v = 97
		r_u_h = 24
		r_u_s = 255
		r_u_v = 180

		g_l_h = 55
		g_l_s = 121
		g_l_v = 49
		g_u_h = 97
		g_u_s = 255
		g_u_v = 204

		###

		lower_red = np.array([r_l_h, r_l_s, r_l_v])
		upper_red = np.array([r_u_h, r_u_s, r_u_v])

		lower_magenta = np.array([174, r_l_s, r_l_v])
		upper_magenta = np.array([255, r_u_s, r_u_v])

		###

		lower_green = np.array([g_l_h, g_l_s, g_l_v])
		upper_green = np.array([g_u_h, g_u_s, g_u_v])

		red_mask = cv2.inRange(hsv, lower_red, upper_red)
		magenta_mask = cv2.inRange(hsv, lower_magenta, upper_magenta)

		green_mask = cv2.inRange(hsv, lower_green, upper_green)

		r_mask = red_mask + magenta_mask
		g_mask = green_mask

		r_contours, _ = cv2.findContours(r_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		g_contours, _ = cv2.findContours(g_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		draw_line_on_image(img, r_contours, r_mask.shape, (0, 0, 255))
		draw_line_on_image(img, g_contours, g_mask.shape, (0, 255, 0))

		if (len(lines) == 2):
			rows, cols = img.shape[:2]
			y0, y1 = get_average_line(rows, cols)
			cv2.line(img, (0, y0), (cols - 1, y1), (255, 0, 0), 2)
		lines = []

		key = cv2.waitKey(1)
		if (key == 27):
			break

		cv2.imshow('image', img)
		# cv2.imshow('mask', g_mask)

cv2.destroyAllWindows()