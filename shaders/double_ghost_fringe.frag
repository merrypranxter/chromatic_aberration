// double_ghost_fringe.frag
// Offset ghost image with colour tint — internal reflection fringe.
//
// A lens element partially reflects light back through the system, creating a
// secondary "ghost" image at a parabolic offset across the frame. The ghost
// carries its own chromatic signature because it has travelled a different
// optical path. This shader renders that secondary image and composites it
// over the primary with an additive blend, simulating the lens-flare-adjacent
// artefact common in pre-coated optics.
//
// Uniforms:
//   u_texture       — source image
//   u_resolution    — viewport size in pixels
//   u_ghost_offset  — centre offset of the ghost image in UV space, e.g. vec2(0.15, 0.0)
//   u_ghost_scale   — zoom factor for the ghost (typically > 1.0, e.g. 1.12)
//   u_ghost_tint    — tint colour for the ghost, e.g. vec3(0.9, 0.5, 1.0) (magenta)
//   u_ghost_alpha   — opacity of the ghost overlay, e.g. 0.18
//   u_ca_amount     — chromatic aberration within the ghost itself

precision highp float;

uniform sampler2D u_texture;
uniform vec2      u_resolution;
uniform vec2      u_ghost_offset;
uniform float     u_ghost_scale;
uniform vec3      u_ghost_tint;
uniform float     u_ghost_alpha;
uniform float     u_ca_amount;

varying vec2 v_uv;

// Sample the ghost image at a given UV, applying an extra internal CA.
vec3 ghost_sample(vec2 uv) {
    vec2 center = vec2(0.5);
    vec2 delta  = uv - center;

    // Ghost UV: offset + scale from its own center.
    vec2 ghost_uv = center + u_ghost_offset + delta / u_ghost_scale;

    // Internal CA within the ghost.
    vec2 ca_dir = normalize(delta + vec2(0.0001));
    float r = texture2D(u_texture, ghost_uv + ca_dir * u_ca_amount).r;
    float g = texture2D(u_texture, ghost_uv).g;
    float b = texture2D(u_texture, ghost_uv - ca_dir * u_ca_amount * 0.5).b;

    return vec3(r, g, b) * u_ghost_tint;
}

void main() {
    vec3 primary = texture2D(u_texture, v_uv).rgb;

    // Parabolic falloff: ghost is brightest at image edges, dimmer at centre.
    float dist       = length(v_uv - vec2(0.5));
    float falloff    = smoothstep(0.0, 0.7, dist);

    vec3 ghost = ghost_sample(v_uv);
    vec3 result = primary + ghost * u_ghost_alpha * falloff;

    gl_FragColor = vec4(result, 1.0);
}
