"""
bokeh_chroma_mapper.py
----------------------
Generate a chromatically-aberrated bokeh kernel for a given lens profile.

In a real lens with chromatic aberration the out-of-focus circles (bokeh
discs) are NOT white — they carry colour fringes because each wavelength has
a slightly different circle-of-confusion (CoC) radius. This tool:

  1. Reads (or synthesises) a lens CA profile.
  2. Generates a per-channel disc kernel for a specified defocus level.
  3. Exports the kernel as a small PNG (one RGB tile) suitable for use as a
     convolution kernel in a bokeh post-processing shader.

Usage
-----
    python bokeh_chroma_mapper.py \\
        --ca-profile ca_profile.npy \\
        --coc-green 32 \\
        --defocus 1.0 \\
        --output bokeh_kernel.png \\
        --show

If --ca-profile is omitted, a BK7 lens profile is synthesised internally.
"""

import argparse
import math
from pathlib import Path
from typing import Optional, Tuple

import numpy as np
from PIL import Image

# Default CA ratios for a BK7 singlet (normalised to green = 1.0).
# Red CoC is larger (focuses behind), blue CoC is smaller (focuses in front).
DEFAULT_COC_RATIOS = {
    "R": 1.22,   # red CoC is ~22 % larger than green
    "G": 1.00,
    "B": 0.82,   # blue CoC is ~18 % smaller than green
}


def make_disc_kernel(radius: float, size: int) -> np.ndarray:
    """Create a normalised circular disc kernel of given radius in a (size×size) array."""
    k = np.zeros((size, size), dtype=np.float32)
    cx, cy = size // 2, size // 2
    y, x = np.ogrid[:size, :size]
    mask = (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2
    k[mask] = 1.0
    total = k.sum()
    if total > 0:
        k /= total
    return k


def load_coc_ratios(ca_profile_path: Optional[str], defocus: float) -> Tuple[float, float, float]:
    """
    Derive per-channel CoC ratios from a saved CA profile.
    defocus is a value in [0, 1] representing the fraction of maximum defocus.
    Returns (r_ratio, g_ratio, b_ratio).
    """
    if ca_profile_path is None:
        d = defocus
        r = 1.0 + (DEFAULT_COC_RATIOS["R"] - 1.0) * d
        b = 1.0 + (DEFAULT_COC_RATIOS["B"] - 1.0) * d
        return r, 1.0, b

    profile = np.load(ca_profile_path)  # shape (N, 3): [h, ca_r, ca_b]
    # Use the peak (edge) CA value to derive the ratio at max height.
    ca_r_px = abs(profile[-1, 1]) * defocus
    ca_b_px = abs(profile[-1, 2]) * defocus
    # Convert pixel shift to a CoC ratio (approximate).
    base_coc = 20.0  # assumed green CoC at this defocus in pixels
    r_ratio = 1.0 + ca_r_px / base_coc
    b_ratio = max(0.5, 1.0 - ca_b_px / base_coc)
    return r_ratio, 1.0, b_ratio


def build_bokeh_kernel(
    coc_green_px: int,
    r_ratio: float,
    g_ratio: float,
    b_ratio: float,
    aperture_shape: str = "circle",
) -> np.ndarray:
    """
    Build an RGB bokeh kernel.

    Returns a float32 array of shape (H, W, 3).
    """
    r_coc = coc_green_px * r_ratio
    g_coc = coc_green_px * g_ratio
    b_coc = coc_green_px * b_ratio

    # Kernel must be large enough to contain the biggest disc.
    max_r = math.ceil(max(r_coc, g_coc, b_coc))
    size = 2 * max_r + 3  # odd for symmetry

    kr = make_disc_kernel(r_coc, size)
    kg = make_disc_kernel(g_coc, size)
    kb = make_disc_kernel(b_coc, size)

    # Stack into RGB.
    kernel = np.stack([kr, kg, kb], axis=-1)
    return kernel


def kernel_to_image(kernel: np.ndarray) -> Image.Image:
    """Convert a float32 (H, W, 3) kernel to a displayable PIL Image."""
    # Normalise each channel to [0, 255] independently for visualisation.
    out = np.zeros_like(kernel, dtype=np.uint8)
    for c in range(3):
        ch = kernel[:, :, c]
        if ch.max() > 0:
            ch_norm = ch / ch.max() * 255.0
            out[:, :, c] = np.clip(ch_norm, 0, 255).astype(np.uint8)
    return Image.fromarray(out, mode="RGB")


def main():
    parser = argparse.ArgumentParser(
        description="Generate a chromatically-aberrated bokeh kernel."
    )
    parser.add_argument(
        "--ca-profile", default=None, help="Path to .npy CA profile (optional)"
    )
    parser.add_argument(
        "--coc-green",
        type=int,
        default=32,
        help="Green channel CoC radius in pixels (controls bokeh size)",
    )
    parser.add_argument(
        "--defocus",
        type=float,
        default=1.0,
        help="Defocus level [0, 1]; 1 = maximum CA from profile",
    )
    parser.add_argument(
        "--output", default="bokeh_kernel.png", help="Output PNG filename"
    )
    parser.add_argument("--show", action="store_true", help="Display the kernel")
    args = parser.parse_args()

    r_ratio, g_ratio, b_ratio = load_coc_ratios(args.ca_profile, args.defocus)

    kernel = build_bokeh_kernel(
        coc_green_px=args.coc_green,
        r_ratio=r_ratio,
        g_ratio=g_ratio,
        b_ratio=b_ratio,
    )

    img = kernel_to_image(kernel)
    img.save(args.output)
    print(f"Bokeh kernel saved to {args.output}  ({img.width}×{img.height} px)")
    print(f"  CoC radii — R: {args.coc_green * r_ratio:.1f}  "
          f"G: {args.coc_green * g_ratio:.1f}  B: {args.coc_green * b_ratio:.1f}  (px)")

    if args.show:
        img.show()


if __name__ == "__main__":
    main()
