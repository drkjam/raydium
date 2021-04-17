"""
Renders solid and hollow glass spheres.
"""
import os

from raydium.io import show_image, save_image
from raydium.geometry import Sphere
from raydium.linalg import vec3
from raydium.scenery import Scene, blue_blend_background_color
from raydium.raytracer import render_scene


def generate_objects():
    """Return a collection of spheres."""
    big_radius = 10000.0

    spheres = [
        #   Light emitting sphere.
        Sphere(
            radius=1.0,
            centre=vec3(0.05, 3.0, -10.0),
            emitted_color=vec3(1.0, 1.0, 1.0),
            diffuse_reflectivity=vec3(0.0, 0.0, 0.0),
            specular_reflectivity=vec3(0.0, 0.0, 0.0),
            refractive_index=1.0
        ),
        #   Large sphere (floor).
        Sphere(
            radius=big_radius,
            centre=vec3(0.0, -big_radius - 1.0, 0.0),
            emitted_color=vec3(0.0, 0.0, 0.0),
            diffuse_reflectivity=vec3(0.0, 0.0, 0.0),
            specular_reflectivity=vec3(0.7, 0.7, 0.7),
            refractive_index=1.0
        ),

        #   Glass sphere (with a refractive component).
        Sphere(
            radius=1.0,
            centre=vec3(1.0, 1.0, -7.0),
            emitted_color=vec3(0.0, 0.0, 0.0),
            diffuse_reflectivity=vec3(0.0, 0.0, 0.0),
            specular_reflectivity=vec3(0.7, 0.6, 0.5),
            refractive_index=1.5
        ),

        #   Sphere inside the glass sphere to "hollow" it out (note inverted radius to switch direction of normals).
        Sphere(
            radius=-0.95,
            centre=vec3(1.0, 1.0, -7.0),
            emitted_color=vec3(0.0, 0.0, 0.0),
            diffuse_reflectivity=vec3(0.0, 0.0, 0.0),
            specular_reflectivity=vec3(0.7, 0.6, 0.5),
            refractive_index=1.5
        ),

        #   Smaller glass sphere (solid).
        Sphere(
            radius=0.25,
            centre=vec3(-0.75, 0.74, -3.0),
            emitted_color=vec3(0.0, 0.0, 0.0),
            diffuse_reflectivity=vec3(0.0, 0.0, 0.0),
            specular_reflectivity=vec3(0.7, 0.6, 0.5),
            refractive_index=1.5
        ),

        #   Metal mirrored sphere.
        Sphere(
            radius=1.0,
            centre=vec3(-1.0, 0.0, -6.0),
            emitted_color=vec3(0.0, 0.0, 0.0),
            diffuse_reflectivity=vec3(0.0, 0.0, 0.0),
            specular_reflectivity=vec3(1.0, 1.0, 1.0),
            refractive_index=1.0
        ),
    ]

    return spheres


def main():
    display = False

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
    filename = os.path.join(image_path, f'glass_spheres_{resolution}.png')
    print(f'generating image (resolution: {resolution}, samples per pixel: {samples}, max bounces: {max_bounces})')

    scene = Scene(objects=generate_objects(), background_color_func=blue_blend_background_color)
    image = render_scene(scene, width, height, num_samples=samples, max_bounces=max_bounces)

    if display:
        show_image(image)

    print(f'saving image to {filename}')
    save_image(image, filename)


if __name__ == '__main__':
    main()
