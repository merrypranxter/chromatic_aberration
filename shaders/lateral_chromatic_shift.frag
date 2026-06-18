// lateral_chromatic_shift.frag
// Radial RGB channel separation — the classic lateral chromatic aberration.
//
// Each color channel is sampled from a slightly different radial position,
// mimicking the way a simple lens refracts red, green, and blue light
// to different extents. The shift magnitude grows with distance from the
// optical axis, following the actual behaviour of a thin lens with dispersion.
//
// Uniforms:
//   u_texture        — the source image (sampler2D)
//   u_shift_amount   — base shift strength in UV units (e.g. 0.005)
//   u_center         — optical axis in UV space (typically vec2(0.5, 0.5))
//   u_wavelength_ratio — relative shift per channel: vec3(red, green, blue)
//                        A physically reasonable default is vec3(1.0, 0.0, -0.6)
//                        (red shifts outward, blue shifts inward, green stays)

precision highp float;

uniform sampler2D u_texture;
uniform float     u_shift_amount;
uniform vec2      u_center;
uniform vec3      u_wavelength_ratio; // (r_scale, g_scale, b_scale)

varying vec2 v_uv;

// Radially offset a UV coordinate by `amount` away from `center`.
vec2 radial_offset(vec2 uv, vec2 center, float amount) {
    vec2 delta = uv - center;
    return uv + delta * amount;
}

void main() {
    vec2 uv = v_uv;

    // Sample each channel at its own radially displaced UV coordinate.
    float r = texture2D(u_texture, radial_offset(uv, u_center, u_shift_amount * u_wavelength_ratio.r)).r;
    float g = texture2D(u_texture, radial_offset(uv, u_center, u_shift_amount * u_wavelength_ratio.g)).g;
    float b = texture2D(u_texture, radial_offset(uv, u_center, u_shift_amount * u_wavelength_ratio.b)).b;

    // Alpha from the green channel (neutral / unshifted reference).
    float a = texture2D(u_texture, uv).a;

    gl_FragColor = vec4(r, g, b, a);
}
