// axial_color_shift.frag
// Color shift as objects move through the focal plane — axial chromatic aberration.
//
// Because different wavelengths focus at different planes along the optical axis,
// an object that is in focus for green may be slightly out of focus for red and
// blue. The colour of a region therefore shifts depending on how far it is from
// the focal plane:
//   - Just inside focus: red/yellow cast (red focus plane is farther)
//   - Exactly in focus:  neutral
//   - Just outside focus: cyan/blue cast (blue focus plane is closer)
//
// Uniforms:
//   u_texture       — source image
//   u_depth         — depth map (0 = far, 1 = near) relative to focal plane
//                     Encode as signed distance: negative = before focus,
//                     positive = beyond focus, 0 = in focus.
//   u_focal_plane   — depth value that corresponds to perfect focus [0,1]
//   u_shift_scale   — maximum UV shift per channel, e.g. 0.008
//   u_resolution    — viewport resolution

precision highp float;

uniform sampler2D u_texture;
uniform sampler2D u_depth;
uniform float     u_focal_plane;
uniform float     u_shift_scale;
uniform vec2      u_resolution;

varying vec2 v_uv;

void main() {
    float depth = texture2D(u_depth, v_uv).r;

    // Signed defocus distance: positive = beyond focus, negative = before.
    float defocus = depth - u_focal_plane;

    // Axial colour shift: red lags, blue leads (typical crown glass).
    // At defocus=0 all offsets are zero.
    vec2 texel = 1.0 / u_resolution;

    // Blur radius grows with |defocus|.  Direction is axial (radial from center).
    vec2  center    = vec2(0.5);
    vec2  axis_dir  = normalize(v_uv - center + vec2(0.0001));

    float r_shift   =  defocus * u_shift_scale;        // red shifts outward when beyond focus
    float b_shift   = -defocus * u_shift_scale * 0.6;  // blue shifts in opposite direction

    float r = texture2D(u_texture, v_uv + axis_dir * r_shift).r;
    float g = texture2D(u_texture, v_uv).g;
    float b = texture2D(u_texture, v_uv + axis_dir * b_shift).b;

    gl_FragColor = vec4(r, g, b, 1.0);
}
