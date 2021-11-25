import numpy as np


# чтение из файла
def read_obj(filename, encoding="utf-8"):
    vertexes = []
    faces = []
    lines = []
    other = []

    file = open(filename, 'r', encoding=encoding)
    file_lines = file.readlines()
    for file_line in file_lines:
        data = file_line.strip()
        if len(data):
            type_, *data = data.split()
            if type_ == 'v':
                vertex = np.array(data, dtype=np.float64)
                vertexes.append(vertex)
            elif type_ == 'f':
                face = [int(item.split('/')[0]) - 1 for item in data]
                faces.append(face)
            elif type_ == 'l':
                line = [int(item) - 1 for item in data]
                lines.append(line)
            elif type_ == "#":
                continue
            else:
                other.append(file_lines)

    return {"vertexes": vertexes,
            "faces": faces,
            "lines": lines,
            "other": other}
