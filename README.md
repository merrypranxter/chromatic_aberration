# chromatic_aberration

A repository exploring the optical phenomenon where a lens fails to focus all colors to the same point, creating colored fringes at high-contrast edges. This is not a "filter" — it's a physical simulation of how glass bends light differently at different wavelengths. The goal is to make chromatic aberration feel like a window into another dimension, not a cheap Instagram effect.

## The Aesthetic

- **Longitudinal CA**: Red, green, and blue focus at different depths, creating soft color fringes in bokeh
- **Lateral/transverse CA**: RGB channels are shifted radially from the center, strongest at the edges
- **Purple fringing**: The extreme violet/blue aberration at high-contrast boundaries (tree branches against sky)
- **Axial color shift**: Objects that change color as they move in/out of focus because different wavelengths focus at different planes
- **Double image fringe**: The "ghost" image that appears offset from the main image, tinted
- **Coma aberration**: Comet-shaped stars off-axis, often combined with chromatic aberration

## Core Concepts

- **Dispersion**: The refractive index of glass varies with wavelength. Crown glass and flint glass have different dispersion curves, which is why achromatic doublet lenses exist.
- **Abbe number**: A measure of a material's dispersion. Lower Abbe number = more chromatic aberration. This is the mathematical heart of the effect.
- **Focal length dependence**: The focal length of a simple lens is `f = R/(n-1)`, where `n` varies with wavelength. So `f_red ≠ f_green ≠ f_blue`.
- **Seidel aberrations**: The five monochromatic aberrations (spherical, coma, astigmatism, field curvature, distortion) that interact with chromatic aberration in real lenses.
- **Apochromatic correction**: Triplets or special glasses that correct three wavelengths simultaneously. The *failure* of apochromatic correction is where interesting residual color appears.

## Repository Structure

```
├── shaders/
│   ├── lateral_chromatic_shift.frag       # Radial RGB channel separation
│   ├── longitudinal_ca_bokeh.frag         # Depth-dependent color fringing in out-of-focus areas
│   ├── purple_fringe.frag                 # High-contrast edge violet/blue bloom
│   ├── axial_color_shift.frag             # Color changes as objects move through focus plane
│   ├── double_ghost_fringe.frag           # Offset ghost image with color tint
│   ├── coma_stars.frag                    # Comet-shaped point sources with chromatic tail
│   └── lens_spectrum_decomposition.frag   # Decompose image into spectral bands and recombine
├── notebooks/
│   ├── dispersion_calculator.ipynb        # Calculate dispersion from Abbe number and refractive index
│   ├── lens_aberration_simulator.ipynb    # Simulate a simple lens with chromatic aberration
│   └── spectral_decomposition.ipynb       # Decompose an image into wavelength bands
├── tools/
│   ├── chromatic_aberrator.py             # Apply physical CA to images based on lens parameters
│   ├── lens_profile_generator.py          # Generate CA profiles for specific lens designs
│   └── bokeh_chroma_mapper.py             # Map chromatic aberration to bokeh shape
├── references/
│   ├── lens_design.md                     # Basic lens design: simple lens, doublet, triplet, aspheric
│   ├── dispersion_curves.md               # Glass dispersion curves (Schott, Ohara, Hoya catalogs)
│   ├── aberration_theory.md               # Seidel aberrations and wavefront error
│   └── camera_lens_profiles.md            # Real lens profiles with measured CA characteristics
├── gallery/
│   └── (output renders)
└── README.md
```

## Design Prompts

- **"Create a shader that simulates looking through a cheap wide-angle lens at night. The city lights at the edges have red and blue fringes, the stars are comet-shaped, and the center is sharp but the edges are a rainbow blur. Make it feel like a dream, not a defect."**
- **"Design a chromatic aberration shader where the color separation is determined by the *depth* of the scene. Far objects have strong purple fringing, near objects have green/yellow fringing. The effect should feel like the world is layered by color."**
- **"Build a 'lens made of water' shader where the chromatic aberration is extreme — like looking through a droplet. The dispersion should follow the actual refractive index of water (n=1.33), and the caustics should be colored."**

## Color Palette

| Name                | Hex       | Description                                          |
|---------------------|-----------|------------------------------------------------------|
| Lens flare gold     | `#FFD700` | The warm color of axial chromatic aberration in the center |
| Edge fringe red     | `#FF0033` | The red separation at the edges                      |
| Edge fringe blue    | `#0066FF` | The blue separation at the edges                     |
| Purple fringe       | `#9933FF` | The high-contrast edge violet bloom                  |
| Apochromatic gray   | `#808080` | The neutral center where all wavelengths converge    |

## References

- Warren J. Smith, *Modern Optical Engineering* (lens design bible)
- Schott glass catalog (dispersion curves for real optical glasses)
- Camera lens reviews (DXOMark, LensRentals) for measured CA data
- Seidel aberration theory and wavefront optics
- *Optical System Design* by Fischer & Tadic-Galeb

## Mood

The world is slightly broken, and the break is beautiful. Every edge has a secret color. The lens is a prism, and the image is a rainbow that forgot to separate. The defect is the art.
