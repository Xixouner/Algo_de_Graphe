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

def create_videos_dijkstra():
    # --- Configuration ---
    plt.style.use('dark_background')
    
    # Colors
    COLOR_BG = '#1e1e1e'
    COLOR_NODE = '#ffffff'
    COLOR_NODE_TEXT = '#000000'
    COLOR_EDGE_EMPTY = '#444444'
    COLOR_EDGE_PATH = '#00ccff' # Neon Cyan
    COLOR_HIGHLIGHT = '#ff00ff' # Neon Magenta
    COLOR_TEXT = '#ffffff'
    
    # Dijkstra Colors
    COLOR_CURRENT = '#ffd700' # Gold
    COLOR_VISITED = '#32cd32' # Lime Green
    COLOR_SCANNING = '#ffa500' # Orange
    COLOR_INF = '#888888' # Gray for infinity

    # Graph Setup
    G = nx.DiGraph()
    # Graph designed to show updates: S->A is 4, but S->B->A is 2+1=3
    edges = [
        ('S', 'A', 4), ('S', 'B', 2),
        ('B', 'A', 1), ('B', 'C', 5), ('B', 'D', 8),
        ('A', 'C', 2),
        ('C', 'E', 3), ('C', 'T', 6),
        ('D', 'E', 1),
        ('E', 'T', 2)
    ]
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)

    pos = {
        'S': (0, 2),
        'A': (2, 3), 'B': (2, 1),
        'C': (4, 3), 'D': (4, 1),
        'E': (5, 2),
        'T': (7, 2)
    }

    # --- Algorithm Execution (Pre-calculation) ---
    history = [] 
    
    # Initial State
    distances = {node: float('inf') for node in G.nodes()}
    distances['S'] = 0
    predecessors = {node: None for node in G.nodes()}
    pq = [(0, 'S')] # Priority Queue
    visited = set()
    
    history.append({
        'msg': "Initialisation : Dist(S)=0, autres=∞",
        'distances': distances.copy(),
        'visited': visited.copy(),
        'current': None,
        'scanning': None,
        'path_edges': []
    })
    
    while pq:
        current_dist, u = heapq.heappop(pq)
        
        # If we found a shorter path to u before, skip this stale entry
        if u in visited:
            continue
            
        history.append({
            'msg': f"Exploration de {u} (Dist min = {current_dist})",
            'distances': distances.copy(),
            'visited': visited.copy(),
            'current': u,
            'scanning': None,
            'path_edges': []
        })
        
        visited.add(u)
        
        if u == 'T':
            history.append({
                'msg': "Destination T atteinte !",
                'distances': distances.copy(),
                'visited': visited.copy(),
                'current': u,
                'scanning': None,
                'path_edges': []
            })
            break
            
        for v in G.neighbors(u):
            weight = G[u][v]['weight']
            new_dist = current_dist + weight
            
            history.append({
                'msg': f"Vérification {u}->{v} (Coût {weight})",
                'distances': distances.copy(),
                'visited': visited.copy(),
                'current': u,
                'scanning': (u, v),
                'path_edges': []
            })
            
            if new_dist < distances[v]:
                old_dist = distances[v]
                distances[v] = new_dist
                predecessors[v] = u
                heapq.heappush(pq, (new_dist, v))
                
                msg_update = f"Mise à jour {v} : {old_dist} -> {new_dist}" if old_dist != float('inf') else f"Découverte {v} : Dist = {new_dist}"
                history.append({
                    'msg': msg_update,
                    'distances': distances.copy(),
                    'visited': visited.copy(),
                    'current': u,
                    'scanning': (u, v),
                    'path_edges': []
                })

    # Reconstruct Path
    path = []
    curr = 'T'
    while curr is not None:
        path.append(curr)
        curr = predecessors[curr]
    path.reverse()
    
    path_edges = list(zip(path, path[1:]))
    
    history.append({
        'msg': f"Terminé ! Plus court chemin : {distances['T']}",
        'distances': distances.copy(),
        'visited': visited.copy(),
        'current': None,
        'scanning': None,
        'path_edges': path_edges
    })

    # --- Frame Generation ---
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(COLOR_BG)
    ax.set_facecolor(COLOR_BG)
    
    FRAMES_PER_TRANSITION = 20
    frames_data = []
    
    for i in range(len(history)):
        state = history[i]
        msg = state['msg']
        
        # Determine hold time based on action
        hold_frames = 10
        if "Exploration" in msg: hold_frames = 20
        if "Mise à jour" in msg or "Découverte" in msg: hold_frames = 25
        if "Terminé" in msg: hold_frames = 60
        
        for _ in range(hold_frames):
            frames_data.append(state)

    def draw_frame(state):
        ax.clear()
        
        distances = state['distances']
        visited = state['visited']
        current = state['current']
        scanning = state['scanning']
        final_path_edges = state['path_edges']
        msg = state['msg']

        # Draw Edges
        for u, v in G.edges():
            p1 = np.array(pos[u])
            p2 = np.array(pos[v])
            vec = p2 - p1
            dist = np.linalg.norm(vec)
            
            radius = 0.3
            if dist > 2 * radius:
                start_p = p1 + vec * (radius / dist)
                end_p = p2 - vec * (radius / dist)
            else:
                start_p = p1
                end_p = p2
            
            edge_color = COLOR_EDGE_EMPTY
            width = 2
            z = 1
            
            if scanning == (u, v):
                edge_color = COLOR_SCANNING
                width = 4
                z = 3
            elif (u, v) in final_path_edges:
                edge_color = COLOR_HIGHLIGHT
                width = 4
                z = 3
            
            arrow = patches.FancyArrowPatch(start_p, end_p, arrowstyle='-|>', 
                                            mutation_scale=20, color=edge_color, 
                                            linewidth=width, zorder=z)
            ax.add_patch(arrow)
            
            # Weight Label
            mid_p = (p1 + p2) / 2
            label_offset = 0.15
            dx, dy = vec[0], vec[1]
            if dist > 0:
                ox, oy = -dy/dist * label_offset, dx/dist * label_offset
            else:
                ox, oy = 0, 0
                
            ax.text(mid_p[0] + ox, mid_p[1] + oy, str(G[u][v]['weight']), 
                    color=COLOR_TEXT, fontsize=9, fontweight='bold',
                    ha='center', va='center',
                    bbox=dict(facecolor=COLOR_BG, edgecolor='none', alpha=0.7, pad=0))

        # Draw Nodes
        for n, p in pos.items():
            fill_color = COLOR_NODE
            edge_color = COLOR_EDGE_EMPTY
            
            if n in visited:
                fill_color = COLOR_VISITED
            if n == current:
                fill_color = COLOR_CURRENT
                edge_color = '#ffffff'
            
            circle = patches.Circle(p, radius=0.3, facecolor=fill_color, edgecolor=edge_color, linewidth=2, zorder=4)
            ax.add_patch(circle)
            
            # Node Name
            ax.text(p[0], p[1]+0.05, n, color=COLOR_NODE_TEXT, fontsize=12, fontweight='bold', ha='center', va='center', zorder=5)
            
            # Distance Label
            d = distances[n]
            d_str = "∞" if d == float('inf') else str(d)
            ax.text(p[0], p[1]-0.1, d_str, color=COLOR_NODE_TEXT, fontsize=10, ha='center', va='center', zorder=5)

        ax.set_title(msg, color=COLOR_TEXT, fontsize=16, fontweight='bold', pad=20)
        ax.axis('off')
        ax.set_xlim(-0.5, 8)
        ax.set_ylim(0, 4)

    # --- Render Loop ---
    print(f"Generating {len(frames_data)} frames...")
    canvas = FigureCanvasAgg(fig)
    
    path_mp4 = os.path.join(output_dir, "dijkstra.mp4")
    path_webm = os.path.join(output_dir, "dijkstra.webm")
    
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
    print("Done! Generated both MP4 and WebM.")

if __name__ == "__main__":
    create_videos_dijkstra()
