import bempp.api

g = bempp.api.shapes.sphere(h=0.3)


with open("sphere.tex", "w") as f:
    f.write("\\begin{tikzpicture}[x={(1.732cm,-1cm)},y={(1.732cm,1cm)},z={(0,2cm)}]\n")

    for i, j in enumerate(g.vertices.T):
        f.write(f"\\coordinate (v{i}) at ({j[0]},{j[1]},{j[2]});\n")

    triangles = [(sum(g.vertices.T[i] for i in t) / 3, t) for t in g.elements.T]

    triangles.sort(key=lambda x: x[0][0] + x[0][2] - x[0][1])
    for _, (i, j, k) in triangles:
        f.write(f"\\draw[fill=white, fill opacity=0.8] (v{i}) -- (v{j}) -- (v{k}) -- cycle;\n")
    f.write("\\end{tikzpicture}")


def to2d(i, j, k):
    return 1.732 * i + 1.732 * j, -i + j + 2 * k


with open("triangles_command.tex", "w") as f:
    f.write("\\newcommand{\\drawtriangles}{\n")

    triangles = [(sum(g.vertices.T[i] for i in t) / 3, t) for t in g.elements.T]

    triangles.sort(key=lambda x: x[0][0] + x[0][2] - x[0][1])
    for _, (i, j, k) in triangles:
        if _[0] + _[2] - _[1] > 0.6:
            p1 = to2d(*g.vertices.T[i])
            p2 = to2d(*g.vertices.T[j])
            p3 = to2d(*g.vertices.T[k])
            if -1.5 > max(p1[0], p2[0], p3[0]) or 1.5 < min(p1[0], p2[0], p3[0]):
                continue
            if -1.5 > max(p1[1], p2[1], p3[1]) or 1.5 < min(p1[1], p2[1], p3[1]):
                continue

            f.write(f"\\draw ({p1[0]},{p1[1]}) -- ({p2[0]},{p2[1]}) -- ({p3[0]},{p3[1]}) -- cycle;\n")
    f.write("}")


