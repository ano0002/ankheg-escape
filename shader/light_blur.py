from ursina import *
camera_gaussian_blur = Shader(
fragment='''
#version 130
uniform vec3 size;//width,height,radius

const int Quality = 8;
const int Directions = 16;
const float Pi = 6.28318530718;//pi * 2
uniform sampler2D tex;
in vec2 uv;
in vec2 window_size;
out vec4 color;
void main()
{
    vec2 radius = size.z/size.xy;
    vec4 frag = texture( tex, uv);
    for( float d=0.0;d<Pi;d+=Pi/float(Directions) )
    {
        for( float i=1.0/float(Quality);i<=1.0;i+=1.0/float(Quality) )
        {
            frag += texture( tex, uv+vec2(cos(d),sin(d))*radius*i);
        }
    }
    frag /= float(Quality)*float(Directions)+1.0;
    color =  frag;
}
''',
default_input=dict(
    blur_size = .1
))
if __name__ == "__main__":
    app = Ursina()
    
    Entity(model='cube', scale=1)
    camera.shader=camera_gaussian_blur
    
    camera.set_shader_input('size', Vec3(1,1,.005))

    EditorCamera()
    
    app.run()