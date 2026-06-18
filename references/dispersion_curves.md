# Glass Dispersion Curves

How the refractive index varies with wavelength — the physical foundation of chromatic aberration.

---

## 1. The Sellmeier Equation

The most accurate standard dispersion formula for optical glass:

```
n²(λ) = 1 + Σ Bᵢλ² / (λ² − Cᵢ)
```

where `λ` is in **micrometres**, and `Bᵢ`, `Cᵢ` are glass-specific constants from the manufacturer's catalogue.

**BK7 Sellmeier coefficients** (Schott):

| i | Bᵢ          | Cᵢ (µm²)    |
|---|-------------|-------------|
| 1 | 1.03961212  | 0.00600069  |
| 2 | 0.23179234  | 0.02001791  |
| 3 | 1.01046945  | 103.560653  |

---

## 2. The Abbe Number

```
V = (n_d − 1) / (n_F − n_C)
```

| Reference line | Wavelength | Element  |
|----------------|------------|----------|
| C              | 656.3 nm   | Hydrogen |
| D              | 589.3 nm   | Sodium   |
| d              | 587.6 nm   | Helium   |
| e              | 546.1 nm   | Mercury  |
| F              | 486.1 nm   | Hydrogen |
| g              | 435.8 nm   | Mercury  |

**Interpretation**: Higher `V` = less dispersion.  Crown glasses: V ≈ 50–80.  Flint glasses: V ≈ 25–50.

---

## 3. Schott Glass Map

Key glasses plotted on the (n_d, V) diagram:

```
                 V  →  (decreasing)
 n_d ↑
 1.90 |              SF57
      |          SF11   SF5
 1.70 |       F2   LaF2
      |    BAK4  LaK9
 1.55 |  SSK5  BK7
      |       FK5
 1.45 |                N-FK5  CaF₂
      +---+---+---+---+---+---+-→
         25  35  45  55  65  75  85  95
```

Glasses in the upper-right (high n, low V) are dense flints — maximum dispersion.
Glasses in the lower-left (low n, high V) are fluorite crowns — minimum dispersion.

---

## 4. Notable Glasses for Chromatic Aberration Simulation

### Crown Glasses (low dispersion)

| Name      | n_d    | V     | Notes                                    |
|-----------|--------|-------|------------------------------------------|
| N-BK7     | 1.5168 | 64.17 | The most common optical glass            |
| N-K5      | 1.5220 | 59.48 | Slightly more dispersive than BK7        |
| N-BAK4    | 1.5688 | 56.13 | Barium crown; used in prism binoculars   |
| N-FK5     | 1.4875 | 70.41 | Fluorophosphate crown; low CA            |
| N-PK52A   | 1.4970 | 81.61 | Very low CA; used in APO lenses          |

### Flint Glasses (high dispersion)

| Name      | n_d    | V     | Notes                                    |
|-----------|--------|-------|------------------------------------------|
| N-F2      | 1.6200 | 36.43 | Classic doublet flint element            |
| N-SF5     | 1.6727 | 32.21 | Dense flint                              |
| N-SF11    | 1.7847 | 25.68 | Very dense flint; maximum CA             |
| N-SF57    | 1.8467 | 23.83 | Extreme flint; used in artistic prisms   |

---

## 5. Partial Dispersion and the Normal Line

The partial dispersion ratio `P_{g,F}` measures the shape of the dispersion curve beyond the C-F interval:

```
P_{g,F} = (n_g − n_F) / (n_F − n_C)
```

Most glasses fall on the "normal line":  `P_{g,F} ≈ 0.6438 − 0.001682 · V`

**Anomalous dispersion** glasses deviate from this line:

| Glass   | ΔP_{g,F} | Type                         |
|---------|-----------|------------------------------|
| N-PK52A | +0.013    | Anomalous crown (low n, high V) |
| CaF₂    | +0.018    | Fluorite (natural crystal)   |
| N-SF6   | −0.006    | Anomalous flint              |

Anomalous glasses are required to build **apochromatic** (three-wavelength corrected) lenses.

---

## 6. Ohara and Hoya Equivalents

| Schott  | Ohara    | Hoya     | n_d    | V     |
|---------|----------|----------|--------|-------|
| N-BK7   | S-BSL7   | BSC7     | 1.5168 | 64.17 |
| N-F2    | S-TIM2   | FF5      | 1.6200 | 36.43 |
| N-SF11  | S-TIH11  | FD11     | 1.7847 | 25.68 |
| N-PK52A | S-FPL53  | FCD10    | 1.4970 | 81.61 |
| CaF₂    | —        | —        | 1.4338 | 95.10 |

---

## 7. Dispersion of Common Transparent Materials

| Material      | n_d    | V     | Use in imaging      |
|---------------|--------|-------|---------------------|
| Air           | 1.0003 | ∞     | Reference medium    |
| Water         | 1.3330 | 55.7  | Underwater housings |
| Acrylic (PMMA)| 1.4917 | 57.4  | Cheap optics        |
| Polycarbonate | 1.5855 | 30.0  | High CA plastic     |
| Fused silica  | 1.4585 | 67.8  | UV/IR transparent   |
| CaF₂          | 1.4338 | 95.1  | Maximum correction  |

---

## References

- Schott AG, *Optical Glass Data Sheets* (current edition), schott.com
- Ohara Inc., *Optical Glass Catalog*, ohara-inc.co.jp
- W. J. Smith, *Modern Optical Engineering*, 4th ed., McGraw-Hill, 2008
- ISO 10110 glass notation standard
