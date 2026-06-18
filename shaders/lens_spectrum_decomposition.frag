// lens_spectrum_decomposition.frag
// Physically-inspired spectral decomposition and recomposition.
//
// Instead of simply shifting three RGB channels, this shader decomposes the
// image into N spectral bands (approximating a continuous spectrum using CIE
// colour matching functions), shifts each band by an amount proportional to
// the dispersion of glass at that wavelength, then recombines them into sRGB.
// The result is more nuanced than simple RGB shifting: intermediate colours
// (cyan, yellow) appear at the fringe boundaries.
//
// Spectral bands sampled (7 bands, 400–700 nm in 50 nm steps):
//   400 nm (violet), 450 nm (blue), 500 nm (cyan), 550 nm (green),
//   600 nm (yellow), 650 nm (orange), 700 nm (red)
//
// Uniforms:
//   u_texture       — source image
//   u_center        — optical axis UV (default vec2(0.5))
//   u_dispersion    — overall dispersion strength, e.g. 0.008
//   u_abbe          — simulated Abbe number (low = more dispersion, e.g. 30.0)
//                     Higher Abbe number = less CA (e.g. 60 for crown glass).

precision highp float;

uniform sampler2D u_texture;
uniform vec2      u_center;
uniform float     u_dispersion;
uniform float     u_abbe;

varying vec2 v_uv;

// Cauchy dispersion approximation: n(λ) ≈ A + B/λ² normalised so n(550nm)=0.
// Returns relative shift coefficient for wavelength `lambda_nm`.
float cauchy_shift(float lambda_nm) {
    float L = lambda_nm / 550.0; // normalised to green
    // Relative deviation from green focal length.
    return (1.0 / (L * L) - 1.0) / u_abbe;
}

// CIE colour matching functions (simplified 3-lobe Gaussians).
// Returns an RGB weight for a given wavelength.
vec3 cie_cmf(float lambda_nm) {
    float r = exp(-0.5 * pow((lambda_nm - 610.0) / 60.0, 2.0));
    float g = exp(-0.5 * pow((lambda_nm - 545.0) / 45.0, 2.0));
    float b = exp(-0.5 * pow((lambda_nm - 450.0) / 40.0, 2.0));
    return vec3(r, g, b);
}

void main() {
    // 7-band spectral grid from 400 nm to 700 nm.
    float bands[7];
    bands[0] = 400.0;
    bands[1] = 450.0;
    bands[2] = 500.0;
    bands[3] = 550.0;
    bands[4] = 600.0;
    bands[5] = 650.0;
    bands[6] = 700.0;

    vec3 colour_out = vec3(0.0);
    vec3 weight_sum = vec3(0.0);

    vec2 delta = v_uv - u_center;

    for (int i = 0; i < 7; i++) {
        float lambda = bands[i];

        // Radial shift for this wavelength.
        float shift  = cauchy_shift(lambda) * u_dispersion;
        vec2  uv_shifted = u_center + delta * (1.0 + shift);

        // Luminance at the shifted UV (average all channels as proxy).
        vec3  sampled = texture2D(u_texture, uv_shifted).rgb;
        float lum     = dot(sampled, vec3(0.333));

        // Weight this band's contribution by the CIE CMF.
        vec3 cmf    = cie_cmf(lambda);
        colour_out += cmf * lum;
        weight_sum += cmf;
    }

    // Normalise by the total CMF weight.
    colour_out /= max(weight_sum, vec3(0.0001));

    // Blend with original to preserve saturation.
    vec3 original = texture2D(u_texture, v_uv).rgb;
    colour_out = mix(original, colour_out, 0.85);

    gl_FragColor = vec4(colour_out, 1.0);
}
