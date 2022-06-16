import numpy as np


class ObjLoader:
    buffer = []

    @staticmethod
    def data(data_values, coordinates, skip, data_type):
        for d in data_values:
            if d == skip:
                continue
            if data_type == 'float':
                coordinates.append(float(d))
            elif data_type == 'int':
                coordinates.append(int(d) - 1)

    @staticmethod
    def vertex_buffer(indices_data, vertices, textures, normals):
        for i, ind in enumerate(indices_data):
            if i % 3 == 0:  # sort the vertex coordinates
                start = ind * 3
                end = start + 3
                ObjLoader.buffer.extend(vertices[start:end])
            elif i % 3 == 1:  # sort the texture coordinates
                start = ind * 2
                end = start + 2
                ObjLoader.buffer.extend(textures[start:end])
            elif i % 3 == 2:  # sort the normal vectors
                start = ind * 3
                end = start + 3
                ObjLoader.buffer.extend(normals[start:end])

    @staticmethod
    def load_model(file):
        vert_coords = []  # will contain all the vertex coordinates
        tex_coords = []  # will contain all the texture coordinates
        norm_coords = []  # will contain all the vertex normals
        all_indices = []  # will contain all the vertex, texture and normal indices
        indices = []  # will contain the indices for indexed drawing

        with open(file, 'r') as f:
            line = f.readline()
            while line:
                values = line.split()
                if values[0] == 'v':
                    ObjLoader.data(values, vert_coords, 'v', 'float')
                elif values[0] == 'vt':
                    ObjLoader.data(values, tex_coords, 'vt', 'float')
                elif values[0] == 'vn':
                    ObjLoader.data(values, norm_coords, 'vn', 'float')
                elif values[0] == 'f':
                    for value in values[1:]:
                        val = value.split('/')
                        ObjLoader.data(val, all_indices, 'f', 'int')
                        indices.append(int(val[0]) - 1)

                line = f.readline()

        ObjLoader.vertex_buffer(all_indices, vert_coords, tex_coords, norm_coords)
        buffer = ObjLoader.buffer.copy()
        ObjLoader.buffer = []

        return np.array(indices, dtype='uint32'), np.array(buffer, dtype='float32')
