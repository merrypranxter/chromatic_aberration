# Camera Lens Profiles — Measured Chromatic Aberration

Real-world CA data from published lens tests (DXOMark, Imatest, LensRentals, lenstip.com).
Values are typical lateral CA at the extreme edge of the image circle for full-frame sensors
unless otherwise noted.

---

## 1. How to Read These Profiles

**Lateral CA** is reported as the maximum colour fringe width in pixels at the image edge,
measured on a sensor with approximately 24 MP full-frame resolution (~6000 × 4000 px).

| CA (px) | Assessment                |
|---------|---------------------------|
| 0–0.5   | Excellent; invisible      |
| 0.5–1   | Very good; barely visible |
| 1–2     | Good; visible at 100 %    |
| 2–4     | Moderate; noticeable      |
| 4–8     | Poor; strong fringing     |
| > 8     | Very poor; severe fringes |

**Longitudinal CA** is reported as the worst-case colour separation in the out-of-focus
region, typically at the widest aperture, in pixels of blur difference between R and B.

---

## 2. Wide-Angle Primes

### Canon EF 24mm f/1.4L II USM
- **Lateral CA at edge**: ~2.5 px at f/1.4, corrects to ~1.2 px at f/5.6
- **Longitudinal CA**: strong at f/1.4 (red/blue bokeh fringe ~4 px), diminishes by f/4
- **Purple fringing**: moderate; visible on high-contrast edges wide open
- **Notes**: Wide-angle + fast aperture = challenging design; field curvature aggravates CA

### Sigma 14mm f/1.8 DG HSM Art
- **Lateral CA at edge**: ~3.0 px (extreme wide angle)
- **Longitudinal CA**: moderate; corrected to ~1.5 px by f/4
- **Notes**: Best-in-class for ultra-wide; Sigma's FLD glass reduces secondary spectrum

### Zeiss Milvus 21mm f/2.8
- **Lateral CA at edge**: ~0.8 px (exceptional for 21mm)
- **Longitudinal CA**: very low; well-corrected wide open
- **Notes**: T* coating reduces flare; internal floating group corrects field-angle CA

---

## 3. Standard Primes

### Nikon AF-S 50mm f/1.4G
- **Lateral CA at edge**: ~1.0 px at f/1.4, < 0.5 px at f/5.6
- **Longitudinal CA**: visible at f/1.4 (~3 px red/blue bokeh shift), negligible by f/2.8
- **Purple fringing**: noticeable on specular highlights wide open
- **Notes**: Classic design; axial CA is the main defect at wide aperture

### Sigma 50mm f/1.4 DG DN Art
- **Lateral CA at edge**: < 0.5 px across all apertures (exceptional)
- **Longitudinal CA**: very low for a fast 50mm; ~1.5 px at f/1.4
- **Notes**: 17-element design with three SLD elements; one of the best-corrected 50mms

### Leica APO-Summicron-M 50mm f/2 ASPH
- **Lateral CA at edge**: < 0.3 px (near-perfect)
- **Longitudinal CA**: effectively zero; truly apochromatic
- **Notes**: Apochromatic design; corrects three wavelengths; reference standard for CA

---

## 4. Short Telephoto / Portraits

### Canon EF 85mm f/1.4L IS USM
- **Lateral CA at edge**: ~0.8 px wide open
- **Longitudinal CA**: moderate; strong bokeh colour fringe at f/1.4 (~3.5 px)
- **Notes**: UA lens element; good overall correction but longitudinal CA is artistic feature

### Sony FE 85mm f/1.4 GM
- **Lateral CA at edge**: ~0.6 px
- **Longitudinal CA**: ~2.5 px at f/1.4; well-controlled for f/1.4 design
- **Purple fringing**: minimal

---

## 5. Telephoto Primes

### Nikon AF-S 300mm f/4E PF ED VR
- **Lateral CA at edge**: < 0.5 px
- **Longitudinal CA**: very low; ED element provides near-APO performance
- **Notes**: Phase Fresnel element corrects CA and chromatic spherical aberration

### Canon EF 400mm f/2.8L IS III USM
- **Lateral CA at edge**: ~0.3 px (excellent for aperture)
- **Longitudinal CA**: low; fluorite elements dominate the design
- **Notes**: Two fluorite elements; flagship "white" telephoto standard

### Sigma 150-600mm f/5-6.3 DG OS HSM Sport (at 600mm)
- **Lateral CA at edge**: ~1.5 px at 600mm
- **Longitudinal CA**: minimal (small aperture limits longitudinal CA)
- **Notes**: Three FLD elements; good for zoom range

---

## 6. Zoom Lenses

### Canon EF 24-70mm f/2.8L II USM (at 24mm)
- **Lateral CA at edge**: ~1.8 px at 24mm, decreasing to ~0.8 px at 70mm
- **Longitudinal CA**: significant at 24mm f/2.8 (~3 px); better at longer focal lengths
- **Notes**: Zoom mechanism introduces variable CA; worst at widest focal length

### Tamron SP 70-200mm f/2.8 Di VC USD G2 (at 70mm)
- **Lateral CA at edge**: ~1.2 px at 70mm
- **Longitudinal CA**: ~2.5 px at 70mm f/2.8; improves toward 200mm
- **Notes**: XLD and LD elements; competitive with Canon/Nikon at lower price

---

## 7. Fisheye and Ultra-Wide

### Sigma 8mm f/3.5 EX DG Circular Fisheye
- **Lateral CA at edge**: ~4–5 px (expected for extreme wide angle)
- **Longitudinal CA**: moderate
- **Notes**: Extreme field angle makes lateral CA unavoidable; characteristic of the genre

### Canon EF 8-15mm f/4L Fisheye USM (at 8mm)
- **Lateral CA at edge**: ~3.5 px
- **Notes**: UD element and floating system; best fisheye CA correction available

---

## 8. CA Correction in Post-Processing

Modern cameras and raw converters apply **lens profile corrections** that remove most lateral CA:

- **Lightroom / ACR**: "Remove Chromatic Aberration" checkbox + lens profile
- **Capture One**: automatic CA correction per lens profile
- **Darktable**: lens correction module (lensfun database)

These corrections work by computing the inverse of the measured CA polynomial and remapping
each colour channel.  **Residual CA** (after correction) is typically < 0.3 px for well-profiled lenses.

For **simulation** purposes the uncorrected values above represent the "raw" lens signature.

---

## References

- DXOMark Lens Metrology Reports, dxomark.com
- LensRentals Roger Cicala blog posts (lensrentals.com/blog)
- lenstip.com objective lens tests
- Imatest Pro chromatic aberration measurement documentation
