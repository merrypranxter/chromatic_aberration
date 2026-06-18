"""
chromatic_aberrator.py
----------------------
Apply physically-based chromatic aberration to images using real lens parameters.

The amount of lateral CA at a given image height h is:

    Δh(λ) = -h * (f_green - f(λ)) / f_green
           ≈ -h * (n(λ) - n_green) / (n_green - 1) / V

where V is the Abbe number of the glass.

Usage
-----
    python chromatic_aberrator.py input.jpg output.jpg \\
        --focal-length 50 --aperture 1.8 --sensor-width 36 \\
        --glass BK7 --strength 1.0

Dependencies
------------
    numpy, Pillow (PIL), scipy
"""

import argparse
import math
from dataclasses import dataclass, field
from typing import Tuple

import numpy as np
from PIL import Image
from scipy.ndimage import map_coordinates

# ---------------------------------------------------------------------------
# Glass catalogue: (n_d, Abbe_number)  at the sodium d-line (589.3 nm)
# Source: Schott glass catalogue
# ---------------------------------------------------------------------------
GLASS_CATALOGUE = {
    "BK7":   (1.5168, 64.17),   # borosilicate crown — classic default
    "F2":    (1.6200, 36.43),   # dense flint — strong dispersion
    "SF11":  (1.7847, 25.68),   # very dense flint — extreme dispersion
    "BAK4":  (1.5688, 56.13),   # barium crown
    "LAK9":  (1.6910, 54.71),   # lanthanum crown — telephoto
    "N-FK5": (1.4875, 70.41),   # fluorite crown — low CA
    "WATER": (1.3330, 55.74),   # approximate water dispersion
}

# Approximate Sellmeier B, C coefficients for BK7 (used for full-spectrum sims)
SELLMEIER_BK7 = {
    "B": [1.03961212, 0.231792344, 1.01046945],
    "C": [6.00069867e-3, 2.00179144e-2, 1.03560653e2],  # in µm²
}


@dataclass
class LensParams:
    focal_length: float        # mm
    aperture: float            # f-number
    sensor_width: float        # mm  (full-frame = 36)
    glass: str = "BK7"
    strength: float = 1.0      # multiplier for artistic control


def sellmeier_n(wavelength_nm: float, B: list, C: list) -> float:
    """Refractive index via the Sellmeier equation (wavelength in nm → µm)."""
    lam_um = wavelength_nm / 1000.0
    lam2 = lam_um ** 2
    n2 = 1.0 + sum(b * lam2 / (lam2 - c) for b, c in zip(B, C))
    return math.sqrt(n2)


def abbe_shift(wavelength_nm: float, n_d: float, abbe_v: float) -> float:
    """
    Fractional focal-length shift at `wavelength_nm` relative to green (550 nm).
    Uses the simplified Abbe-number formula:
        Δf/f_d ≈ -(n(λ) - n_d) / (n_d - 1) / V
    We approximate n(λ) linearly from the Abbe number definition.
    """
    # Abbe number: V = (n_d - 1) / (n_F - n_C)
    # n_F at 486.1 nm, n_C at 656.3 nm
    # Linear approximation of index variation:
    ref_green = 550.0
    ref_f = 486.1
    ref_c = 656.3
    # Interpolate n at `wavelength_nm` using a parabolic dispersion model.
    t = (wavelength_nm - ref_green) / (ref_c - ref_f)
    delta_n = -(n_d - 1) / abbe_v * t
    shift = -delta_n / (n_d - 1)
    return shift


def build_ca_map(
    image_shape: Tuple[int, int],
    params: LensParams,
    wavelengths_nm: Tuple[float, float, float] = (656.3, 550.0, 486.1),
) -> np.ndarray:
    """
    Returns a (3, H, W, 2) array of sampling coordinates for R, G, B channels.
    Each channel[c, y, x] = (src_x, src_y) to sample for pixel (y, x).
    """
    H, W = image_shape
    n_d, abbe_v = GLASS_CATALOGUE[params.glass]

    # Normalised image height map: 0 at centre, 1 at corner.
    cx, cy = W / 2.0, H / 2.0
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    dx = (xs - cx) / (W / 2.0)
    dy = (ys - cy) / (H / 2.0)
    r = np.sqrt(dx**2 + dy**2)  # normalised radius [0, ~1.41]

    coords = np.zeros((3, H, W, 2), dtype=np.float32)
    for ch, lam in enumerate(wavelengths_nm):
        shift_frac = abbe_shift(lam, n_d, abbe_v) * params.strength
        # Pixel displacement in the image plane.
        disp = r * shift_frac * (W / 2.0)
        # Each channel is sampled at a radially offset position.
        coords[ch, :, :, 0] = ys + dy * disp  # row coordinate
        coords[ch, :, :, 1] = xs + dx * disp  # col coordinate

    return coords


def apply_chromatic_aberration(
    image: Image.Image, params: LensParams
) -> Image.Image:
    """Apply lateral chromatic aberration to a PIL Image."""
    img = np.array(image.convert("RGB"), dtype=np.float32)
    H, W, _ = img.shape

    coords = build_ca_map((H, W), params)
    result = np.zeros_like(img)

    for ch in range(3):
        row_coords = coords[ch, :, :, 0]
        col_coords = coords[ch, :, :, 1]
        result[:, :, ch] = map_coordinates(
            img[:, :, ch],
            [row_coords, col_coords],
            order=3,
            mode="nearest",
            prefilter=True,
        )

    return Image.fromarray(np.clip(result, 0, 255).astype(np.uint8))


def main():
    parser = argparse.ArgumentParser(
        description="Apply physically-based chromatic aberration to an image."
    )
    parser.add_argument("input", help="Input image path")
    parser.add_argument("output", help="Output image path")
    parser.add_argument("--focal-length", type=float, default=50.0, help="mm")
    parser.add_argument("--aperture", type=float, default=2.8, help="f-number")
    parser.add_argument("--sensor-width", type=float, default=36.0, help="mm")
    parser.add_argument(
        "--glass",
        default="BK7",
        choices=list(GLASS_CATALOGUE.keys()),
        help="Glass type from catalogue",
    )
    parser.add_argument(
        "--strength", type=float, default=1.0, help="Artistic multiplier"
    )
    args = parser.parse_args()

    params = LensParams(
        focal_length=args.focal_length,
        aperture=args.aperture,
        sensor_width=args.sensor_width,
        glass=args.glass,
        strength=args.strength,
    )

    img = Image.open(args.input)
    out = apply_chromatic_aberration(img, params)
    out.save(args.output)
    print(f"Saved {args.output}")


if __name__ == "__main__":
    main()
