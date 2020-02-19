#!/usr/bin/env python

# Authors:      Shawn Herrington & Paul Klappa
# Date:         2/17/2020
# Purpose:      mwe for logging data to a file
# Depends:      You will need to create a directory called "log_files" somewhere and
#		and make sure that the code points to the directory you created, see
#		line 39
# Details:	filename is todays date and the current time
#

# ------------------
# ATTENTION STUDENTS
# ------------------

# this file contains an example of how to write position information from a .csv.
# The important part of this is understanding how the turtlebot is communicating its
# messages

# ----------------
# END INSTRUCTIONS
# ----------------

import rospy, time, csv, os, datetime, math
from beginner_tutorials.msg import Position
from nav_msgs.msg import Odometry

x1 = 0
y1 = 0
z1 = 0
yaw = 0

# Time initial number
t_init = 0

# callback dunction for3DOF rotation position
def callback_ori(data):
    global yaw

    yaw  = data.angular.yaw
    # pitch = data.angular.pitch
    # roll   = data.angular.roll

# callback function for 3DOF linear position
def callback_pos(data):
    global x,y,z

    x = data.pose.pose.position.x
    y = data.pose.pose.position.y
    z = data.pose.pose.position.z

if __name__ == "__main__":

	try:

		# declare new object Position()
		# Position() is a custom message format consisting of 3 linear
		# and 3 angular position states (x,y,z,roll,pitch,yaw)
		position = Position()

		# create subscriber to the euler angle node, this node is created
		# the quaternion to euler conversion and yaw wrappin is being
		# handled, the angular positions are also converted
		# from radians prior to being published
		rospy.Subscriber('/eul', Position, callback_ori)
		
		# create a subscriber to the odometry node, this node is created
		# automatically in te turtlebot3 simulation, it contains the 
		# position in 3 dimensions in the global frame, the angular
		# position is stored as a quaternion and has to be converted to
		# euler angles to be "readable"
		rospy.Subscriber('/odom', Odometry, callback_pos)

		# create a node & specify anonymous since we don't care about the name
		rospy.init_node('LogFileNode', anonymous=True)

		# create a rate object for timing, the argument is in Hz
		r = rospy.Rate(100) #HZ

		# Set up time constant so the constant is not always 0
		time.sleep(1)
		t_init = rospy.get_rostime()
		t_init = t_init.to_sec()

		# this will constitute the header for the columns in the csv file, this is simply because
		# it is the first line which will be written
		myData = ["time [s]","x","y","z","yaw"]

		# the following code creates a base filename containing the data and time
		fileNameBase = "/home/klap/paul_ws/src/mec-engr_401/scripts/log_files/" + datetime.datetime.now().strftime("%b_%d_%H_%M")

		# the end of the file will always be ".csv"
		fileNameSuffix = ".csv"

		# this number will only be used if the filename already exists
		num = 1

		# compose the complete filename from the component parts, don't use num yet
		fileName = fileNameBase + fileNameSuffix

		# while loop will execute until we have a unique filename
		while os.path.isfile(fileName):
			# if the filename is not unique, add a number to the end of it
			fileName = fileNameBase + "_" + str(num) + fileNameSuffix
			# increments the number in case the filename is still not unique
			num = num + 1

		# now that we have a good filename open it, the "a" option is "append", the default
		# behavior is to overwrite the file each time the file is opened, in this case we
		# want to keep the existing file but add a new line each time we open so we use
		# the append option

		myFile = open(fileName, 'a')
		# using the newly create file object

		with myFile:
			# create a csv writer object which is attached to the file object
			writer = csv.writer(myFile)
			# write a single row, there are other write functions which can be used,
			# since this one only writes a single row it automatically adds a newline
			# to the end of the data
			writer.writerow(myData)

		while not rospy.is_shutdown():

			# Loop Time Data
			tnew = rospy.get_rostime()
			tnew = tnew.to_sec()
			tout = (tnew - t_init)

			# this represents the "real" data which we want to write to the file
			myData = [tout,x,y,z,yaw]

			# print status message
			print "write to file"

			# same as the code block above
			myFile = open(fileName, 'a')
			with myFile:
				writer = csv.writer(myFile)
				writer.writerow(myData)

			# print status message
			print "write complete, waiting"

			r.sleep()

	except rospy.ROSInterruptException:

	    pass
