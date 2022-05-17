#! /usr/bin/env python

import time
from geometry_msgs.msg import PoseWithCovarianceStamped, Pose
from my_turtlebot_localization.srv import MyServiceMessage, MyServiceMessageResponse
import rospy


class SaveSpots(object):

    def __init__(self):
        self.pose = PoseWithCovarianceStamped()
        self.detection_dict = {}

        self._my_service = rospy.Service(
            '/save_spot', MyServiceMessage, self.srv_callback)
        self.pose_sub = rospy.Subscriber(
            '/amcl_pose', PoseWithCovarianceStamped, self.sub_callback)
        while self.pose_sub.get_num_connections() < 1:
            rospy.loginfo("Waiting for subscription to /amcl_pose")
            time.sleep(0.1)

    def sub_callback(self, msg):
        self.pose = msg

    def srv_callback(self, request):

        label = request.label

        response = MyServiceMessageResponse()

        if label != "end":
            self.detection_dict[label] = self.pose
            response.message = "Saved Pose"
            rospy.loginfo("position saved")

        else:
            with open("~/catkin_ws/my_turtlebot_localization/spots.txt", 'w') as file:

                for key, value in self.detection_dict.items():
                    if value:
                        file.write(str(key) + ':\n----------\n' +
                                   str(value) + '\n===========\n')

                response.message = "Written Poses to spots.txt file"

        response.navigation_successfull = True

        return response


if __name__ == "__main__":
    rospy.init_node('spots_node')
    save_spots_object = SaveSpots()
    rospy.spin()
