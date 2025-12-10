import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches
import os
import numpy as np
import imageio
from matplotlib.backends.backend_agg import FigureCanvasAgg

# Ensure output directory exists
output_dir = "docs/img"
os.makedirs(output_dir, exist_ok=True)

class UnionFind:
    def __init__(self, nodes):
        self.parent = {node: node for node in nodes}
    
    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]
    
    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u != root_v:
            self.parent[root_u] = root_v
            return True
        return False

def create_videos_kruskal():
    # --- Configuration ---
    plt.style.use('dark_background')
    
    # Colors
    COLOR_BG = '#1e1e1e'
    COLOR_NODE = '#ffffff'
    COLOR_NODE_TEXT = '#000000'
    COLOR_EDGE_EMPTY = '#444444'
    COLOR_EDGE_MST = '#00ccff' # Neon Cyan
    COLOR_EDGE_REJECTED = '#ff4444' # Red
    COLOR_SCANNING = '#ffd700' # Gold
    COLOR_TEXT = '#ffffff'

    # Graph Setup (Larger Graph)
    G = nx.Graph()
    # 8 Nodes: A-H
    # Edges with weights
    edges = [
        ('A', 'B', 4), ('A', 'E', 2),
        ('B', 'C', 6), ('B', 'F', 9), ('B', 'E', 12),
        ('C', 'D', 3), ('C', 'G', 5), ('C', 'F', 1),
        ('D', 'H', 7),
        ('E', 'F', 8),
        ('F', 'G', 11), ('F', 'H', 15),
        ('G', 'H', 10),
        ('E', 'I', 13) # Wait, let's stick to 8 nodes A-H
    ]
    # Redefine edges for 8 nodes (2x4 gridish)
    edges = [
        ('A', 'B', 4), ('B', 'C', 8), ('C', 'D', 7),
        ('E', 'F', 9), ('F', 'G', 2), ('G', 'H', 14),
        ('A', 'E', 8), ('B', 'F', 11), ('C', 'G', 4), ('D', 'H', 9),
        ('B', 'E', 1), ('C', 'F', 7), ('D', 'G', 6), ('C', 'H', 10) # Diagonals/Cross
    ]
    # Clean up duplicate weights for clarity if needed, but duplicates are fine.
    # Let's ensure connectivity and interesting structure.
    
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)

    pos = {
        'A': (0, 3), 'B': (2, 3), 'C': (4, 3), 'D': (6, 3),
        'E': (0, 1), 'F': (2, 1), 'G': (4, 1), 'H': (6, 1)
    }

    # --- Algorithm Execution ---
    history = []
    
    # Sort edges
    sorted_edges = sorted(edges, key=lambda x: x[2])
    uf = UnionFind(G.nodes())
    mst_edges = set()
    
    history.append({
        'msg': "Initialisation : Tri des arêtes par poids",
        'mst_edges': mst_edges.copy(),
        'scanning': None,
        'rejected': None
    })
    
    for u, v, w in sorted_edges:
        history.append({
            'msg': f"Examen de ({u}, {v}) - Poids {w}",
            'mst_edges': mst_edges.copy(),
            'scanning': (u, v),
            'rejected': None
        })
        
        if uf.union(u, v):
            mst_edges.add((u, v))
            mst_edges.add((v, u)) # Add both directions for easier checking
            history.append({
                'msg': f"Ajout de ({u}, {v}) à l'ACM (Pas de cycle)",
                'mst_edges': mst_edges.copy(),
                'scanning': (u, v), # Keep highlighted as scanning/added
                'rejected': None
            })
        else:
            history.append({
                'msg': f"Rejet de ({u}, {v}) : Crée un cycle !",
                'mst_edges': mst_edges.copy(),
                'scanning': None,
                'rejected': (u, v)
            })
            
    history.append({
        'msg': "Terminé ! Arbre Couvrant Minimum construit.",
        'mst_edges': mst_edges.copy(),
        'scanning': None,
        'rejected': None
    })

    # --- Frame Generation ---
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(COLOR_BG)
    ax.set_facecolor(COLOR_BG)
    
    frames_data = []
    
    for i in range(len(history)):
        state = history[i]
        msg = state['msg']
        
        hold_frames = 10 # Faster for larger graph
        if "Ajout" in msg: hold_frames = 15
        if "Rejet" in msg: hold_frames = 15
        if "Terminé" in msg: hold_frames = 60
        
        for _ in range(hold_frames):
            frames_data.append(state)

    def draw_frame(state):
        ax.clear()
        
        mst_edges = state['mst_edges']
        scanning = state['scanning']
        rejected = state['rejected']
        msg = state['msg']

        # Draw Edges
        for u, v in G.edges():
            p1 = np.array(pos[u])
            p2 = np.array(pos[v])
            
            edge_color = COLOR_EDGE_EMPTY
            width = 2
            z = 1
            style = '-'
            
            # Check if edge is in MST (order-independent)
            if (u, v) in mst_edges or (v, u) in mst_edges:
                edge_color = COLOR_EDGE_MST
                width = 4
                z = 2
            
            # Overwrite if scanning or rejected
            if scanning == (u, v) or scanning == (v, u):
                edge_color = COLOR_SCANNING
                width = 5
                z = 3
            elif rejected == (u, v) or rejected == (v, u):
                edge_color = COLOR_EDGE_REJECTED
                width = 3
                z = 3
                style = '--'
            
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=edge_color, linewidth=width, zorder=z, linestyle=style)
            
            # Weight Label
            mid_p = (p1 + p2) / 2
            ax.text(mid_p[0], mid_p[1], str(G[u][v]['weight']), 
                    color=COLOR_TEXT, fontsize=10, fontweight='bold',
                    ha='center', va='center',
                    bbox=dict(facecolor=COLOR_BG, edgecolor='none', alpha=0.7, pad=1))

        # Draw Nodes
        for n, p in pos.items():
            fill_color = COLOR_NODE
            edge_color = COLOR_EDGE_EMPTY
            
            # Check if node is part of MST (connected to at least one MST edge)
            in_mst = False
            for u, v in mst_edges:
                if u == n or v == n:
                    in_mst = True
                    break
            
            if in_mst:
                fill_color = COLOR_EDGE_MST
                edge_color = '#ffffff'
            
            circle = patches.Circle(p, radius=0.2, facecolor=fill_color, edgecolor=edge_color, linewidth=2, zorder=4)
            ax.add_patch(circle)
            ax.text(p[0], p[1], n, color=COLOR_NODE_TEXT, fontsize=10, fontweight='bold', ha='center', va='center', zorder=5)

        ax.set_title(msg, color=COLOR_TEXT, fontsize=16, fontweight='bold', pad=20)
        ax.axis('off')
        ax.set_xlim(-0.5, 7)
        ax.set_ylim(0, 4)

    # --- Render Loop ---
    print(f"Generating {len(frames_data)} frames for Kruskal...")
    canvas = FigureCanvasAgg(fig)
    
    path_mp4 = os.path.join(output_dir, "kruskal.mp4")
    path_webm = os.path.join(output_dir, "kruskal.webm")
    
    writer_mp4 = imageio.get_writer(path_mp4, fps=10, codec='libx264', pixelformat='yuv420p')
    writer_webm = imageio.get_writer(path_webm, fps=10, codec='libvpx-vp9')
    
    for i, state in enumerate(frames_data):
        if i % 50 == 0: print(f"Rendering frame {i}/{len(frames_data)}")
        
        draw_frame(state)
        
        canvas.draw()
        buf = canvas.buffer_rgba()
        image = np.asarray(buf)
        image = image[:, :, :3] # RGB
        
        writer_mp4.append_data(image)
        writer_webm.append_data(image)

    writer_mp4.close()
    writer_webm.close()
    print("Done! Generated Kruskal videos.")

if __name__ == "__main__":
    create_videos_kruskal()
