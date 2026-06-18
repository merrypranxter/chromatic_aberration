"""
lens_profile_generator.py
--------------------------
Generate a radial chromatic aberration profile for a specific lens design.

Input : lens prescription — a sequence of surfaces described by radius of
        curvature, thickness, and glass material (or AIR).
Output: a radial CA map as a NumPy array and optional PNG export.

The radial CA map gives the lateral colour fringe width in pixels at each
image-height fraction [0, 1], for a given sensor / image-circle size.

Usage
-----
    python lens_profile_generator.py \\
        --prescription doublet_achromat.json \\
        --image-circle 43.3 \\
        --sensor-pixels 6000 \\
        --output ca_profile.npy \\
        --plot

Prescription JSON format
------------------------
[
    {"radius": 61.47, "thickness": 6.0,  "glass": "BK7"},
    {"radius": -44.64, "thickness": 2.5, "glass": "F2"},
    {"radius": -129.94,"thickness": 97.0,"glass": "AIR"}
]
"""

import argparse
import json
import math
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np

# Reuse glass catalogue from chromatic_aberrator
GLASS_CATALOGUE = {
    "AIR":   (1.0000, 1e9),
    "BK7":   (1.5168, 64.17),
    "F2":    (1.6200, 36.43),
    "SF11":  (1.7847, 25.68),
    "BAK4":  (1.5688, 56.13),
    "LAK9":  (1.6910, 54.71),
    "N-FK5": (1.4875, 70.41),
    "WATER": (1.3330, 55.74),
}

WAVELENGTHS_NM = {
    "C": 656.3,   # red hydrogen line
    "d": 589.3,   # sodium d (reference)
    "e": 546.1,   # mercury e
    "F": 486.1,   # blue hydrogen line
    "g": 435.8,   # mercury g (violet)
}

# -----------------------------------------------------------------------------
# Dispersion model
# -----------------------------------------------------------------------------

def _n_linear(glass: str, wavelength_nm: float) -> float:
    """
    Simple linear interpolation of refractive index between C and F lines
    using the Abbe number.  Accurate enough for paraxial analysis.
    """
    n_d, V = GLASS_CATALOGUE[glass]
    if glass == "AIR":
        return 1.0
    # n_F - n_C = (n_d - 1) / V
    delta_n_FC = (n_d - 1.0) / V
    # n at d-line is 589.3 nm; interpolate linearly vs 1/λ²
    # Use Hartmann approximation: n(λ) ≈ n_d + C_H / (λ - λ_0)
    # For our purposes a linear interpolation in wavelength is sufficient.
    lam_C, lam_F = WAVELENGTHS_NM["C"], WAVELENGTHS_NM["F"]
    t = (wavelength_nm - lam_C) / (lam_F - lam_C)  # 0=C, 1=F
    return n_d + delta_n_FC * (t - 0.5)  # n_d lies midway by definition


# -----------------------------------------------------------------------------
# Paraxial ray trace
# -----------------------------------------------------------------------------

Surface = Tuple[float, float, str]  # (radius, thickness_after, glass)


def paraxial_trace(
    surfaces: List[Surface],
    wavelength_nm: float,
    h0: float = 1.0,
    u0: float = 0.0,
) -> float:
    """
    Trace a paraxial marginal ray through a sequence of surfaces.
    Returns the back focal distance (BFD) from the last surface.

    surfaces : list of (R, t, glass_after)
               R = radius of curvature (+ve = centre to the right)
               t = thickness to next surface (in mm)
               glass_after = material after this surface
    h0       : initial ray height (mm)
    u0       : initial ray angle (radians), 0 for paraxial marginal ray
    """
    h = h0
    u = u0
    n_prev = 1.0  # starts in air

    for R, t, glass in surfaces:
        n_next = _n_linear(glass, wavelength_nm)
        # Refraction: n'u' = nu - h * (n' - n) / R
        if abs(R) > 1e10:  # flat surface
            u_new = u * n_prev / n_next
        else:
            u_new = (n_prev * u - h * (n_next - n_prev) / R) / n_next
        h = h + t * u_new
        u = u_new
        n_prev = n_next

    # Back focal distance from exit pupil (last surface location)
    if abs(u) < 1e-12:
        return float("inf")
    return -h / u


