"""Packed, repeatable PBR surfaces; all detail survives glTF export as image maps."""
import math
import bpy
import numpy as np

CACHE = {}


def noise_field(n, seed, frequency):
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:n, 0:n] / n
    value = np.zeros((n, n))
    weight = 0
    for octave in range(3):
        f = max(2, int(frequency / 4 * 2**octave))
        grid = rng.random((f,f)) - .5
        xx,yy=x*f,y*f
        ix,iy=xx.astype(int),yy.astype(int)
        u,v=xx-ix,yy-iy
        u=u*u*(3-2*u);v=v*v*(3-2*v)
        interpolated=(grid[iy%f,ix%f]*(1-u)+grid[iy%f,(ix+1)%f]*u)*(1-v)+(grid[(iy+1)%f,ix%f]*(1-u)+grid[(iy+1)%f,(ix+1)%f]*u)*v
        amplitude=.5**octave
        value+=interpolated*amplitude;weight+=amplitude
    return value/weight


def image(name, values, data=False):
    n = values.shape[0]
    img = bpy.data.images.new('TEX-Art-' + name, width=n, height=n, alpha=False)
    if data:
        img.colorspace_settings.name = 'Non-Color'
    pixels = np.ones((n, n, 4), dtype=np.float32)
    pixels[:, :, :3] = values if values.ndim == 3 else values[:, :, None]
    img.pixels.foreach_set(pixels.ravel())
    img.pack()
    return img


def fields(kind):
    if kind in CACHE:
        return CACHE[kind]
    n = 512
    yy, xx = np.mgrid[0:n, 0:n] / n
    broad = noise_field(n, 17, 4)
    fine = noise_field(n, 51, 34)
    micro = noise_field(n, 29, 100)
    if kind == 'wood':
        warp = xx + .035 * np.sin(yy * math.tau) + .018 * np.sin(yy * math.tau * 3 + 1)
        grain = np.sin(warp * math.tau * 112 + broad * 18)
        pores = np.maximum(0, np.sin(warp * math.tau * 83 + broad * 14)) ** 14
        height = .47 + grain * .006 - pores * .012 + broad * .04 + fine * .012
        value = .94 + broad * .32 + grain * .025 - pores * .05
        # Dark growth rings wrap naturally around elongated knots.
        for kx, ky in [(0.27, .3), (.78, .74)]:
            r = np.sqrt(((xx - kx) * 1.6) ** 2 + ((yy - ky) * .45) ** 2)
            mask = np.exp(-r * r / .012)
            value -= mask * (.06 + .045 * np.sin(r * 340))
            height += mask * .005 * np.sin(r * 340)
        roughness = .65 + broad * .3 + pores * .16
        strength = .16
    elif kind == 'cloth':
        weave = np.sin(xx * math.tau * 128) * np.sin(yy * math.tau * 128)
        height = .5 + weave * .014 + broad * .015
        value = .97 + broad * .09 + weave * .015
        roughness = .86 + broad * .12
        strength = .1
    elif kind in ['grass', 'soil']:
        height = .5 + broad * .04 + fine * .10 + micro * .04
        value = .92 + broad * .7 + fine * .22 + micro * .15
        roughness = .92 + fine * .08
        strength = .2
    elif kind == 'metal':
        height = .5 + fine * .018 + micro * .01
        value = .94 + broad * .15 + fine * .03
        roughness = .34 + broad * .25 + fine * .09
        strength = .08
    else:
        strata = np.sin(yy * math.tau * 10 + broad * 3) if kind == 'cliff' else np.zeros_like(xx)
        pits = np.maximum(0, -micro - .13) * .15
        height = .5 + broad * .06 + fine * .09 + strata * .008 - pits
        value = .94 + broad * .34 + fine * .1 + strata * .025 - pits * .7
        roughness = .84 + fine * .13
        strength = .22
    dx = (np.roll(height, -1, 1) - np.roll(height, 1, 1)) * 18 * strength
    dy = (np.roll(height, -1, 0) - np.roll(height, 1, 0)) * 18 * strength
    normal = np.stack([-dx, -dy, np.ones_like(dx)], -1)
    normal /= np.linalg.norm(normal, axis=2)[..., None]
    normal_image = image(kind + '-normal', normal * .5 + .5, True)
    rough_image = image(kind + '-roughness', np.clip(roughness, .15, .99), True)
    CACHE[kind] = value, normal_image, rough_image
    return CACHE[kind]


def apply_surface(material, shader, rgb, kind):
    value, normal_image, rough_image = fields(kind)
    color = np.clip(np.array(rgb)[None, None, :] * value[:, :, None], 0, 1)
    # Generated packed image pixels are serialized as supplied by this export path.
    # Keep the authored sRGB values: linearizing here darkens them a second time in glTF.
    color_image = image(material.name + '-color', color)
    nodes, links = material.node_tree.nodes, material.node_tree.links
    for img, socket in [(color_image, 'Base Color'), (rough_image, 'Roughness')]:
        tex = nodes.new('ShaderNodeTexImage')
        tex.image = img
        links.new(tex.outputs['Color'], shader.inputs[socket])
    tex = nodes.new('ShaderNodeTexImage')
    tex.image = normal_image
    normal = nodes.new('ShaderNodeNormalMap')
    normal.inputs['Strength'].default_value = .55
    links.new(tex.outputs['Color'], normal.inputs['Color'])
    links.new(normal.outputs['Normal'], shader.inputs['Normal'])
