import numpy as np


class Metrics():

    @staticmethod
    def dists(x, y, t):
        return np.sqrt(np.diff(x)**2 + np.diff(y)**2)


    @staticmethod
    def vel_2d(x, y, t):
        return Metrics.dists(x, y, t)/np.diff(t)


    @staticmethod
    def vel_1d(x, t):
        return np.diff(x)/np.diff(t)     


    @staticmethod
    def accel_2d(x, y, t):
        return np.diff(Metrics.vel_2d(x, y, t))/np.diff(t)[1:]


    @staticmethod
    def accel_1d(x, t):
        return np.diff(Metrics.vel_1d(x, t))/np.diff(t)[1:]


    @staticmethod
    def inv_curv(x, y, t):
        """
        Measures inverse curvature (radius of circle) of a path
        """
        vx, vy = Metrics.vel_1d(x, t),   Metrics.vel_1d(y, t)
        ax, ay = Metrics.accel_1d(x, t), Metrics.accel_1d(y, t)
        
        return ((vx**2 + vy**2)**(3/2))/(ax*vy - ay*vx)


    @staticmethod
    def cent_accel(x, y, t):
        """
        Measures centripetal acceleration of a path
        """
        r = Metrics.inv_curv(x, y, t)
        vel = Metrics.vel_2d(x, y, t)

        return (vel**2)/r


    # https://docs.google.com/document/d/14p6-5uzQDzLpnwgPDCXvSsaNiqN7Z6rlgdWtmrq4M-8
    @staticmethod
    def angle(x, y, t):
        """
        Measures the angles made by the path
        """
        dx, dy = np.diff(x), np.diff(y)
        theta1  = np.arctan2(dy, dx)

        # Construct vector angles from parametric velocities
        theta1 = np.arctan2(dy[1:], dx[1:])
        theta2 = np.arctan2(dy[:-1], dx[:-1])

        # Make stacks 0 angle change
        mask = np.where(np.logical_and(dy[1:] == 0, dx[1:] == 0))[0]
        theta1[mask] = theta1[mask - 1]

        mask = np.where(np.logical_and(dy[:-1] == 0, dx[:-1] == 0))[0]
        theta2[mask] = theta2[mask - 1]

        # Calculate the parametric difference between the two positions
        vx = np.cos(theta2 - theta1)
        vy = np.sin(theta2 - theta1)

        # Convert parametric difference into angle difference
        return np.arctan2(vy, vx)


    @staticmethod
    def avg_ang_vel(x, y, t):
        """
        Average angular velocity

        Average velocity is how fast the cursor moves in a circle. There are two types of patterns to consider: 
        zig-zag and circular. A zig-zag pattern has no angular velocity, but has linear velocity. In a zig-zag
        pattern one angle would be positive indicating a rotation in a clockwise direction, and another angle 
        would be negative indicating a rotation in a counter-clockwise direction. Ultimately those two cancel 
        out to result in no overall rotation direction. A circular pattern would have either both angles positive 
        or both angles negative, yielding a net negative or a net positive rotation direction.
        """
        angle = Metrics.angle(x, y, t)
        rot   = 0.5*(angle[1:] + angle[:-1])
        dt    = t[2:] - t[:-2]

        return rot/dt


    @staticmethod
    def inst_ang_vel(x, y, t):
        """
        Instantanious angular velocity
        """
        angle = Metrics.angle(x, y, t)
        dt    = np.diff(t)[1:]

        return angle/dt


    @staticmethod
    def accel_ang_vel(x, y, t):
        """
        Angular velocity
        """
        dx, dy = np.diff(x), np.diff(y)
        r = Metrics.inv_curv(x, y, t)
        cent_accel = Metrics.cent_accel(x, y, t)

        # Center of circle making the curve
        px = x[1:] + (r*dy)/np.sqrt(dx**2 + dy**2)
        py = y[1:] + (r*dx)/np.sqrt(dx**2 + dy**2)

        # Normalized acceleration vector
        acx = cent_accel*(px/np.sqrt(dx**2 + dy**2))
        acy = cent_accel*(py/np.sqrt(dx**2 + dy**2))

        return Metrics.inst_ang_vel(acx, acy, t[1:])