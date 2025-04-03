'''OpenGL extension KHR.parallel_shader_compile

This module customises the behaviour of the 
OpenGL.raw.GLES2.KHR.parallel_shader_compile to provide a more 
Python-friendly API

Overview (from the spec)
	
	Compiling GLSL into implementation-specific code can be a time consuming
	process, so a GL implementation may wish to perform the compilation in a
	separate CPU thread. This extension provides a mechanism for the application
	to provide a hint to limit the number of threads it wants to be used to
	compile shaders, as well as a query to determine if the compilation process
	is complete.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/KHR/parallel_shader_compile.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLES2 import _types, _glgets
from OpenGL.raw.GLES2.KHR.parallel_shader_compile import *
from OpenGL.raw.GLES2.KHR.parallel_shader_compile import _EXTENSION_NAME

def glInitParallelShaderCompileKHR():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION