import os
import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader
import pyrr
from graphics2.loader.TextureLoader import load_texture
from graphics2.loader.ObjLoader import ObjLoader


def get_shader_file(filename):
    p = os.path.join(os.getcwd(), filename)
    return open(p, 'r').read()


# initializing glfw
if not glfw.init():
    glViewport(0, 0, 500, 500)
    raise Exception("glfw can not be initialized!")

# creating glfw window
window = glfw.create_window(1280, 700, "3D BUILDING MODEL", None, None)
if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")
glfw.make_context_current(window)

# loading obj_files
obj1_indices, obj1_buffer = ObjLoader.load_model("obj_files/obj1.obj")
obj2_indices, obj2_buffer = ObjLoader.load_model("obj_files/obj2.obj")
obj3_indices, obj3_buffer = ObjLoader.load_model("obj_files/obj3.obj")
obj4_indices, obj4_buffer = ObjLoader.load_model("obj_files/obj4.obj")

vertexShader = compileShader(get_shader_file(
    "shaders/vertex.shader"), GL_VERTEX_SHADER)
fragmentShader = compileShader(get_shader_file(
    "shaders/fragment.shader"), GL_FRAGMENT_SHADER)

shader = glCreateProgram()
glAttachShader(shader, vertexShader)
glAttachShader(shader, fragmentShader)
glLinkProgram(shader)

num = 3
VAO = glGenVertexArrays(num)
VBO = glGenBuffers(num)


# obj1 VAO
glBindVertexArray(VAO[0])
glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
glBufferData(GL_ARRAY_BUFFER, obj1_buffer.nbytes, obj1_buffer, GL_STATIC_DRAW)
# obj1 vertices, textures, normals
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, obj1_buffer.itemsize * 8, ctypes.c_void_p(0))
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, obj1_buffer.itemsize * 8, ctypes.c_void_p(12))
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, obj1_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

# obj2 VAO
glBindVertexArray(VAO[1])
glBindBuffer(GL_ARRAY_BUFFER, VBO[1])
glBufferData(GL_ARRAY_BUFFER, obj2_buffer.nbytes, obj2_buffer, GL_STATIC_DRAW)
# obj2 vertices, textures, normals
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, obj2_buffer.itemsize * 8, ctypes.c_void_p(0))
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, obj2_buffer.itemsize * 8, ctypes.c_void_p(12))
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, obj2_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

# obj3 VAO
glBindVertexArray(VAO[2])
glBindBuffer(GL_ARRAY_BUFFER, VBO[2])
glBufferData(GL_ARRAY_BUFFER, obj3_buffer.nbytes, obj3_buffer, GL_STATIC_DRAW)
# obj3 vertices, textures, normals
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, obj3_buffer.itemsize * 8, ctypes.c_void_p(0))
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, obj3_buffer.itemsize * 8, ctypes.c_void_p(12))
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, obj3_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

# obj4 VAO
glBindVertexArray(VAO[2])
glBindBuffer(GL_ARRAY_BUFFER, VBO[2])
glBufferData(GL_ARRAY_BUFFER, obj4_buffer.nbytes, obj4_buffer, GL_STATIC_DRAW)
# obj4 vertices, textures, normals
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, obj4_buffer.itemsize * 8, ctypes.c_void_p(0))
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, obj4_buffer.itemsize * 8, ctypes.c_void_p(12))
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, obj4_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)


# loading textures
textures = glGenTextures(num)
load_texture("images/floor5.jpg", textures[0])
load_texture("images/floor4.jpg", textures[1])
load_texture("images/fence.jpg", textures[2])
load_texture("images/floor5.jpg", textures[2])

# the main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()

    # making the 3d appropriate
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glUseProgram(shader)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # defining positions, location, matrix and rotation
    projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1280 / 720, 0.1, 220)
    position = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, -40, -150]))
    view = pyrr.matrix44.create_look_at(pyrr.Vector3([0, 0, 8]), pyrr.Vector3([0, 0, 0]), pyrr.Vector3([0, 1, 0]))
    model_loc = glGetUniformLocation(shader, "model")
    proj_loc = glGetUniformLocation(shader, "projection")
    view_loc = glGetUniformLocation(shader, "view")
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
    rot_y = pyrr.Matrix44.from_y_rotation(-0.3 * glfw.get_time())
    model = pyrr.matrix44.multiply(rot_y, position)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

    # draw ground1
    glBindVertexArray(VAO[0])
    glBindTexture(GL_TEXTURE_2D, textures[0])
    glDrawArrays(GL_TRIANGLES, 0, len(obj1_indices))

    # draw ground2
    glBindVertexArray(VAO[1])
    glBindTexture(GL_TEXTURE_2D, textures[1])
    glDrawArrays(GL_TRIANGLES, 0, len(obj2_indices))

    # draw ground3
    glBindVertexArray(VAO[2])
    glBindTexture(GL_TEXTURE_2D, textures[2])
    glDrawArrays(GL_TRIANGLES, 0, len(obj3_indices))

    # draw ground3
    glBindVertexArray(VAO[3])
    glBindTexture(GL_TEXTURE_2D, textures[3])
    glDrawArrays(GL_TRIANGLES, 0, len(obj4_indices))

    glfw.swap_buffers(window)

glfw.terminate()
