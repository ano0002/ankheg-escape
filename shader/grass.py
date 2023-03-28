from ursina import *
import time

                    
grass_shader = Shader(name='grass_shader', language=Shader.GLSL,

fragment='''
#version 430
uniform sampler2D tex;
uniform float iTime;
uniform vec3 cp;
uniform vec3 rotation;
#define BLADES 110



vec4 grass(vec2 p, float x)
{
	float s = mix(0.7, 2.0, 0.5 + sin(x * 12.0) * 0.5);
	p.x += pow(1.0 + p.y, 2.0) * 0.1 * cos(x * 0.5 + iTime);
	p.x *= s;
	p.y = (1.0 + p.y) * s - 1.0;
	float m = 1.0 - smoothstep(0.0, clamp(1.0 - p.y * 1.5, 0.01, 0.6) * 0.2 * s, pow(abs(p.x) * 19.0, 1.5) + p.y - 0.6);
	return vec4(mix(vec3(0.05, 0.1, 0.0) * 0.8, vec3(0.0, 0.3, 0.0), (p.y + 1.0) * 0.5 + abs(p.x)), m * smoothstep(-1.0, -0.9, p.y));
}


in vec2 window_size;
in vec2 uv;
out vec4 fragColor;
void main()
{
    vec3 ct = vec3(0, 0, 0);	
	vec3 cw = normalize(cp - ct);

    vec3 cu = normalize(cross(cw, vec3(0.0, 1.0, 0.0)));
 
	vec3 cv = normalize(cross(cu, cw));
	
	mat3 rm = mat3(cu, cv, cw);
	
	vec2 t = uv;
	
	vec3 ro = cp, rd = vec3(t, 1);
	
	vec3 fcol = texture(tex, uv).rgb;
 
	for(int i = 0; i < BLADES; i += 1)
	{
		float z = -(float(BLADES - i) * 0.1 + 1.0);
		vec4 pln = vec4(0.0, 0.0, -1.0, z);
		float t = (pln.w - dot(pln.xyz, ro)) / dot(pln.xyz, rd);
		vec2 tc = ro.xy + rd.xy * t;
		
		tc.x += cos(float(i) * 3.0) * 4.0;
		
		float cell = floor(tc.x);
		
		tc.x = (tc.x - cell) - 0.5;
		
		vec4 c = grass(tc, float(i) + cell * 10.0);
		
		fcol = mix(fcol, c.rgb, step(0.0, t) * c.w);
	}
	
	fcol = pow(fcol* 1.1, vec3(0.8));
	
	
	
	fragColor.rgb = fcol * 1.8 ;
	fragColor.a = 1.0;
}

''',
default_input={
    'iTime': 1
})

if __name__ == '__main__':
    app = Ursina()
    
    Entity(model='cube')
    
    delta = 0
    camera.shader = grass_shader
    def update():
        global delta
        delta += time.dt
        camera.set_shader_input('iTime',delta)
        camera.set_shader_input('cp',camera.position)
        camera.set_shader_input('rotation',Vec3(tuple(i*360 for i in camera.rotation.normalized())))
    
    EditorCamera()
    
    app.run()