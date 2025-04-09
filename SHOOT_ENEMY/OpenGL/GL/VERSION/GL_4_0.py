'''OpenGL extension VERSION.GL_4_0

This module customises the behaviour of the 
OpenGL.raw.GL.VERSION.GL_4_0 to provide a more 
Python-friendly API

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/VERSION/GL_4_0.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.VERSION.GL_4_0 import *
from OpenGL.raw.GL.VERSION.GL_4_0 import _EXTENSION_NAME

def glInitGl40VERSION():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

# INPUT glUniform1dv.value size not checked against count
glUniform1dv=wrapper.wrapper(glUniform1dv).setInputArraySize(
    'value', None
)
# INPUT glUniform2dv.value size not checked against count*2
glUniform2dv=wrapper.wrapper(glUniform2dv).setInputArraySize(
    'value', None
)
# INPUT glUniform3dv.value size not checked against count*3
glUniform3dv=wrapper.wrapper(glUniform3dv).setInputArraySize(
    'value', None
)
# INPUT glUniform4dv.value size not checked against count*4
glUniform4dv=wrapper.wrapper(glUniform4dv).setInputArraySize(
    'value', None
)
# INPUT glUniformMatrix2dv.value size not checked against count*4
glUniformMatrix2dv=wrapper.wrapper(glUniformMatrix2dv).setInputArraySize(
    'value', None
)
# INPUT glUniformMatrix3dv.value size not checked against count*9
glUniformMatrix3dv=wrapper.wrapper(glUniformMatrix3dv).setInputArraySize(
    'value', None
)
# INPUT glUniformMatrix4dv.value size not checked against count*16
glUniformMatrix4dv=wrapper.wrapper(glUniformMatrix4dv).setInputArraySize(
    'value', None
)
# INPUT glUniformMatrix2x3dv.value size not checked against count*6
glUniformMatrix2x3dv=wrapper.wrapper(glUniformMatrix2x3dv).setInputArraySize(
    'value', None
)
# INPUT glUniformMatrix2x4dv.value size not checked against count*8
glUniformMatrix2x4dv=wrapper.wrapper(glUniformMatrix2x4dv).setInputArraySize(
    'value', None
)
# INPUT glUniformMatrix3x2dv.value size not checked against count*6
glUniformMatrix3x2dv=wrapper.wrapper(glUniformMatrix3x2dv).setInputArraySize(
    'value', None
)
# INPUT glUniformMatrix3x4dv.value size not checked against count*12
glUniformMatrix3x4dv=wrapper.wrapper(glUniformMatrix3x4dv).setInputArraySize(
    'value', None
)
# INPUT glUniformMatrix4x2dv.value size not checked against count*8
glUniformMatrix4x2dv=wrapper.wrapper(glUniformMatrix4x2dv).setInputArraySize(
    'value', None
)
# INPUT glUniformMatrix4x3dv.value size not checked against count*12
glUniformMatrix4x3dv=wrapper.wrapper(glUniformMatrix4x3dv).setInputArraySize(
    'value', None
)
# OUTPUT glGetUniformdv.params COMPSIZE(program, location) 
glGetActiveSubroutineUniformiv=wrapper.wrapper(glGetActiveSubroutineUniformiv).setOutput(
    'values',size=_glgets._glget_size_mapping,pnameArg='pname',orPassIn=True
)
glGetActiveSubroutineUniformName=wrapper.wrapper(glGetActiveSubroutineUniformName).setOutput(
    'length',size=(1,),orPassIn=True
).setOutput(
    'name',size=lambda x:(x,),pnameArg='bufsize',orPassIn=True
)
glGetActiveSubroutineName=wrapper.wrapper(glGetActiveSubroutineName).setOutput(
    'length',size=(1,),orPassIn=True
).setOutput(
    'name',size=lambda x:(x,),pnameArg='bufsize',orPassIn=True
)
# INPUT glUniformSubroutinesuiv.indices size not checked against count
glUniformSubroutinesuiv=wrapper.wrapper(glUniformSubroutinesuiv).setInputArraySize(
    'indices', None
)
glGetUniformSubroutineuiv=wrapper.wrapper(glGetUniformSubroutineuiv).setOutput(
    'params',size=(1,),orPassIn=True
)
glGetProgramStageiv=wrapper.wrapper(glGetProgramStageiv).setOutput(
    'values',size=(1,),orPassIn=True
)
# INPUT glPatchParameterfv.values size not checked against 'pname'
glPatchParameterfv=wrapper.wrapper(glPatchParameterfv).setInputArraySize(
    'values', None
)
# INPUT glDeleteTransformFeedbacks.ids size not checked against n
glDeleteTransformFeedbacks=wrapper.wrapper(glDeleteTransformFeedbacks).setInputArraySize(
    'ids', None
)
glGenTransformFeedbacks=wrapper.wrapper(glGenTransformFeedbacks).setOutput(
    'ids',size=lambda x:(x,),pnameArg='n',orPassIn=True
)
glGetQueryIndexediv=wrapper.wrapper(glGetQueryIndexediv).setOutput(
    'params',size=_glgets._glget_size_mapping,pnameArg='pname',orPassIn=True
)
### END AUTOGENERATED SECTION
