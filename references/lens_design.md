# Lens Design Reference

A concise guide to the optical designs that produce (and correct) chromatic aberration.

---

## 1. The Simple Thin Lens

The lensmaker's equation relates focal length `f` to the surface radii and refractive index:

```
1/f = (n - 1) * (1/R1 - 1/R2)
```

Because `n` varies with wavelength (dispersion), so does `f`.  This is the root cause of all chromatic aberration.

For a crown-glass singlet (BK7, V ≈ 64):

| Wavelength | n       | Δf/f_d   |
|------------|---------|----------|
| 656 nm (C) | 1.5143  | +0.039 % |
| 589 nm (d) | 1.5168  | 0        |
| 486 nm (F) | 1.5224  | −0.087 % |

The difference `f_C − f_F` is the **primary chromatic aberration** (longitudinal).

---

## 2. The Achromatic Doublet

Two elements cemented or air-spaced: a positive crown element and a negative flint element.  The condition for achromatism is:

```
φ1/V1 + φ2/V2 = 0
```

where `φ = 1/f` is the power of each element and `V` is the Abbe number.

**Result**: `f_C = f_F` (red and blue focus at the same plane), while the green wavelength focuses slightly differently — the **secondary spectrum**.

Typical doublet: BK7 + F2 (`V = 64` and `V = 36`).  Residual secondary spectrum ≈ `f / (V1 − V2)`.

---

## 3. The Apochromatic Triplet

Corrects three wavelengths (usually C, d, F) by using a third element or a special glass with anomalous partial dispersion (e.g., fluorite CaF₂, Schott N-FK5, Ohara FPL-53).

The partial dispersion ratio `P_{g,F} = (n_g − n_F) / (n_F − n_C)` deviates from the "normal line" in the glass map for ED and fluorite glasses, allowing residual spectrum correction.

**Telescope/apo designs**: Petzval doublet + field-flattener, Zeiss APQ triplet, Leica APO-Summicron.

---

## 4. Aspheric Elements

Aspheric surfaces (described by conic constant `k` and higher-order polynomial terms) correct **monochromatic** aberrations (spherical, coma) without adding elements, leaving room in the glass budget for chromatic correction.  They do **not** directly reduce chromatic aberration but reduce interactions between CA and spherical aberration.

---

## 5. Floating Elements and Internal Focusing

Modern telephoto and macro lenses use internal focusing — moving an internal group rather than the front element — to keep the entrance pupil position stable.  This is important because lateral CA changes with focusing distance in many designs.

---

## 6. ED and Fluorite Glass

| Glass       | n_d    | V     | P_{g,F} deviation |
|-------------|--------|-------|-------------------|
| BK7 (crown) | 1.5168 | 64.2  | normal            |
| F2 (flint)  | 1.6200 | 36.4  | normal            |
| N-FK5 (ED)  | 1.4875 | 70.4  | +0.008            |
| N-PK52A     | 1.4970 | 81.6  | +0.013            |
| CaF₂        | 1.4338 | 95.1  | +0.018            |

Anomalous partial dispersion (positive deviation) allows apochromatic correction.

---

## 7. The Telephoto Effect and CA

Long telephoto lenses have **smaller** relative CA (lateral CA is proportional to `h/f`, so a longer focal length at the same image size has lower CA) but are more sensitive to secondary spectrum.  This is why apo telephoto lenses use fluorite or ED elements.

Wide-angle lenses have **larger** relative lateral CA at the edges of the frame because the image height `h` is large relative to the short focal length.

---

## 8. Summary of Residual CA by Design Type

| Design        | Longitudinal CA | Lateral CA at edge | Secondary spectrum |
|---------------|-----------------|--------------------|--------------------|
| Singlet       | Large           | Large              | N/A                |
| Doublet       | Corrected       | Moderate           | Present            |
| Apochromat    | Corrected       | Corrected          | Minimised          |
| Superachromat | Corrected       | Corrected          | Near zero          |
