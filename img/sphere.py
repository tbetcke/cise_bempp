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
