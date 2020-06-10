# The purpose of this program was to identify a marked path as the desired path of the drone. After the video is taken by a downward 
# facing USB camera, the video is processed by this program using OpenCV in python. The program not only identifies the desired path but 
# it also calculates the angle error between the desired and current path of the drone. This angle is used in the controller of the drone 
# to keep it moving along the desired path.

# Credit for the path detection development goes to kemfic on GitHub. His post about "Simple Lane Detection" on hackster.io inspired the 
# path detection aspect of this project. I have used his path detection software as the foundation of my path detection program in this 
# project. If you are interested in an indepth article on how kemfic developed his simple lane detection software please refer to his 
# article on hackster.io (https://www.hackster.io/kemfic/simple-lane-detection-c3db2f).

#! /usr/bin/env python

from __future__ import division
import rospy
import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
from matplotlib import image as mpimg
from std_msgs.msg import Float32

rospy.init_node('path-detection_node')

pub = rospy.Publisher('angle_error', Float32, queue_size=10)

rate = rospy.Rate(10)
msg = Float32()

#cap = cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720,format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")

cap = cv2.VideoCapture(1)

if cap.isOpened():	
	while not rospy.is_shutdown():	
		ret_val, frame = cap.read();

		def color_filter(image):
			hls = cv2.cvtColor(image, cv2.COLOR_RGB2HLS)
			lower = np.array([190, 190, 190])
			upper = np.array([255, 255, 255])
			yellower = np.array([0, 190, 0])
			yelupper = np.array([255, 255, 255])
			yellowmask = cv2.inRange(hls, yellower, yelupper)
			whitemask = cv2.inRange(hls, lower, upper)
			mask = cv2.bitwise_or(yellowmask, whitemask)
			masked = cv2.bitwise_and(image, image, mask = mask)
			return masked
		
		filtered_img = color_filter(frame)

		def roi(img):
			x = int(img.shape[1])
			y = int(img.shape[0])
			shape = np.array([[int(0.3*x), int(0.9*y)], [int(0.7*x), int(0.9*y)], [int(0.7*x), int(0.1*y)], [int(0.3*x), int(0.1*y)]])

			mask = np.zeros_like(img)

			if len(img.shape) > 2:
				channel_count = img.shape[2]
				ignore_mask_color = (255,) * channel_count
			else:
				ignore_mask_color = 255

			cv2.fillPoly(mask, np.int32([shape]), ignore_mask_color)

			masked_image = cv2.bitwise_and(img, mask)
			return masked_image

		roi_img = roi(filtered_img)

		def grayscale(img):
			return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
		def canny(img):
			return cv2.Canny(grayscale(img), 50, 120)

		canny_img = canny(roi_img)

		rightSlope, leftSlope, rightIntercept, leftIntercept = [], [], [], []

		def draw_lines(img, lines, thickness = 5):
			global rightSlope, leftSlope, rightIntercept, leftIntercept
			rightColor = [0, 255, 0]
			leftColor = [0, 255, 0]

			if lines is not None:
				for line in lines:
					for x1, y1, x2, y2 in line:
						slope = (y1-y2) / (x1-x2)
						if slope > 0.3:
							if x1 > 500:
								yintercept = y2 - (slope*x2)
								rightSlope.append(slope)
								rightIntercept.append(yintercept)
							else: None
						elif slope < -0.3:
							if x1 < 600:
								yintercept = y2 - (slope*x2)
								leftSlope.append(slope)
								leftIntercept.append(yintercept)

			leftavgSlope = np.mean(leftSlope[-30:])
			leftavgIntercept = np.mean(leftIntercept[-30:])

			rightavgSlope = np.mean(rightSlope[-30:])
			rightavgIntercept = np.mean(rightIntercept[-30:])

			try:
				left_line_x1 = int((0.65 * img.shape[0] - leftavgIntercept) / leftavgSlope)
				left_line_x2 = int((img.shape[0] - leftavgIntercept) / leftavgSlope)

				right_line_x1 = int((0.65 * img.shape[0] - rightavgIntercept) / rightavgSlope)
				right_line_x2 = int((img.shape[0] - rightavgIntercept) / rightavgSlope)

				pts = np.array([[left_line_x1, int(0.1 * img.shape[0])], [left_line_x2, int(0.9 * img.shape[0])], [right_line_x2, int(0.9 * img.shape[0])], [right_line_x1, int(0.1 * img.shape[0])]], np.int32)
				pts = pts.reshape((-1, 1, 2))
				cv2.fillPoly(img, [pts], (255, 0, 0))

				cv2.line(img, (left_line_x1, int(0.2 * img.shape[0])), (left_line_x2, int(0.8 * img.shape[0])), leftColor, 10)
				cv2.line(img, (right_line_x1, int(0.2 * img.shape[0])), (right_line_x2, int(0.8 * img.shape[0])), rightColor, 10)
				
				x3 = int(img.shape[1])
				y3 = int(img.shape[0])
				midpoint = int(x3/2)		
				endpoint1 = int((left_line_x1 + right_line_x1)/2)
				endpoint2 = int((left_line_x2 + right_line_x2)/2)
				yellowline = [0, 255, 255]				
				blueline = [255, 255, 0]				

				cv2.line(img, (midpoint , int(0.8*y3)), (midpoint , int(0.2*y3)), yellowline, thickness = 1, lineType = 8, shift = 0) #center line, current path of movement
				cv2.line(img, (endpoint1 , int(0.7*y3)), (endpoint2, y3), blueline, thickness = 1, lineType = 8, shift = 0) #desired line, desired path of movement
				
				length1 = y3 - int(0.7 * img.shape[0])
				length2 = midpoint - endpoint1
				
				msg = 0
				if (length1 != 0):	
					theta = np.arctan((length2 / length1))
					msg = theta
					pub.publish(msg)
					rate.sleep()
						
			except ValueError:
				pass

		def hough_lines(img, rho, theta, threshold, min_line_length, max_line_gap):
			lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength = min_line_length, maxLineGap = max_line_gap)
			line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype = np.uint8)
			draw_lines(line_img, lines)
			return line_img
			
		def linedetect(img):
			return hough_lines(img, 1, np.pi/180, 10, 20, 100)
			
		#hough_img = linedetect(canny_img)


		def findline(img):
			lines = cv2.HoughLines(img, 1, np.pi/180,100, np.array([]), 0, 0)

			a,b,c = lines.shape

			for i in range(a):
				rho = lines[i][0][0]
				theta = lines[i][0][1]
				a = np.cos(theta)
				b = np.sin(theta)
				x0, y0 = a*rho, b*rho
				pt1 = ( int(x0+1000*(-b)), int(y0+1000*(a)) )
				pt2 = ( int(x0-1000*(-b)), int(y0-1000*(a)) )
				hough_img = cv2.line(img, pt1, pt2, (0, 0, 255), 2, cv2.LINE_AA)
		
			return hough_img

		hough_img = findline(canny_img)

		background = frame
		overlay = hough_img

		final_img = cv2.addWeighted(background, 0.7, overlay, 0.4, 0)
		resize_img = cv2.resize(final_img, (960, 540))

		cv2.imshow('Camera', resize_img)
		key = cv2.waitKey(10)
		if key == 27: # Check for ESC key
			cv2.destroyAllWindows()
			break ;
