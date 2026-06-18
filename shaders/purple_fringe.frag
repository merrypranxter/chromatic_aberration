// purple_fringe.frag
// High-contrast edge violet/blue bloom — purple fringing.
//
// Consumer zoom lenses and fast primes suffer from extreme violet/blue
// aberration at high-contrast boundaries (e.g. tree branches against sky).
// The shader:
//   1. Computes a luminance gradient to find high-contrast edges.
//   2. Along the gradient direction, samples the UV channel and exaggerates it.
//   3. Blends the violet bloom back over the original image.
//
// Uniforms:
//   u_texture        — source image
//   u_resolution     — viewport size in pixels
//   u_fringe_amount  — bloom intensity [0, 1], e.g. 0.35
//   u_threshold      — luminance gradient threshold to trigger fringing
//   u_fringe_color   — tint of the bloom, e.g. vec3(0.6, 0.0, 1.0) for violet

precision highp float;

uniform sampler2D u_texture;
uniform vec2      u_resolution;
uniform float     u_fringe_amount;
uniform float     u_threshold;
uniform vec3      u_fringe_color;

varying vec2 v_uv;

float luminance(vec3 c) {
    return dot(c, vec3(0.2126, 0.7152, 0.0722));
}

void main() {
    vec2 texel = 1.0 / u_resolution;

    vec3 col = texture2D(u_texture, v_uv).rgb;

    // Sobel gradient of luminance.
    float lum_px = luminance(texture2D(u_texture, v_uv + vec2( texel.x, 0.0)).rgb);
    float lum_mx = luminance(texture2D(u_texture, v_uv + vec2(-texel.x, 0.0)).rgb);
    float lum_py = luminance(texture2D(u_texture, v_uv + vec2(0.0,  texel.y)).rgb);
    float lum_my = luminance(texture2D(u_texture, v_uv + vec2(0.0, -texel.y)).rgb);

    vec2  grad      = vec2(lum_px - lum_mx, lum_py - lum_my);
    float grad_mag  = length(grad);

    // Only bloom where the gradient exceeds the threshold.
    float edge_mask = smoothstep(u_threshold, u_threshold * 2.0, grad_mag);

    // Sample a bloom kernel along the gradient direction.
    vec3 bloom = vec3(0.0);
    vec2 dir   = (grad_mag > 0.0001) ? normalize(grad) * texel : vec2(0.0);
    float weights = 0.0;
    for (int i = 1; i <= 5; i++) {
        float w = 1.0 / float(i);
        bloom   += texture2D(u_texture, v_uv + dir * float(i) * 2.0).rgb * w;
        weights += w;
    }
    bloom /= weights;

    // Tint the bloom toward the fringe color.
    vec3 fringe = mix(bloom, u_fringe_color * luminance(bloom), 0.7);

    gl_FragColor = vec4(mix(col, col + fringe * u_fringe_amount, edge_mask), 1.0);
}
