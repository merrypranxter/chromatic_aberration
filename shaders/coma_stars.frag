// coma_stars.frag
// Comet-shaped point sources with chromatic tail — off-axis coma aberration.
//
// Coma is a Seidel aberration where point sources off the optical axis become
// comet-shaped, with the tail pointing away from the centre. Combined with
// chromatic aberration the tail is a miniature rainbow: red at the base,
// through yellow and green, to blue at the tip. This shader detects bright
// highlights and deforms them into coma-shaped blobs with spectral colour.
//
// Uniforms:
//   u_texture       — source image
//   u_center        — optical axis, UV space (default vec2(0.5))
//   u_coma_strength — tail length scale, e.g. 0.012
//   u_threshold     — luminance threshold to trigger the coma effect, e.g. 0.85
//   u_resolution    — viewport size

precision highp float;

uniform sampler2D u_texture;
uniform vec2      u_center;
uniform float     u_coma_strength;
uniform float     u_threshold;
uniform vec2      u_resolution;

varying vec2 v_uv;

float luminance(vec3 c) {
    return dot(c, vec3(0.2126, 0.7152, 0.0722));
}

// Spectral colour for parameter t in [0, 1]: 0=red, 0.5=green, 1=blue.
vec3 spectral(float t) {
    float r = smoothstep(0.5, 0.0, t);
    float g = 1.0 - abs(t - 0.5) * 2.0;
    float b = smoothstep(0.5, 1.0, t);
    return vec3(r, g, b);
}

void main() {
    vec2 texel   = 1.0 / u_resolution;
    vec3 col     = texture2D(u_texture, v_uv).rgb;
    float lum    = luminance(col);

    // Direction away from optical axis — coma tail points this way.
    vec2  axis_dir = normalize(v_uv - u_center + vec2(0.0001));

    // Perpendicular direction for the fan spread.
    vec2  perp_dir = vec2(-axis_dir.y, axis_dir.x);

    // Distance from axis drives coma strength.
    float axis_dist = length(v_uv - u_center);
    float coma_r    = u_coma_strength * axis_dist;

    // Accumulate a fan of spectral samples.
    vec3  coma_col = vec3(0.0);
    float weight   = 0.0;
    int   N        = 12;

    for (int i = 0; i < 12; i++) {
        float t     = float(i) / float(N - 1);       // 0 → 1
        float tail  = t * coma_r;                     // how far along the tail
        float fan   = (t - 0.5) * coma_r * 0.5;      // lateral fan width

        vec2 sample_uv  = v_uv - axis_dir * tail + perp_dir * fan;
        float s_lum     = luminance(texture2D(u_texture, sample_uv).rgb);

        // Only pixels above threshold contribute (bright highlights only).
        float contrib   = smoothstep(u_threshold, 1.0, s_lum);
        coma_col       += spectral(t) * contrib;
        weight         += contrib;
    }

    if (weight > 0.0) {
        coma_col /= weight;
        float blend = smoothstep(u_threshold, 1.0, luminance(
            texture2D(u_texture, v_uv - axis_dir * coma_r * 0.5).rgb));
        col = mix(col, coma_col, blend * 0.6);
    }

    gl_FragColor = vec4(col, 1.0);
}
