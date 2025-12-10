import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches
import os
import heapq
import numpy as np
import imageio
from matplotlib.backends.backend_agg import FigureCanvasAgg

# Ensure output directory exists
output_dir = "docs/img"
os.makedirs(output_dir, exist_ok=True)

def create_videos_prim():
    # --- Configuration ---
    plt.style.use('dark_background')
    
    # Colors
    COLOR_BG = '#1e1e1e'
    COLOR_NODE = '#ffffff'
    COLOR_NODE_TEXT = '#000000'
    COLOR_EDGE_EMPTY = '#444444'
    COLOR_EDGE_MST = '#ff00ff' # Neon Magenta
    COLOR_EDGE_CANDIDATE = '#ffd700' # Gold
    COLOR_TEXT = '#ffffff'
    COLOR_VISITED = '#ff00ff'

    # Graph Setup (Same as Kruskal for consistency)
    G = nx.Graph()
    edges = [
        ('A', 'B', 4), ('B', 'C', 8), ('C', 'D', 7),
        ('E', 'F', 9), ('F', 'G', 2), ('G', 'H', 14),
        ('A', 'E', 8), ('B', 'F', 11), ('C', 'G', 4), ('D', 'H', 9),
        ('B', 'E', 1), ('C', 'F', 7), ('D', 'G', 6), ('C', 'H', 10)
    ]
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)

    pos = {
        'A': (0, 3), 'B': (2, 3), 'C': (4, 3), 'D': (6, 3),
        'E': (0, 1), 'F': (2, 1), 'G': (4, 1), 'H': (6, 1)
    }

    # --- Algorithm Execution ---
    history = []
    
    start_node = 'A'
    visited = {start_node}
    mst_edges = set()
    candidate_edges = [] # Priority Queue
    
    # Initial candidates from start node
    for v in G.neighbors(start_node):
        heapq.heappush(candidate_edges, (G[start_node][v]['weight'], start_node, v))
        
    history.append({
        'msg': f"Initialisation : Départ de {start_node}",
        'visited': visited.copy(),
        'mst_edges': mst_edges.copy(),
        'candidates': list(candidate_edges), # Snapshot for visualization
        'current_edge': None
    })
    
    while len(visited) < len(G.nodes()):
        # Find valid edge (one end in visited, one outside)
        while candidate_edges:
            w, u, v = heapq.heappop(candidate_edges)
            
            if v in visited:
                continue # Skip internal edges
            
            # Found the min edge
            history.append({
                'msg': f"Choix de l'arête ({u}, {v}) - Poids {w}",
                'visited': visited.copy(),
                'mst_edges': mst_edges.copy(),
                'candidates': list(candidate_edges) + [(w, u, v)], # Show it as candidate before adding
                'current_edge': (u, v)
            })
            
            visited.add(v)
            mst_edges.add((u, v))
            mst_edges.add((v, u))
            
            # Add new candidates
            for neighbor in G.neighbors(v):
                if neighbor not in visited:
                    heapq.heappush(candidate_edges, (G[v][neighbor]['weight'], v, neighbor))
            
            history.append({
                'msg': f"Ajout de {v} à l'arbre",
                'visited': visited.copy(),
                'mst_edges': mst_edges.copy(),
                'candidates': list(candidate_edges),
                'current_edge': None
            })
            break # Move to next step
            
    history.append({
        'msg': "Terminé ! Arbre Couvrant Minimum construit.",
        'visited': visited.copy(),
        'mst_edges': mst_edges.copy(),
        'candidates': [],
        'current_edge': None
    })

    # --- Frame Generation ---
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(COLOR_BG)
    ax.set_facecolor(COLOR_BG)
    
    frames_data = []
    
    for i in range(len(history)):
        state = history[i]
        msg = state['msg']
        
        hold_frames = 10
        if "Choix" in msg: hold_frames = 20
        if "Ajout" in msg: hold_frames = 15
        if "Terminé" in msg: hold_frames = 60
        
        for _ in range(hold_frames):
            frames_data.append(state)

    def draw_frame(state):
        ax.clear()
        
        visited = state['visited']
        mst_edges = state['mst_edges']
        candidates = state['candidates']
        current_edge = state['current_edge']
        msg = state['msg']
        
        candidate_set = set()
        for _, u, v in candidates:
            candidate_set.add((u, v))
            candidate_set.add((v, u))

        # Draw Edges
        for u, v in G.edges():
            p1 = np.array(pos[u])
            p2 = np.array(pos[v])
            
            edge_color = COLOR_EDGE_EMPTY
            width = 2
            z = 1
            
            if (u, v) in mst_edges or (v, u) in mst_edges:
                edge_color = COLOR_EDGE_MST
                width = 4
                z = 2
            elif (u, v) in candidate_set or (v, u) in candidate_set:
                edge_color = COLOR_EDGE_CANDIDATE
                width = 3
                z = 2
                
            if current_edge == (u, v) or current_edge == (v, u):
                edge_color = '#ffffff' # Flash white when chosen
                width = 5
                z = 3
            
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=edge_color, linewidth=width, zorder=z)
            
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
            
            if n in visited:
                fill_color = COLOR_VISITED
                edge_color = '#ffffff'
            
            circle = patches.Circle(p, radius=0.2, facecolor=fill_color, edgecolor=edge_color, linewidth=2, zorder=4)
            ax.add_patch(circle)
            ax.text(p[0], p[1], n, color=COLOR_NODE_TEXT, fontsize=10, fontweight='bold', ha='center', va='center', zorder=5)

        ax.set_title(msg, color=COLOR_TEXT, fontsize=16, fontweight='bold', pad=20)
        ax.axis('off')
        ax.set_xlim(-0.5, 7)
        ax.set_ylim(0, 4)

    # --- Render Loop ---
    print(f"Generating {len(frames_data)} frames for Prim...")
    canvas = FigureCanvasAgg(fig)
    
    path_mp4 = os.path.join(output_dir, "prim.mp4")
    path_webm = os.path.join(output_dir, "prim.webm")
    
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
    print("Done! Generated Prim videos.")

if __name__ == "__main__":
    create_videos_prim()
