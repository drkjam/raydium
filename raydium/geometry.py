import numpy as np
from numpy import math
from raydium.linalg import Vec3


class Sphere:
    """Represents a sphere and its various properties."""
    def __init__(self, radius: float, centre: Vec3, emitted_color: Vec3, diffuse_reflectivity: Vec3,
                 specular_reflectivity: Vec3, refractive_index: float):
        """
        Constructor.

        Parameters
        ----------
        radius: float
            radius of sphere
        centre: Vec3
            position of sphere's centre
        emitted_color: Vec3
            color of light emitted by the object (RGB normalized to interval [0,1])
        diffuse_reflectivity: Vec3
            how much light scatters when it hits the surface
        specular_reflectivity: Vec3
            fraction of reflected light attenuated for each color channel (0.0 - no reflection, 1.0 - full reflection)
        refractive_index: float
            refraction index of material surface (air is 1.0003, water is 1.333, diamond is 2.417, etc)
        """
        self.radius = radius
        self.centre = centre
        self.emitted_color = emitted_color
        self.diffuse_reflectivity = diffuse_reflectivity
        self.specular_reflectivity = specular_reflectivity
        self.refractive_index = refractive_index

    def hit(self, origin: Vec3, direction: Vec3) -> float:
        """Calculates the distance between origin and sphere surface from an incoming ray."""
        oc = origin - self.centre
        qb = np.dot(oc, direction)
        qc = np.dot(oc, oc) - self.radius * self.radius
        discriminant = qb * qb - qc
        if discriminant > 0:
            t = (-qb - math.sqrt(discriminant))
            if t > 0.00001:
                return t
            t = (-qb + math.sqrt(discriminant))
            if t > 0.00001:
                return t
        return 1e9
