'''
hw3p5.py

   This is a skeleton for HW3 Problem 5.  Please EDIT.

   It creates a trajectory generation node to command the joint
   movements.

   Node:        /generator
   Publish:     /joint_states           sensor_msgs/JointState
'''

import rclpy
import numpy as np

from math               import pi, sin, cos, acos, atan2, sqrt, fmod

from rclpy.node         import Node
from sensor_msgs.msg    import JointState


#
#   Trajectory Class
#
class Trajectory():
    # Initialization.
    def __init__(self):
        self.cycle_time = 0
        self.old_time = 0
        self.new_time = 0

    # Declare the joint names.
    def jointnames(self):
        # Return a list of joint names
        return ['theta1', 'theta2', 'theta3']

    # Evaluate at the given time.
    def evaluate(self, t, dt):
        self.new_time = t
        delta_t = self.new_time - self.old_time
        position  = np.zeros
        omega = np.zeros
        
        a = np.array([0.6747,  0.508,  0.6435], dtype = float)        
        b = np.array([0.6747,  1.152, -0.6435], dtype = float)
        c = np.array([-2.466,  2.633, -0.6435], dtype = float)
        d = np.array([-2.466,  1.990,  0.6435], dtype = float)
        
        if 0 <= self.cycle_time < 1:
            omega = (b - a)
            position  = a + omega * delta_t 
            print('in A')
        elif 1 <= self.cycle_time < 1.5:
            omega = np.zeros(3)
            position = b
            self.old_time = self.new_time
            print(' holding ')
        elif 1.5 <=self.cycle_time < 2.5:
            omega = (c - b)
            position  = b + omega * delta_t
            print( ' in B')  
        elif 2.5 <= self.cycle_time < 3:
            omega = np.zeros(3)
            position = c
            self.old_time = self.new_time
            print( ' holding')
        elif 3 <= self.cycle_time < 4:
            omega = (d - c)
            position  = c + omega * delta_t
            print( ' in C') 
        elif 4 <= self.cycle_time < 4.5:
            omega = np.zeros(3)
            position = d
            self.old_time = self.new_time
            print( ' holding')
        elif 4.5 <= self.cycle_time < 5.5:
            omega = (a - d)
            position  = d + omega * delta_t
            print( ' in d')
        elif  5.5 <= self.cycle_time < 6:
            omega = np.zeros(3)
            position = a
            self.old_time = self.new_time
            print( ' holding')
        self.cycle_time+=dt
        if self.cycle_time >= 6:
            self.cycle_time = 0
            self.old_time = self.new_time
        print(self.cycle_time)
        # Return the position and velocity as python lists.
        return (list(position),list(omega))


#
#   Generator Node Class
#
#   This inherits all the standard ROS node stuff, but adds an
#   update() method to be called regularly by an internal timer and a
#   shutdown method to stop the timer.
#
#   Take the node name and the update frequency as arguments.
#
class Generator(Node):
    # Initialization.
    def __init__(self, name, rate):
        # Initialize the node, naming it 'generator'
        super().__init__(name)

        # Set up the trajectory.
        self.trajectory = Trajectory()
        self.jointnames = self.trajectory.jointnames()

        # Add a publisher to send the joint commands.
        self.pub = self.create_publisher(JointState, '/joint_states', 10)

        # Wait for a connection to happen.  This isn't necessary, but
        # means we don't start until the rest of the system is ready.
        self.get_logger().info("Waiting for a /joint_states subscriber...")
        while(not self.count_subscribers('/joint_states')):
            pass

        # Create a timer to trigger calculating/sending commands.
        self.timer     = self.create_timer(1/float(rate), self.update)
        self.dt        = self.timer.timer_period_ns * 1e-9
        self.t         = - self.dt
        self.get_logger().info("Running with dt of %f seconds (%fHz)" %
                               (self.dt, rate))

    # Shutdown
    def shutdown(self):
        # Destroy the timer, then shut down the node.
        self.timer.destroy()
        self.destroy_node()

    # Update - send a new joint command every time step.
    def update(self):
        # Grab the current time (from the ROS clock, since 1970).
        now = self.get_clock().now()

        # To avoid any time jitter enforce a constant time step in
        # integrate to get the current time.
        self.t += self.dt

        # Compute the desired joint positions and velocities for this time.
        (q, qdot) = self.trajectory.evaluate(self.t, self.dt)

        # Build up a command message and publish.
        cmdmsg = JointState()
        cmdmsg.header.stamp = now.to_msg()      # Current time for ROS
        cmdmsg.name         = self.jointnames   # List of joint names
        cmdmsg.position     = q                 # List of joint positions
        cmdmsg.velocity     = qdot              # List of joint velocities
        self.pub.publish(cmdmsg)


#
#  Main Code
#
def main(args=None):
    # Initialize ROS.
    rclpy.init(args=args)

    # Initialize the generator node for 100Hz udpates.
    generator = Generator('generator', 100)

    # Spin, meaning keep running (taking care of the timer callbacks
    # and message passing), until interrupted.
    rclpy.spin(generator)

    # Shutdown the node and ROS.
    generator.shutdown()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
