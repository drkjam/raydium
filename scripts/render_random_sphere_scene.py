"""
Renders a scene of randomly generated spheres with various surface properties.

Fix the seed for the PRNG to regenerate the same scene.
"""
import os
import time

from numpy import random

from raydium.io import show_image, save_image
from raydium.geometry import Sphere
from raydium.linalg import vec3
from raydium.scenery import Scene, blue_blend_background_color
from raydium.raytracer import render_scene


def generate_random_spheres(seed=None):
    """Return a collection of spheres with randomised properties."""
    if seed is not None:
        random.seed(seed)

    white = vec3(1.0, 1.0, 1.0)
    big_radius = 10000.0

    spheres = [
        #   Scene lighting sphere.
        Sphere(
            radius=5.0,
            centre=vec3(0.0, 4.0, -10.0),
            emitted_color=white,
            diffuse_reflectivity=vec3(0.0, 0.0, 0.0),
            specular_reflectivity=vec3(0.0, 0.0, 0.0),
            refractive_index=1.0
        ),
        #   Large sphere (floor).
        Sphere(
            radius=big_radius,
            centre=vec3(0.0, -big_radius - 1.0, 0.0),
            emitted_color=vec3(0.0, 0.0, 0.0),
            diffuse_reflectivity=vec3(1.0, 1.0, 1.0),
            specular_reflectivity=vec3(0.0, 0.0, 0.0),
            refractive_index=1.0
        ),
    ]

    # build random sphere configurations
    for i in range(9):
        radius = random.uniform(0.2, 0.5)
        if random.uniform(0.0, 1.0) < 0.5:
            specular_ref = vec3(random.uniform(0.5, 0.9), random.uniform(0.5, 0.9), random.uniform(0.5, 0.9))
        else:
            specular_ref = vec3(random.uniform(0.1, 0.9), random.uniform(0.1, 0.9), random.uniform(0.1, 0.9))
        sphere = Sphere(
            radius=radius,
            centre=vec3(random.uniform(-5.0, 5.0), -1.0 + radius, random.uniform(-3.0, -15.0)),
            emitted_color=vec3(0.0, 0.0, 0.0),
            diffuse_reflectivity=vec3(0.0, 0.0, 0.0),
            specular_reflectivity=specular_ref,
            refractive_index=1.0
        )

        spheres.append(sphere)

    for i in range(11):
        radius = random.uniform(0.2, 0.5)
        spheres.append(Sphere(
            radius=radius,
            centre=vec3(random.uniform(-5.0, 5.0), -1.0 + radius, random.uniform(-3.0, -15.0)),
            emitted_color=vec3(0.0, 0.0, 0.0),
            diffuse_reflectivity=vec3(0.0, 0.0, 0.0),
            specular_reflectivity=vec3(0.0, 0.0, 0.0),
            refractive_index=1.5
        ))

    for i in range(4):
        radius = random.uniform(0.2, 0.7)
        center = vec3(random.uniform(-4.0, 4.0), -1.0 + radius, random.uniform(-2.0, -10.0))

        spheres.append(Sphere(
            radius=radius,
            centre=center,
            emitted_color=vec3(0.0, 0.0, 0.0),
            diffuse_reflectivity=vec3(0.0, 0.0, 0.0),
            specular_reflectivity=vec3(0.0, 0.0, 0.0),
            refractive_index=1.5
        ))

        spheres.append(Sphere(
            radius=-0.9 * radius,
            centre=center,
            emitted_color=vec3(0.0, 0.0, 0.0),
            diffuse_reflectivity=vec3(0.0, 0.0, 0.0),
            specular_reflectivity=vec3(0.0, 0.0, 0.0),
            refractive_index=1.5
        ))

    return spheres


def main():
    display = False
    now = time.time()
    # now = time.time()
    # seed = int(now)
    # seed = 1618611390
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
    filename = os.path.join(image_path, f'random_sphere_scene_{seed}_{resolution}.png')
    print(f'generating image (resolution: {resolution}, samples per pixel: {samples},'
          f'max ray bounces: {max_bounces}, seed: {seed!r})')

    scene = Scene(objects=generate_random_spheres(seed), background_color_func=blue_blend_background_color)
    image = render_scene(scene, width, height, num_samples=samples, max_bounces=max_bounces)

    if display:
        show_image(image)

    print(f'saving image to {filename}')
    save_image(image, filename)


if __name__ == '__main__':
    main()
