from typing import Callable, Tuple

from raydium.linalg import Vec3, vec3


ColorFunction = Callable[[Vec3], Vec3]


def blue_blend_background_color(v: Vec3) -> Vec3:
    """
    The unit vector v returns a color that is a linear blend of light blue and dark blue
    depending on the y value of v
    """
    u = 0.5 * (1.0 + v[1])
    return u * vec3(0.7, 0.8, 0.9) + (1.0 - u) * vec3(0.05, 0.05, 0.2)


class Scene:
    """A scene containing a collection of objects."""
    def __init__(self, objects: list, background_color_func: ColorFunction):
        """
        Constructor.

        Parameters
        ----------
        objects: list
            collection of scene objects
        background_color_func: callable
            a callable taking a direction vector returning the background pixel color
        """
        self.objects = objects
        self.background_color = background_color_func

    def hit_object(self, origin: Vec3, direction: Vec3) -> Tuple[bool, float, int]:
        """
        Checks to see if a tracing ray hits an object.

        Parameters
        ----------
        origin: vec3
            ray origin (camera location)
        direction: vec3
            ray direction (unit vector)

        Returns
        -------
        tuple: (hit, t, object)
        """
        t_min = 9e8
        i_min = -1
        hit = False
        for idx, obj in enumerate(self.objects):
            t = obj.hit(origin, direction)
            if 1e-4 <= t < t_min:
                t_min = t
                i_min = idx
                hit = True
        return hit, t_min, i_min
