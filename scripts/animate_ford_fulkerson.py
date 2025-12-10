import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches
import os
import collections
import numpy as np
import imageio
from matplotlib.backends.backend_agg import FigureCanvasAgg

# Ensure output directory exists
output_dir = "docs/img"
os.makedirs(output_dir, exist_ok=True)

def create_videos_ford_fulkerson():
    # --- Configuration ---
    plt.style.use('dark_background')
    
    # Colors
    COLOR_BG = '#1e1e1e'
    COLOR_NODE = '#ffffff'
    COLOR_NODE_TEXT = '#000000'
    COLOR_EDGE_EMPTY = '#444444'
    COLOR_EDGE_FULL = '#00ccff' # Neon Cyan
    COLOR_EDGE_SATURATED = '#ff4444' # Red for saturated
    COLOR_HIGHLIGHT = '#ff00ff' # Neon Magenta
    COLOR_TEXT = '#ffffff'
    
    # BFS Colors
    COLOR_CURRENT = '#ffd700' # Gold
    COLOR_VISITED = '#32cd32' # Lime Green
    COLOR_SCANNING = '#ffa500' # Orange
    
    # Graph Setup
    G = nx.DiGraph()
    edges = [
        ('S', 'A', 10), ('S', 'B', 10),
        ('A', 'B', 2), ('A', 'C', 4), ('A', 'D', 8),
        ('B', 'D', 9),
        ('C', 'T', 10),
        ('D', 'C', 6), ('D', 'T', 10)
    ]
    for u, v, c in edges:
        G.add_edge(u, v, capacity=c, flow=0)

    pos = {
        'S': (0.5, 2),
        'A': (2, 3), 'B': (2, 1),
        'C': (4, 3), 'D': (4, 1),
        'T': (5.5, 2)
    }

    # --- Algorithm Execution (Pre-calculation) ---
    history = [] 
    
    # Initial State
    history.append((G.copy(), "Initialisation du réseau", [], {}))
    
    max_flow = 0
    while True:
        # BFS (Edmonds-Karp)
        parent = {'S': 'S'}
        queue = collections.deque(['S'])
        path_found = False
        
        history.append((G.copy(), "Début de la recherche (BFS)", [], {'visited': set(parent.keys())}))

        while queue:
            u = queue.popleft()
            
            history.append((G.copy(), f"Exploration du sommet {u}", [], 
                            {'visited': set(parent.keys()), 'current': u}))

            if u == 'T':
                path_found = True
                break
            
            for v in G.nodes():
                if G.has_edge(u, v):
                    history.append((G.copy(), f"Vérification arc {u}->{v}", [], 
                                    {'visited': set(parent.keys()), 'current': u, 'scanning': (u, v)}))
                    
                    if v not in parent:
                        cap = G[u][v]['capacity']
                        flow = G[u][v]['flow']
                        if cap - flow > 0:
                            parent[v] = u
                            queue.append(v)
                            history.append((G.copy(), f"Ajout de {v} à la file (Cap. résiduelle > 0)", [], 
                                            {'visited': set(parent.keys()), 'current': u, 'scanning': (u, v)}))
                        else:
                            history.append((G.copy(), f"Arc {u}->{v} saturé ou bloqué", [], 
                                            {'visited': set(parent.keys()), 'current': u, 'scanning': (u, v)}))
        
        if not path_found:
            history.append((G.copy(), "Aucun chemin vers T trouvé.", [], {'visited': set(parent.keys())}))
            break

        # Reconstruct path
        path = []
        curr = 'T'
        while curr != 'S':
            path.append(curr)
            curr = parent[curr]
        path.append('S')
        path.reverse()
        
        # Calculate bottleneck
        path_flow = float('inf')
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            path_flow = min(path_flow, G[u][v]['capacity'] - G[u][v]['flow'])
            
        history.append((G.copy(), f"Chemin trouvé ! Augmentation de {path_flow}", path, {}))
        
        # Update flow
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            G[u][v]['flow'] += path_flow
            
        max_flow += path_flow
        
        history.append((G.copy(), f"Nouveau Flot Total: {max_flow}", [], {}))

    history.append((G.copy(), f"Terminé. Flot Max = {max_flow}", [], {}))

    # --- Frame Generation ---
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(COLOR_BG)
    ax.set_facecolor(COLOR_BG)
    
    FRAMES_PER_TRANSITION = 30 
    frames_data = []
    
    for i in range(len(history) - 1):
        start_G, msg, path, visuals = history[i]
        end_G, next_msg, next_path, next_visuals = history[i+1]
        
        is_flow_update = False
        for u, v in start_G.edges():
            if start_G[u][v]['flow'] != end_G[u][v]['flow']:
                is_flow_update = True
                break
        
        if is_flow_update:
            for f in range(FRAMES_PER_TRANSITION + 1):
                progress = f / FRAMES_PER_TRANSITION
                frames_data.append({
                    'start_G': start_G, 'end_G': end_G,
                    'path': path, 'msg': next_msg if progress > 0.5 else msg,
                    'progress': progress, 'is_transition': True,
                    'visuals': visuals
                })
        else:
            hold_frames = 10
            if "Exploration" in msg: hold_frames = 20
            if "Chemin trouvé" in msg: hold_frames = 40
            if "Ajout" in msg: hold_frames = 25
            if "saturé" in msg: hold_frames = 15
            
            for _ in range(hold_frames):
                frames_data.append({
                    'G': start_G, 'path': path, 'msg': msg,
                    'progress': 0.0, 'is_transition': False,
                    'visuals': visuals
                })

    final_G, final_msg, final_path, final_visuals = history[-1]
    for _ in range(60):
        frames_data.append({
            'G': final_G, 'path': final_path, 'msg': final_msg,
            'progress': 1.0, 'is_transition': False,
            'visuals': final_visuals
        })

    def draw_frame(frame_data):
        ax.clear()
        
        if frame_data['is_transition']:
            G_curr = frame_data['start_G']
            G_next = frame_data['end_G']
            progress = frame_data['progress']
            current_flows = {}
            for u, v in G_curr.edges():
                f_start = G_curr[u][v]['flow']
                f_end = G_next[u][v]['flow']
                current_flows[(u,v)] = f_start + (f_end - f_start) * progress
        else:
            G_curr = frame_data['G']
            current_flows = {(u,v): d['flow'] for u, v, d in G_curr.edges(data=True)}
            
        path = frame_data['path']
        msg = frame_data['msg']
        visuals = frame_data['visuals']
        
        visited = visuals.get('visited', set())
        current_node = visuals.get('current', None)
        scanning_edge = visuals.get('scanning', None)

        for u, v in G_curr.edges():
            cap = G_curr[u][v]['capacity']
            flow = current_flows[(u,v)]
            
            p1 = np.array(pos[u])
            p2 = np.array(pos[v])
            vec = p2 - p1
            dist = np.linalg.norm(vec)
            
            radius = 0.25
            if dist > 2 * radius:
                start_p = p1 + vec * (radius / dist)
                end_p = p2 - vec * (radius / dist)
            else:
                start_p = p1
                end_p = p2
            
            edge_color = COLOR_EDGE_EMPTY
            width = 2
            
            if scanning_edge == (u, v):
                edge_color = COLOR_SCANNING
                width = 4
            
            arrow = patches.FancyArrowPatch(start_p, end_p, arrowstyle='-|>', 
                                            mutation_scale=20, color=edge_color, 
                                            linewidth=width, zorder=1)
            ax.add_patch(arrow)
            
            if flow > 0:
                flow_width = 2 + (flow / cap) * 4 if cap > 0 else 2
                is_saturated = abs(flow - cap) < 0.1
                flow_color = COLOR_EDGE_SATURATED if is_saturated else COLOR_EDGE_FULL
                
                flow_arrow = patches.FancyArrowPatch(start_p, end_p, arrowstyle='-|>', 
                                                     mutation_scale=20, color=flow_color, 
                                                     linewidth=flow_width, zorder=2, alpha=0.8)
                ax.add_patch(flow_arrow)
            
            if path:
                path_edges = list(zip(path, path[1:]))
                if (u, v) in path_edges:
                    highlight_arrow = patches.FancyArrowPatch(start_p, end_p, arrowstyle='-|>', 
                                                              mutation_scale=20, color=COLOR_HIGHLIGHT, 
                                                              linewidth=3, zorder=3, linestyle='--')
                    ax.add_patch(highlight_arrow)

            mid_p = (p1 + p2) / 2
            
            label_offset = 0.15
            dx = vec[0]
            dy = vec[1]
            if dist > 0:
                ox, oy = -dy/dist * label_offset, dx/dist * label_offset
            else:
                ox, oy = 0, 0
                
            txt = f"{int(flow)}/{cap}"
            ax.text(mid_p[0] + ox, mid_p[1] + oy, txt, color=COLOR_TEXT, fontsize=8, 
                    ha='center', va='center', fontweight='bold',
                    bbox=dict(facecolor=COLOR_BG, edgecolor='none', alpha=0.7, pad=0))

        for n, p in pos.items():
            fill_color = COLOR_NODE
            edge_color = COLOR_EDGE_FULL
            
            if n in visited:
                fill_color = COLOR_VISITED
            if n == current_node:
                fill_color = COLOR_CURRENT
                edge_color = '#ffffff'
            
            circle = patches.Circle(p, radius=0.25, facecolor=fill_color, edgecolor=edge_color, linewidth=2, zorder=4)
            ax.add_patch(circle)
            ax.text(p[0], p[1], n, color=COLOR_NODE_TEXT, fontsize=12, fontweight='bold', ha='center', va='center', zorder=5)

        ax.set_title(msg, color=COLOR_TEXT, fontsize=16, fontweight='bold', pad=20)
        ax.axis('off')
        ax.set_xlim(-0.5, 6)
        ax.set_ylim(0, 4)
        
        return fig

    # --- Render Loop ---
    print(f"Generating {len(frames_data)} frames...")
    canvas = FigureCanvasAgg(fig)
    
    # We will generate frames once and write to both writers
    path_mp4 = os.path.join(output_dir, "ford_fulkerson.mp4")
    path_webm = os.path.join(output_dir, "ford_fulkerson.webm")
    
    writer_mp4 = imageio.get_writer(path_mp4, fps=10, codec='libx264', pixelformat='yuv420p')
    writer_webm = imageio.get_writer(path_webm, fps=10, codec='libvpx-vp9')
    
    for i, frame_data in enumerate(frames_data):
        if i % 100 == 0: print(f"Rendering frame {i}/{len(frames_data)}")
        
        draw_frame(frame_data)
        
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
    create_videos_ford_fulkerson()
