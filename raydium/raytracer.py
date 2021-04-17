import numpy as np
from numpy import math
from numpy import random

from raydium.linalg import Vec3, vec3, not_zero, unit_vector
from raydium.scenery import Scene
from raydium.io import Image


def reflect(v: Vec3, normal: Vec3) -> Vec3:
    """
    Reflect direction vector based on surface normal vector.

    Parameters
    ----------
    v: Vec3
        ray direction vector.
    normal: vec
        surface normal of object.

    Returns
    -------
    Vec3: new ray direction vector.
    """
    return v - 2.0 * np.dot(v, normal) * normal


def refract(v: Vec3, normal: Vec3, ni: float, nt: float) -> (bool, Vec3):
    """
    Calculate refraction direction vector where applicable using surface normal vector.

    Parameters
    ----------
    v: Vec3
        ray direction vector.
    normal: vec
        surface normal of object.
    ni: float
    nt: float

    Returns
    -------
    tuple: (bool, Vec3): can refract and new ray direction vector.
    """
    eta = ni / nt
    c1 = -np.dot(v, normal)
    w = eta * c1
    c2m = (w - eta) * (w + eta)
    if c2m < -1.0:
        return False, v
    else:
        return True, eta * v + (w - math.sqrt(1.0 + c2m)) * normal


def glass_fresnel(c: float) -> float:
    """Calculate total internal reflection (Fresnel glass lens effect)."""
    c5 = math.pow(1 - c, 5)
    return 0.05 * (1 - c5) + 0.95 * c5


def random_on_sphere(centre: Vec3, radius: float) -> Vec3:
    """Calculate a random point on the surface of a given sphere."""
    a = random.uniform(-1.0, 1.0)
    b = math.sqrt(1.0 - a * a)
    phi = random.uniform(0.0, 2.0 * np.pi)
    x = radius * b * math.cos(phi)
    y = radius * b * math.sin(phi)
    z = radius * a
    return centre + vec3(x, y, z)


def trace_ray(origin: Vec3, direction: Vec3, scene: Scene, max_bounces: int = 30) -> Vec3:
    """
    Performs a path trace of an individual ray to determine the color of a scene pixel.

    Parameters
    ----------
    origin: vec3
        ray origin (camera location)
    direction: vec3
        ray direction (unit vector)
    scene: Scene
        collection of scene objects
    max_bounces: int
        maximum number of bounces to calculate

    Returns
    -------
    vec3: pixel color
    """
    multiplier = vec3(1.0, 1.0, 1.0)
    color = multiplier * scene.background_color(direction)

    bounces = 0
    while bounces < max_bounces:
        bounces += 1
        hit, t, i = scene.hit_object(origin, direction)
        obj = scene.objects[i]
        if hit:
            if not_zero(obj.emitted_color):
                color = multiplier * obj.emitted_color
                break
            origin = origin + t * direction
            surface_normal = (1.0 / obj.radius) * (origin - obj.centre)
            if not_zero(obj.diffuse_reflectivity):
                target = random_on_sphere(origin + surface_normal, 0.99)
                direction = unit_vector(target - origin)
                multiplier *= obj.diffuse_reflectivity
            elif obj.refractive_index > 1.0:
                cos_incident = np.dot(direction, surface_normal)
                if cos_incident < 0.0:
                    ni, nt = 1.0, obj.refractive_index
                else:
                    ni, nt = obj.refractive_index, 1.0
                    surface_normal = -surface_normal
                can_refract, refracted_direction = refract(direction, surface_normal, ni, nt)
                if can_refract:
                    cos1 = abs(cos_incident)
                    cos2 = abs(np.dot(refracted_direction, surface_normal))
                    cos3 = min(cos1, cos2)
                    prob_reflect = glass_fresnel(cos3)
                    if np.random.uniform(0.0, 1.0) < prob_reflect:
                        direction = reflect(direction, surface_normal)
                    else:
                        direction = refracted_direction
                else:
                    direction = reflect(direction, surface_normal)
            else:
                direction = reflect(direction, surface_normal)
                multiplier *= obj.specular_reflectivity
        else:
            color = multiplier * scene.background_color(direction)
            break

    return color


def render_scene(scene: Scene, width: int, height: int, num_samples: int = 2, max_bounces: int = 30) -> Image:
    """
    Render an image of a scene with ray tracing.

    Parameters
    ----------
    scene: Scene
        container of all object in the scene being rendered
    width: int
        image width
    height: int
        image height
    num_samples: int
        number of samples to calculate per pixel
    max_bounces: int
        maximum number of ray bounces per pixel
    Returns
    -------
    Image: an image of the rendered scene
    """
    image = np.random.random(size=(height, width, 3))
    aspect_ratio = height / width
    depth = 2.0
    for row in range(height):
        if row % 50 == 0:
            print(row)
        for column in range(width):
            accumulator = vec3(0.0, 0.0, 0.0)
            for sample in range(num_samples):
                origin = vec3(0.0, 0.0, 0.0)
                u = (column + 0.5) / width
                v = (row + 0.5) / height
                direction = unit_vector(vec3(2.0 * u - 1.0, aspect_ratio * (2.0 * v - 1.0), -depth))
                pixel_color = trace_ray(origin, direction, scene, max_bounces)
                accumulator += pixel_color
            image[height-row - 1, column, :] = accumulator / num_samples
    print(height)

    return image
