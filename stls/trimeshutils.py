import numpy as np
import trimesh
import networkx as nx
import time

start = time.time()
# attach to logger so trimesh messages will be printed to console
trimesh.util.attach_to_log()

def hex_to_RGB(hex):
    ''' "#FFFFFF" -> [255,255,255] '''
    return [int(hex[i:i + 2], 16) for i in range(1, 6, 2)] # Pass 16 to the integer function for change of base


def linear_gradient(start_hex, finish_hex, n):
    ''' Returns a gradient list of (n) colors between two hex colors. start_hex and finish_hex
        should be the full six-digit color string, including the number sign ("#FFFFFF") '''
    # Starting and ending colors in RGB form
    s = hex_to_RGB(start_hex)
    f = hex_to_RGB(finish_hex)
    # Initialize a list of the output colors with the starting color
    RGB_list = []
    # Calculate a color at each evenly spaced value of t from 1 to n
    for t in range(0, n):
        # Interpolate RGB vector for color at the current value of t
        curr_vector = [round(int(s[j] + (float(t) / (n - 1)) * (f[j] - s[j])) / 255, 3) for j in range(3)]
        # Add it to our list of output colors
        RGB_list.append(curr_vector)

    return RGB_list


def set_color(RGBcolor, dtype=np.uint8):
    color = np.array(RGBcolor)
    if np.dtype(dtype).kind in 'iu':
        max_value = (2**(np.dtype(dtype).itemsize * 8)) - 1
        color *= max_value
    color = np.append(color, max_value).astype(dtype)
    return color


def fix_normals_direction(mesh):
    """
    Check to see if a mesh has normals pointed outside the solid.
    If the mesh is not watertight, this is meaningless.
    """
    volume = trimesh.triangles.mass_properties(mesh.triangles, crosses=mesh.triangles_cross, skip_inertia=True)['volume']
    flipped = volume < 0.0

    if flipped:
        trimesh.constants.log.debug('Flipping face normals and winding')
        # since normals were regenerated, this means winding is backwards
        # if winding is incoherent this won't fix anything
        mesh.faces = np.fliplr(mesh.faces)
        mesh.face_normals = None


def fix_face_winding(mesh):
    """
    Traverse and change mesh faces in-place to make sure winding is coherent,
    or that edges on adjacent faces are in opposite directions
    """

    if mesh.is_winding_consistent:
        trimesh.constants.log.debug('consistent winding, exiting repair')
        return

    # we create the face adjacency graph:
    # every node in g is an index of mesh.faces
    # every edge in g represents two faces which are connected
    graph_all = nx.from_edgelist(mesh.face_adjacency)
    faces = mesh.faces.view(np.ndarray).copy()
    flipped = 0

    # we are going to traverse the graph using BFS, so we have to start
    # a traversal for every connected component
    for components in nx.connected_components(graph_all):
        # get a subgraph for this component
        graph = graph_all.subgraph(components)
        # get the first node in the graph in a way that works on nx's new API and their old API
        start = next(iter(graph.nodes()))
        # we traverse every pair of faces in the graph
        # we modify mesh.faces and mesh.face_normals in place
        for face_pair in nx.bfs_edges(graph, start):
            # for each pair of faces, we convert them into edges,
            # find the edge that both faces share, and then see if the edges
            # are reversed in order as you would expect in a well constructed mesh
            face_pair = np.ravel(face_pair)
            pair = faces[face_pair]
            edges = trimesh.geometry.faces_to_edges(pair)
            overlap = trimesh.grouping.group_rows(np.sort(edges, axis=1), require_count=2)
            if len(overlap) == 0: # only happens on non-watertight meshes
                continue
            edge_pair = edges[[overlap[0]]]
            if edge_pair[0][0] == edge_pair[1][0]:
                # if the edges aren't reversed, invert the order of one of the faces
                flipped += 1
                faces[face_pair[1]] = faces[face_pair[1]][::-1]
    if flipped > 0:
        mesh.faces = faces
    trimesh.constants.log.debug('flipped %d/%d edges', flipped, len(mesh.faces) * 3)


def fix_normals(mesh):
    """
    Fix the winding and direction of a mesh face and face normals in-place
    Really only meaningful on watertight meshes, but will orient all
    faces and winding in a uniform way for non-watertight face patches as well.
    """
    fix_face_winding(mesh)
    fix_normals_direction(mesh)

# load a file by name or from a buffer
filename = 'out5.STL'
mesh = trimesh.load(filename)

#fix_normals(mesh)
direction = [0., 0., -1.0]
alpha = []
critical_angle = 30
colors = linear_gradient(start_hex='#ff0000', finish_hex="#0000ff", n=critical_angle)  # Create a gradient color string for different lines (blue - critical, red - 0)

for index in enumerate(mesh.face_normals):
    alpha_angle = int(np.rad2deg(np.arccos(np.clip(np.dot(mesh.face_normals[index[0]], direction), -1.0, 1.0))))
    alpha.append(alpha_angle)

    if critical_angle < 45:
        if 1 < alpha_angle <= critical_angle:
            mesh.visual.face_colors[index[0]] = set_color(colors[alpha_angle-1])
        elif critical_angle < alpha_angle <= 45:
            mesh.visual.face_colors[index[0]] = set_color(colors[critical_angle-1])
    else:
        if 1 < alpha_angle <= 45:
            mesh.visual.face_colors[index[0]] = set_color(colors[alpha_angle-1])
        elif 45 < alpha_angle <= critical_angle:
            mesh.visual.face_colors[index[0]] = set_color(colors[0])

import collections

counter=collections.Counter(alpha)
# print(counter)
# print(counter.values())
# print(counter.keys())
# print(counter.most_common(3))

end = time.time()
time_elapsed = end - start
print('elapsed time ' + str(round(time_elapsed, 1)) + ' s')

mesh.show()
# http://www.cb.uu.se/~aht/Vis2014/lecture2.pdf
# https://www.vtk.org/Wiki/VTK/Examples/Python/Visualization/ElevationBandsWithGlyphs
# https://conference.scipy.org/proceedings/scipy2015/pdfs/cory_quammen.pdf