def focal_length_from_surfaces(surfaces: List[Surface], wavelength_nm: float) -> float:
    """Return the effective focal length (EFL) via paraxial marginal ray trace."""
    bfd = paraxial_trace(surfaces, wavelength_nm)
    # For a system in air we need to find the rear principal plane position.
    # Quick approximation: trace with h0=1, u0=0 → f ≈ BFD when input is collimated.
    return bfd


# -----------------------------------------------------------------------------
# CA profile generation
# -----------------------------------------------------------------------------

def generate_ca_profile(
    surfaces: List[Surface],
    image_circle_mm: float = 43.3,
    sensor_pixels: int = 6000,
    num_heights: int = 100,
) -> np.ndarray:
    """
    Generate a radial CA profile.

    Returns an array of shape (num_heights, 3) where columns are:
        [normalised_height, lateral_CA_px (R-G), lateral_CA_px (B-G)]
    """
    heights = np.linspace(0.0, 1.0, num_heights)
    px_per_mm = sensor_pixels / image_circle_mm

    f_r = focal_length_from_surfaces(surfaces, WAVELENGTHS_NM["C"])
    f_g = focal_length_from_surfaces(surfaces, WAVELENGTHS_NM["e"])
    f_b = focal_length_from_surfaces(surfaces, WAVELENGTHS_NM["F"])

    profile = np.zeros((num_heights, 3))
    profile[:, 0] = heights

    for i, h in enumerate(heights):
        h_mm = h * (image_circle_mm / 2.0)
        # Lateral CA = h * (f_ref - f(λ)) / f_ref
        ca_r = h_mm * (f_g - f_r) / f_g * px_per_mm
        ca_b = h_mm * (f_g - f_b) / f_g * px_per_mm
        profile[i, 1] = ca_r
        profile[i, 2] = ca_b

    return profile


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Generate a radial CA profile from a lens prescription."
    )
    parser.add_argument(
        "--prescription",
        required=True,
        help="Path to lens prescription JSON file",
    )
    parser.add_argument(
        "--image-circle", type=float, default=43.3, help="Image circle diameter mm"
    )
    parser.add_argument(
        "--sensor-pixels", type=int, default=6000, help="Sensor width in pixels"
    )
    parser.add_argument("--output", default="ca_profile.npy", help="Output .npy file")
    parser.add_argument("--plot", action="store_true", help="Show a matplotlib plot")
    args = parser.parse_args()

    with open(args.prescription) as f:
        data = json.load(f)

    surfaces = [(s["radius"], s["thickness"], s["glass"]) for s in data]
    profile = generate_ca_profile(
        surfaces,
        image_circle_mm=args.image_circle,
        sensor_pixels=args.sensor_pixels,
    )

    np.save(args.output, profile)
    print(f"CA profile saved to {args.output}")
    print(f"  Peak R-G CA: {profile[-1, 1]:.3f} px")
    print(f"  Peak B-G CA: {profile[-1, 2]:.3f} px")

    if args.plot:
        import matplotlib.pyplot as plt

        h = profile[:, 0]
        plt.figure(figsize=(8, 4))
        plt.plot(h, profile[:, 1], "r-", label="R-G lateral CA (px)")
        plt.plot(h, profile[:, 2], "b-", label="B-G lateral CA (px)")
        plt.xlabel("Normalised image height")
        plt.ylabel("Lateral CA (pixels)")
        plt.title("Radial chromatic aberration profile")
        plt.legend()
        plt.grid(True, alpha=0.4)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    main()
