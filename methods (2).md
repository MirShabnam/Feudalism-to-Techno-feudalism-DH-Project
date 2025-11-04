# Methods

**Datasets**
- `marx_events.csv` — synthetic, curated demo of actions vs publications with intensity (0–1)
- `marx_concepts.csv` — relative frequencies of key concepts in Marx vs Post‑Marx eras

**Processing & Visualisation**
- Timeline of intensity (line)
- Average intensity by type (bar)
- Events per decade, split by action/publication (grouped bar)
- Concept frequency per era and concept shift (bars)
- Era–concept association network (NetworkX)

**Reproducibility**
- Pure Python + matplotlib + networkx
- All charts saved in `output/`
