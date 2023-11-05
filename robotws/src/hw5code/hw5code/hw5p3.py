'''hw5p3.py

   This is skeleton code for HW5 Problem 3.  Please EDIT.

   Repeatedly and smoothly move the 3DOF.

'''

import rclpy
import numpy as np

from math                       import pi, sin, cos, acos, atan2, sqrt, fmod

# Grab the utilities
from GeneratorNode      import GeneratorNode
from TrajectoryUtils    import goto, spline, goto5, spline5


#
#   Trajectory Class
#
class Trajectory():
    # Initialization.
    def __init__(self, node):
        # Define the three joint positions.
        self.qA = np.radians(np.array([   0,  60, -120])).reshape(3,1)
        self.qB = np.radians(np.array([ -90, 135,  -90])).reshape(3,1)
        self.qC = np.radians(np.array([-180,  60, -120])).reshape(3,1)

    # Declare the joint names.
    def jointnames(self):
        # Return a list of joint names
        return ['theta1', 'theta2', 'theta3']

    # Evaluate at the given time.
    def evaluate(self, t, dt):
        # First modulo the time by 6 seconds
        if(t > 6):
            return None
        t = fmod(t, 6.0)

        # Compute the joint values.
        v_qB = spline(2, 4.0, self.qA, self.qC, 0,0)[1]
        print(v_qB)
        if   (t < 2.0):        (q, qdot) = spline(t    , 2.0, self.qA, self.qB, 0, v_qB)
        elif (2.0 < t <= 4.0): (q, qdot) = spline(t-2.0, 2.0, self.qB, self.qC, v_qB, 0)
        else:                  (q, qdot) = spline(t-4.0, 2.0, self.qC, self.qA, 0, 0)
        
        # get the time at qB for a continuous movement from qA to qC
        print(spline(2, 4.0, self.qA, self.qC, 0,0))
        
        # Return the posiion and velocity as flat python lists!
        return (q.flatten().tolist(), qdot.flatten().tolist())
     

#
#  Main Code
#
def main(args=None):
    # Initialize ROS.
    rclpy.init(args=args)

    # Initialize the generator node for 100Hz udpates, using the above
    # Trajectory class.
    generator = GeneratorNode('generator', 100, Trajectory)

    # Spin, meaning keep running (taking care of the timer callbacks
    # and message passing), until interrupted or the trajectory ends.
    generator.spin()
    # Shutdown the node and ROS.
    generator.shutdown()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
