import numpy as np

Vec3 = np.array


def vec3(x: float, y: float, z: float) -> Vec3:
    """Returns a 3D vector (as a numpy array)."""
    return np.array((x, y, z))


def unit_vector(v: Vec3) -> Vec3:
    """Returns the unit vector for the specified vector."""
    length = np.math.sqrt(np.dot(v, v))
    return v / length


def not_zero(c: Vec3) -> Vec3:
    """Returns True if vector is not a zero vector, False otherwise."""
    return np.dot(c, c) > 1e-6
