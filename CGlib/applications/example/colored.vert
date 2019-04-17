#version 330 core

in vec4 vPosition;
in vec4 vInColor;
out vec4 vOutColor;

void main()
{
	vOutColor = vInColor;
	gl_Position = vPosition;
}
