"""
Renders solid a glass sphere with bubbles in it.
"""
import os
import time

import numpy as np
from numpy import math
from numpy import random

from raydium.io import show_image, save_image
from raydium.geometry import Sphere
from raydium.linalg import vec3, Vec3
from raydium.scenery import Scene, blue_blend_background_color
from raydium.raytracer import render_scene


def random_in_sphere(centre: Vec3, radius: float) -> Vec3:
    """Calculate centre of a random sphere of specified radius within the bounds of a reference sphere."""
    a = random.uniform(-1.0, 1.0)
    b = math.sqrt(1.0 - a * a)
    phi = random.uniform(0.0, 2.0 * np.pi)
    r = radius * pow(random.uniform(0.0, 1.0), 0.33333)
    x = r * b * math.cos(phi)
    y = r * b * math.sin(phi)
    z = r * a
    return centre + vec3(x, y, z)


def generate_glass_spheres(seed=None):
    """Return a collection of spheres."""
    if seed is not None:
        random.seed(seed)

    glass_sphere_centre = vec3(1.0, 0.0, -5.0)

    spheres = [
        #   Light emitting sphere.
        Sphere(
            radius=1.0,
            centre=vec3(-1.0, 0.0, -5.0),
            emitted_color=vec3(3.0, 3.0, 3.0),
            diffuse_reflectivity=vec3(0.0, 0.0, 0.0),
            specular_reflectivity=vec3(0.0, 0.0, 0.0),
            refractive_index=1.0
        ),

        #   Glass sphere (with a refractive component).
        Sphere(
            radius=1.0,
            centre=glass_sphere_centre,
            emitted_color=vec3(0.0, 0.0, 0.0),
            diffuse_reflectivity=vec3(0.0, 0.0, 0.0),
            specular_reflectivity=vec3(0.0, 0.0, 0.0),
            refractive_index=1.5
        ),
    ]

    #   Add bubbles (invert radius and associated surface normals).
    num_small_spheres = 10
    small_radius = 0.3 * math.pow(1.0 / num_small_spheres, 0.333)
    for sphere in range(num_small_spheres):
        spheres.append(Sphere(
            radius=-small_radius,
            centre=random_in_sphere(glass_sphere_centre, 1.0 - 1.1 * small_radius),
            emitted_color=vec3(0.0, 0.0, 0.0),
            diffuse_reflectivity=vec3(0.0, 0.0, 0.0),
            specular_reflectivity=vec3(0.0, 0.0, 0.0),
            refractive_index=1.5
        ))

    return spheres


def main():
    display = False
    # now = time.time()
    # seed = int(now)
    seed = 1618611775

    pwd = os.path.dirname(__file__)
    image_path = os.path.abspath(os.path.join(pwd, '..', 'images'))
    if not os.path.exists(image_path):
        os.makedirs(image_path)

    #   Quality settings (tune with take care, tweaking these can lead to very long run times).
    width = 640
    height = 480
    samples = 2
    max_bounces = 30

    resolution = f'{width}x{height}'
    filename = os.path.join(image_path, f'glass_sphere_bubbles_{seed}_{resolution}.png')
    print(f'generating image (resolution: {resolution}, samples per pixel: {samples},'
          f'max bounces: {max_bounces}, seed: {seed!r})')

    scene = Scene(objects=generate_glass_spheres(seed), background_color_func=blue_blend_background_color)
    image = render_scene(scene, width, height, num_samples=samples, max_bounces=max_bounces)

    if display:
        show_image(image)

    print(f'saving image to {filename}')
    save_image(image, filename)


if __name__ == '__main__':
    main()
