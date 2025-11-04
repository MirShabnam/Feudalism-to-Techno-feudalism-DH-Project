#!/usr/bin/env python3
import os
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

HERE = os.path.dirname(__file__)
CFILE = os.path.join(HERE, '..', 'data', 'feud_techno_concepts.csv')
EFILE = os.path.join(HERE, '..', 'data', 'feud_techno_events.csv')
OUT   = os.path.join(HERE, '..', 'output')
os.makedirs(OUT, exist_ok=True)

concepts = pd.read_csv(CFILE)
events = pd.read_csv(EFILE)

# --- Bar charts for concept scores
ax = concepts.set_index('concept')[['feudalism_score','technofeudalism_score']].plot(kind='bar', title='Concept Scores: Feudalism vs Technofeudalism')
ax.set_xlabel('Concept'); ax.set_ylabel('Relative Score'); fig=ax.get_figure(); fig.tight_layout()
fig.savefig(os.path.join(OUT, 'concept_scores_comparison.png')); plt.close(fig)

# --- Difference plot (techno - feudal)
concepts['delta'] = concepts['technofeudalism_score'] - concepts['feudalism_score']
ax = concepts.set_index('concept')['delta'].plot(kind='bar', title='Shift (Technofeudalism − Feudalism)')
ax.set_xlabel('Concept'); ax.set_ylabel('Delta'); fig=ax.get_figure(); fig.tight_layout()
fig.savefig(os.path.join(OUT, 'concept_shift_delta.png')); plt.close(fig)

# --- Timeline of intensity (simple)
events_sorted = events.sort_values('year')
ax = events_sorted.set_index('year')['intensity'].plot(kind='line', title='Timeline Intensity')
ax.set_xlabel('Year'); ax.set_ylabel('Intensity (0-1)'); fig=ax.get_figure(); fig.tight_layout()
fig.savefig(os.path.join(OUT, 'timeline_intensity.png')); plt.close(fig)

# --- Era composition (avg intensity)
comp = events.groupby('era')['intensity'].mean()
ax = comp.plot(kind='bar', title='Average Intensity by Era')
ax.set_xlabel('Era'); ax.set_ylabel('Avg Intensity'); fig=ax.get_figure(); fig.tight_layout()
fig.savefig(os.path.join(OUT, 'avg_intensity_by_era.png')); plt.close(fig)

# --- Concept network (era-to-concept edges weighted by score)
G = nx.Graph()
for _, row in concepts.iterrows():
    c = row['concept']
    fs = row['feudalism_score']
    ts = row['technofeudalism_score']
    for era, w in [('Feudalism', fs), ('Technofeudalism', ts)]:
        if w <= 0: 
            continue
        G.add_node(era)
        G.add_node(c)
        if G.has_edge(era, c):
            G[era][c]['weight'] += w
        else:
            G.add_edge(era, c, weight=w)

pos = nx.spring_layout(G, seed=3)
plt.figure()
nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_edges(G, pos, width=[G[u][v]['weight']/20 for u,v in G.edges()])
nx.draw_networkx_labels(G, pos, font_size=8)
plt.axis('off'); plt.tight_layout()
plt.savefig(os.path.join(OUT, 'era_concept_network.png')); plt.close()

# --- Export merged comparison table
concepts.to_csv(os.path.join(OUT, 'concepts_with_delta.csv'), index=False)
events_sorted.to_csv(os.path.join(OUT, 'events_sorted.csv'), index=False)
print("Analysis complete. Outputs written to output/.")
