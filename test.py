#!/usr/bin/env python
#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
import cv_bridge
import cv2
from geometry_msgs.msg import Twist
import imutils
from std_msgs.msg import String

keep_going = False


def move_to_object(image_message, publisher):
    global keep_going
    bridge = cv_bridge.CvBridge()
    image = None
    try:
        image = bridge.imgmsg_to_cv2(image_message, "bgr8")  # convert image message to OpenCV image matrix
    except cv_bridge.CvBridgeError, e:
        rospy.logerr(e.message)
        print e.message

    if image is not None:
	crackCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        
	# resize the frame, blur it, and convert it to the HSV
	# color space
	#frame = self.bridge.imgmsg_to_cv2(msg,desired_encoding= 'bgr8')
	
	cracks = crackCascade.detectMultiScale(image,scaleFactor=1.1,minNeighbors=5,minSize=(100, 100),flags = 0)
	# Draw a rectangle around the faces
	vel = Twist()        
	if(len(cracks)):
		for (x, y, w, h) in cracks:
			cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
           	vel.angular.z = 0
                vel.linear.x = 1.0
        publisher.publish(vel)

	
	# show the frame to our screen and increment the frame counter
	#cv2.imshow("Frame", frame)
          #  vel = Twist()
           # vel.angular.z = 0
           # vel.linear.x = 0.4
            #publisher.publish(vel)

        cv2.imshow("Camera Feed", image)  # show the image
        cv2.waitKey(1)  # refresh contents of image frame



if __name__ == "__main__":
    rospy.init_node("find_object")  # initialize the node
    robot = rospy.Publisher("/cmd_vel", Twist, queue_size=10)  # set up a publisher to control Turtlebot
    rospy.Subscriber("usb_cam/image_raw", Image, move_to_object, callback_args=robot)  # camera subscriber
    #rospy.Subscriber("rfid_data", String, on_rfid_found, queue_size=10)  # rfid data subscriber
    rospy.loginfo("Node `find_object` started...")  # loginfo that the node has been set up
    rospy.spin()  # keeps the script from exiting until the node is killed