with open("colouring_triangles.tex", "w") as f:
    triangles = [(sum(g.vertices.T[i] for i in t) / 3, t) for t in g.elements.T]

    triangles.sort(key=lambda x: x[0][0] + x[0][2] - x[0][1])
    triangles = [(i, j) for i, j in triangles if i[0] + i[2] - i[1] > 0.6][::-1]

    at_vertex = {}
    numbers = []
    for i, j in triangles:
        banned = []
        for v in j:
            if v not in at_vertex:
                at_vertex[v] = []
            banned += at_vertex[v]
        n = min([i for i in range(1, 50) if i not in banned])
        numbers.append(n)
        for v in j:
            at_vertex[v].append(n)

    for n, (_, (i, j, k)) in zip(numbers, triangles):
        if _[0] + _[2] - _[1] > 0.6:
            p1 = to2d(*g.vertices.T[i])
            p2 = to2d(*g.vertices.T[j])
            p3 = to2d(*g.vertices.T[k])
            if -1.5 > max(p1[0], p2[0], p3[0]) or 1.5 < min(p1[0], p2[0], p3[0]):
                continue
            if -1.5 > max(p1[1], p2[1], p3[1]) or 1.5 < min(p1[1], p2[1], p3[1]):
                continue

            f.write(f"\\draw[fill=col{n}] ({p1[0]},{p1[1]}) -- ({p2[0]},{p2[1]}) -- ({p3[0]},{p3[1]}) -- cycle;\n")
            mid = ((p1[0] + p2[0] + p3[0]) / 3, (p1[1] + p2[1] + p3[1]) / 3)
            if n == 1:
                f.write(f"\\fill[white,fill opacity=0.65] ({mid[0]},{mid[1]}) circle (1pt);\n")
            if n == 2:
                f.write(f"\\begin{{scope}}[shift={{(2pt,-2pt)}}]\\fill[white,fill opacity=0.65] ({mid[0]},{mid[1]}) circle (1pt);\\end{{scope}}\n")
                f.write(f"\\begin{{scope}}[shift={{(-2pt,2pt)}}]\\fill[white,fill opacity=0.65] ({mid[0]},{mid[1]}) circle (1pt);\\end{{scope}}\n")
            if n == 3:
                f.write(f"\\begin{{scope}}[shift={{(2pt,-2pt)}}]\\fill[white,fill opacity=0.65] ({mid[0]},{mid[1]}) circle (1pt);\\end{{scope}}\n")
                f.write(f"\\fill[white,fill opacity=0.65] ({mid[0]},{mid[1]}) circle (1pt);\n")
                f.write(f"\\begin{{scope}}[shift={{(-2pt,2pt)}}]\\fill[white,fill opacity=0.65] ({mid[0]},{mid[1]}) circle (1pt);\\end{{scope}}\n")
            if n == 4:
                f.write(f"\\begin{{scope}}[shift={{(2pt,-2pt)}}]\\fill[white,fill opacity=0.65] ({mid[0]},{mid[1]}) circle (1pt);\\end{{scope}}\n")
                f.write(f"\\begin{{scope}}[shift={{(-2pt,2pt)}}]\\fill[white,fill opacity=0.65] ({mid[0]},{mid[1]}) circle (1pt);\\end{{scope}}\n")
                f.write(f"\\begin{{scope}}[shift={{(2pt,2pt)}}]\\fill[white,fill opacity=0.65] ({mid[0]},{mid[1]}) circle (1pt);\\end{{scope}}\n")
                f.write(f"\\begin{{scope}}[shift={{(-2pt,-2pt)}}]\\fill[white,fill opacity=0.65] ({mid[0]},{mid[1]}) circle (1pt);\\end{{scope}}\n")
            if n == 5:
                f.write(f"\\fill[white,fill opacity=0.65] ({mid[0]},{mid[1]}) circle (1pt);\n")
                f.write(f"\\begin{{scope}}[shift={{(2pt,-2pt)}}]\\fill[white,fill opacity=0.65] ({mid[0]},{mid[1]}) circle (1pt);\\end{{scope}}\n")
                f.write(f"\\begin{{scope}}[shift={{(-2pt,2pt)}}]\\fill[white,fill opacity=0.65] ({mid[0]},{mid[1]}) circle (1pt);\\end{{scope}}\n")
                f.write(f"\\begin{{scope}}[shift={{(2pt,2pt)}}]\\fill[white,fill opacity=0.65] ({mid[0]},{mid[1]}) circle (1pt);\\end{{scope}}\n")
                f.write(f"\\begin{{scope}}[shift={{(-2pt,-2pt)}}]\\fill[white,fill opacity=0.65] ({mid[0]},{mid[1]}) circle (1pt);\\end{{scope}}\n")
            if n == 6:
                f.write(f"\\begin{{scope}}[shift={{(2pt,-2pt)}}]\\fill[white,fill opacity=0.65] ({mid[0]},{mid[1]}) circle (1pt);\\end{{scope}}\n")
                f.write(f"\\begin{{scope}}[shift={{(-2pt,2pt)}}]\\fill[white,fill opacity=0.65] ({mid[0]},{mid[1]}) circle (1pt);\\end{{scope}}\n")
                f.write(f"\\begin{{scope}}[shift={{(2pt,2pt)}}]\\fill[white,fill opacity=0.65] ({mid[0]},{mid[1]}) circle (1pt);\\end{{scope}}\n")
                f.write(f"\\begin{{scope}}[shift={{(-2pt,-2pt)}}]\\fill[white,fill opacity=0.65] ({mid[0]},{mid[1]}) circle (1pt);\\end{{scope}}\n")
                f.write(f"\\begin{{scope}}[shift={{(2pt,0pt)}}]\\fill[white,fill opacity=0.65] ({mid[0]},{mid[1]}) circle (1pt);\\end{{scope}}\n")
                f.write(f"\\begin{{scope}}[shift={{(-2pt,0pt)}}]\\fill[white,fill opacity=0.65] ({mid[0]},{mid[1]}) circle (1pt);\\end{{scope}}\n")
            if n == 7:
                f.write(f"\\fill[white,fill opacity=0.65] ({mid[0]},{mid[1]}) circle (1pt);\n")
                f.write(f"\\begin{{scope}}[shift={{(2pt,-2pt)}}]\\fill[white,fill opacity=0.65] ({mid[0]},{mid[1]}) circle (1pt);\\end{{scope}}\n")
                f.write(f"\\begin{{scope}}[shift={{(-2pt,2pt)}}]\\fill[white,fill opacity=0.65] ({mid[0]},{mid[1]}) circle (1pt);\\end{{scope}}\n")
                f.write(f"\\begin{{scope}}[shift={{(2pt,2pt)}}]\\fill[white,fill opacity=0.65] ({mid[0]},{mid[1]}) circle (1pt);\\end{{scope}}\n")
                f.write(f"\\begin{{scope}}[shift={{(-2pt,-2pt)}}]\\fill[white,fill opacity=0.65] ({mid[0]},{mid[1]}) circle (1pt);\\end{{scope}}\n")
                f.write(f"\\begin{{scope}}[shift={{(2pt,0pt)}}]\\fill[white,fill opacity=0.65] ({mid[0]},{mid[1]}) circle (1pt);\\end{{scope}}\n")
                f.write(f"\\begin{{scope}}[shift={{(-2pt,0pt)}}]\\fill[white,fill opacity=0.65] ({mid[0]},{mid[1]}) circle (1pt);\\end{{scope}}\n")
