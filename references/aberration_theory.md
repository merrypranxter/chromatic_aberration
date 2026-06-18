# Aberration Theory

Seidel (third-order) aberrations and their interaction with chromatic aberration.

---

## 1. Wavefront Aberration

Any real optical system produces a wavefront `W(ρ, θ)` that deviates from the ideal spherical reference.  The wavefront error is expanded as a polynomial in pupil coordinates `(ρ, θ)` and field angle `H`:

```
W(H, ρ, θ) = Σ Wₖₗₘ · Hᵏ · ρˡ · cos^m(θ)
```

The Seidel (third-order) terms dominate for paraxial-to-moderate apertures.

---

## 2. The Five Seidel Monochromatic Aberrations

### 2.1 Spherical Aberration (W040)

Rays at different aperture heights focus at different axial positions.  Rotationally symmetric.  Produces a circular blur regardless of field position.

- **Blur**: radially symmetric halo / filled disc
- **Interaction with CA**: spherochromatism — different colours have different amounts of spherical aberration

### 2.2 Coma (W131)

Off-axis point sources produce comet-shaped blur.  The tail always points away from the optical axis (positive coma) or toward it (negative coma).

- **Blur**: V-shaped / comet with 60° flare angle
- **Interaction with CA**: chromatic coma — each colour has its own coma figure; spectral tails appear

### 2.3 Astigmatism (W222)

At a given field point, the tangential and sagittal ray fans focus at different axial positions.

- **Blur**: lines at different orientations (tangential / sagittal) transitioning through an ellipse
- **Interaction with CA**: the tangential and sagittal fields shift differently for each colour

### 2.4 Field Curvature / Petzval Curvature (W220)

The sharpest image lies on a curved surface (the Petzval surface) rather than a flat plane.

```
1/R_P = -Σ φᵢ / nᵢ
```

- **Blur**: radial smear increasing toward field edge on a flat sensor
- **Interaction with CA**: different colours have different Petzval radii

### 2.5 Distortion (W311)

The magnification varies with field height.  No blur — just positional error.

- **Types**: barrel (negative), pincushion (positive)
- **Interaction with CA**: lateral CA is a colour-dependent distortion

---

## 3. Chromatic Aberrations

### 3.1 Axial (Longitudinal) Chromatic Aberration

Different colours focus at different axial positions.  Described by the **chromatic focal shift**:

```
δf = f / V
```

where `V` is the Abbe number of the lens.  A high-speed (low f-number) lens makes this visible on-axis.

**Wavefront coefficient**: `W020(λ)` — defocus that varies with wavelength.

### 3.2 Lateral (Transverse) Chromatic Aberration

At off-axis field positions the image height differs by colour.  Also called **chromatic difference of magnification**.

```
δy' = -y' / V  (for a thin singlet)
```

Lateral CA does not contribute to on-axis blur but causes colour fringing at the image edge.

**Wavefront coefficient**: `W111(λ)` — tilt that varies with wavelength.

### 3.3 Secondary Spectrum

Residual axial CA after achromatic doublet correction — the difference in focus between the corrected wavelengths (C, F) and the reference wavelength (d):

```
δf_secondary ≈ f · P_{g,F} / (V1 − V2)
```

Requires anomalous-dispersion glass to minimise.

### 3.4 Chromatic Difference of Spherical Aberration (Spherochromatism)

The spherical aberration coefficient `W040` varies with wavelength, causing a coloured halo in fast lenses.  Very noticeable in fast catadioptric (mirror-lens) systems.

---

## 4. Zernike Polynomial Representation

For wavefront sensing and adaptive optics the Seidel terms map to Zernike polynomials:

| Seidel term        | Primary Zernike(s)              |
|--------------------|---------------------------------|
| Defocus (W020)     | Z₄ (n=2, m=0)                  |
| Astigmatism (W222) | Z₃, Z₅ (n=2, m=±2)            |
| Coma (W131)        | Z₇, Z₈ (n=3, m=±1)            |
| Spherical (W040)   | Z₁₁ (n=4, m=0)                 |
| Trefoil (W333)     | Z₉, Z₁₀ (n=3, m=±3)           |

Chromatic aberration adds a wavelength index to each coefficient: `Zₖ(λ)`.

---

## 5. Interaction Matrix (Qualitative)

|                    | Axial CA | Lateral CA | Spherical | Coma | Astigmatism |
|--------------------|----------|------------|-----------|------|-------------|
| Fast aperture      | ↑↑       | —          | ↑↑        | ↑    | ↑           |
| Large field angle  | —        | ↑↑         | —         | ↑↑   | ↑↑          |
| Short focal length | ↑        | ↑↑         | ↑         | ↑↑   | ↑           |
| Refocus (zoom out) | ↑        | ↑          | —         | —    | —           |

---

## 6. Measuring Wavefront Error

- **Ronchi test**: fringes reveal wavefront shape
- **Shack-Hartmann sensor**: lenslet array → spot grid displacement → wavefront gradient
- **Interferometry (Fizeau, Twyman-Green)**: direct fringe pattern = wavefront map
- **PSF / MTF measurement**: indirect — deconvolve to infer wavefront

---

## References

- W. J. Smith, *Modern Optical Engineering*, 4th ed.
- R. Kingslake, *Lens Design Fundamentals*
- V. N. Mahajan, *Optical Imaging and Aberrations* (2 vols.)
- SPIE Field Guide to Optical Aberrations (FG21)
