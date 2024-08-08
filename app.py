import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, render_template
from streamlit.components.v1 import html
from io import BytesIO
import base64

# Flask App Initialization
flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    return render_template('index.html')

# Streamlit App Initialization
def generate_maze(n):
    G = nx.grid_2d_graph(n, n)
    maze = nx.Graph()
    stack = [(0, 0)]
    visited = set((0, 0))

    while stack:
        current = stack[-1]
        neighbors = [(current[0] + dx, current[1] + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
        neighbors = [n for n in neighbors if n in G and n not in visited]

        if neighbors:
            neighbor = neighbors[np.random.randint(len(neighbors))]
            stack.append(neighbor)
            visited.add(neighbor)
            maze.add_edge(current, neighbor)
        else:
            stack.pop()

    return maze

def plot_maze(maze, n):
    pos = {node: (node[1], -node[0]) for node in maze.nodes()}
    edges = maze.edges()

    plt.figure(figsize=(8, 8))
    nx.draw(maze, pos=pos, node_size=50, width=2, with_labels=False, node_color="blue", edge_color="black")
    plt.xlim(-1, n)
    plt.ylim(-n, 1)
    plt.gca().invert_yaxis()
    plt.show()

def maze_to_base64_image(maze, n):
    buf = BytesIO()
    plot_maze(maze, n)
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_bytes = buf.getvalue()
    return base64.b64encode(img_bytes).decode()

# Streamlit Section
st.title("Maze Visualization with Graph Algorithms")

n = st.slider("Select Maze Size", min_value=5, max_value=20, value=10)
maze = generate_maze(n)
maze_img = maze_to_base64_image(maze, n)

st.image(f"data:image/png;base64,{maze_img}", use_column_width=True)

# HTML template for Flask
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Maze Visualization</title>
</head>
<body>
    <h1>Maze Visualization</h1>
    <img src="data:image/png;base64,{}" alt="Maze">
</body>
</html>
""".format(maze_img)

html(html_template, height=600)

# Flask Server Runner
def run_flask():
    flask_app.run()

if __name__ == '__main__':
    run_flask()
