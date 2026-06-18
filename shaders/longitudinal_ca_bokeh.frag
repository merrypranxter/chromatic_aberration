// longitudinal_ca_bokeh.frag
// Depth-dependent color fringing in out-of-focus areas — longitudinal CA.
//
// In a real lens the focal length varies with wavelength:
//   f(λ) ≈ f_green / (1 + (n(λ) - n_green) / (n_green - 1))
// This shader approximates that by giving each colour channel a different
// circle of confusion (CoC) radius, then blurring each channel independently.
// The result is the "beautiful" chromatic bokeh: out-of-focus highlights
// glow with coloured halos.
//
// Uniforms:
//   u_texture       — source image
//   u_depth         — depth / focus map (0 = in-focus, 1 = far out-of-focus)
//   u_coc_scale     — global CoC scale factor
//   u_coc_rgb       — per-channel CoC multipliers, e.g. vec3(1.3, 1.0, 0.75)
//                     (red focuses behind green, blue focuses in front)
//   u_resolution    — viewport size in pixels
//   u_samples       — number of disc samples (8–16 is usually enough)

precision highp float;

uniform sampler2D u_texture;
uniform sampler2D u_depth;
uniform float     u_coc_scale;
uniform vec3      u_coc_rgb;
uniform vec2      u_resolution;
uniform int       u_samples;

varying vec2 v_uv;

// Golden-angle spiral sample pattern for a disc kernel.
vec2 disc_sample(int i, int total) {
    float golden_angle = 2.399963; // radians
    float r = sqrt(float(i + 1) / float(total));
    float theta = float(i) * golden_angle;
    return vec2(cos(theta), sin(theta)) * r;
}

void main() {
    float depth = texture2D(u_depth, v_uv).r;

    // CoC radius in UV space for each channel.
    float base_coc = depth * u_coc_scale;
    vec3  coc      = base_coc * u_coc_rgb;

    vec3 colour_sum = vec3(0.0);
    int n = u_samples;

    for (int i = 0; i < 16; i++) {
        if (i >= n) break;
        vec2 offset = disc_sample(i, n) / u_resolution;

        colour_sum.r += texture2D(u_texture, v_uv + offset * coc.r).r;
        colour_sum.g += texture2D(u_texture, v_uv + offset * coc.g).g;
        colour_sum.b += texture2D(u_texture, v_uv + offset * coc.b).b;
    }

    colour_sum /= float(n);

    gl_FragColor = vec4(colour_sum, texture2D(u_texture, v_uv).a);
}
