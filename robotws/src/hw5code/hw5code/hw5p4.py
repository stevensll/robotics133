'''hw5p4.py

   This is skeleton code for HW5 Problem 4.  Please EDIT.

   This moves the tip in a straight line (tip spline), then returns in
   a joint spline.

'''

import rclpy
import numpy as np

from math                       import pi, sin, cos, acos, atan2, sqrt, fmod

# Grab the utilities
from GeneratorNode      import GeneratorNode
from TrajectoryUtils    import goto, spline, goto5, spline5

# Grab the fkin and Jac from P1.
from hw5p1              import fkin, Jac


#
#   Trajectory Class
#
class Trajectory():
    # Initialization.
    def __init__(self, node):
        # Define the known tip/joint positions.
        self.qA = np.radians(np.array([ 0, 60, -120])).reshape(3,1)
        self.xA = fkin(self.qA)

        self.qD = np.array(self.qA)
        self.xD = np.array([0.5, -0.5, 1.0]).reshape(3,1)

        # Select the leg duration.
        self.T = 3.0

        # Initialize the parameters and anything stored between cycles!
        self.lamb = 20

    # Declare the joint names.
    def jointnames(self):
        # Return a list of joint names
        return ['theta1', 'theta2', 'theta3']

    # Evaluate at the given time.
    def evaluate(self, t, dt):
        # End after one cycle.
        if (t > 2*self.T):
          return None
        
        # First modulo the time by 2 legs.
        t = fmod(t, 2*self.T)

        # COMPUTE THE MOTION.
        q = self.qD
        q_t_dt = q
        qdot = np.array([0.0,0.0,0.0]).reshape(3,1)
        if (t < self.T):
            q_t_dt = q 
            # get the translational position and velocity
            x_t, x_t_dot       = goto(t,    self.T, self.xA, self.xD)
            x_t_dt, x_t_dt_dot = goto(t-dt, self.T, self.xA, self.xD)
            # note that q(t-dt) is q at this point, we didn't update q yet
            x_diff = x_t_dt - fkin(q_t_dt)
            # find the respective angular velocity
            qdot = np.linalg.inv(Jac(q)) @ (x_t_dot + self.lamb * x_diff)
            # numerically integrate the angle 
            print(t, self.qA)
            q+=qdot * dt
            self.qD = q
        else:
        # return from qD to qA smoothly without care for the tip position
            q, qdot = goto(t-3.0, self.T, self.qD, self.qA)
        # Return the position and velocity as python lists!
        # print(t,self.qA)
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
