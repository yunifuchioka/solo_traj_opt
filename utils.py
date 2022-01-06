import numpy as np
import casadi as ca


# given 1x3 vector, returns 3x3 skew symmetric cross product matrix
def skew(s):
    return np.array([[0, -s[2], s[1]], [s[2], 0, -s[0]], [-s[1], s[0], 0]])


# derives a symbolic version of the skew function
def derive_skew():
    s = ca.SX.sym('s', 3)

    skew_sym = ca.SX(3, 3)
    # skew_sym = ca.SX.zeros(3, 3)
    skew_sym[0, 1] = -s[2]
    skew_sym[0, 2] = s[1]
    skew_sym[1, 0] = s[2]
    skew_sym[1, 2] = -s[0]
    skew_sym[2, 0] = -s[1]
    skew_sym[2, 1] = s[0]

    return ca.Function('skew', [s], [skew_sym])


# given axis and angle, returns 3x3 rotation matrix
def rotMat(s, th):
    # normalize s if isn't already normalized
    norm_s = np.linalg.norm(s)
    assert norm_s != 0.0
    s_normalized = s / norm_s

    # Rodrigues' rotation formula
    skew_s = skew(s_normalized)
    return np.eye(3) + np.sin(th) * skew_s + (1.0 - np.cos(th)) * skew_s @ skew_s


def derive_rotMat():
    s = ca.SX.sym('s', 3)
    th = ca.SX.sym('th')
    skew_func = derive_skew()
    skew_sym = skew_func(s)

    rotMat_sym = ca.SX.eye(3) + ca.sin(th)*skew_sym + \
        (1-ca.cos(th))*skew_sym@skew_sym
    return ca.Function('rotMat', [s, th], [rotMat_sym])


# given position vector and rotation matrix, returns 4x4 homogeneous
# transformation matrix
def homog(p, R):
    return np.block([[R, p[:, np.newaxis]], [np.zeros((1, 3)), 1]])


# multiplication between a 4x4 homogenous transformation matrix and 3x1
# position vector, returns 3x1 position
def mult_homog_point(T, p):
    p_aug = np.concatenate((p, [1.0]))
    return (T @ p_aug)[:3]


# test functions
if __name__ == "__main__":
    x_axis = np.eye(3)[:, 0]
    y_axis = np.eye(3)[:, 1]
    z_axis = np.eye(3)[:, 2]

    print("\ntest skew")
    skew_func = derive_skew()
    print(skew(np.array([1, 2, 3])))
    print(skew_func(np.array([1, 2, 3])))
    s = ca.SX.sym('s', 3)
    print(skew_func(s))

    print("\ntest rotMat")
    rotMat_func = derive_rotMat()
    print(rotMat(x_axis, np.pi/4))
    print(rotMat_func(x_axis, np.pi/4))
    print(rotMat(y_axis, np.pi/4))
    print(rotMat_func(y_axis, np.pi/4))
    print(rotMat(z_axis, np.pi/4))
    print(rotMat_func(z_axis, np.pi/4))
    print(np.linalg.norm(rotMat(x_axis, np.pi/4) @
          rotMat(x_axis, np.pi/4).T - np.eye(3)))
    print(np.linalg.norm(rotMat(x_axis, np.pi/4).T @
          rotMat(x_axis, np.pi/4) - np.eye(3)))
    th = ca.SX.sym('th')
    print(rotMat_func(s, th))
    print(np.linalg.norm(rotMat_func(x_axis, np.pi/4) @
          rotMat_func(x_axis, np.pi/4).T - np.eye(3)))

    print("\ntest homog")
    p = np.array([1, 2, 3])
    R = rotMat(x_axis, np.pi/4)
    print(homog(p, R))

    print("\ntest mult_homog_point")
    print(mult_homog_point(homog(x_axis, R), y_axis))

    import ipdb
    ipdb.set_trace()
