#!/usr/bin/env python3
"""Generate visuals from data for the TechnoFeudalism DH project."""

import pandas as pd
import matplotlib.pyplot as plt

scores = pd.read_csv('data/intensity_scores.csv')

# Grouped bars
plt.figure(figsize=(12,6))
x = range(len(scores))
plt.bar([i - 0.2 for i in x], scores['Feudal_Intensity'], width=0.4, label='Feudalism')
plt.bar([i + 0.2 for i in x], scores['TechnoFeudal_Intensity'], width=0.4, label='Techno-feudalism')
plt.xticks(list(x), scores['Aspect'], rotation=35, ha='right')
plt.ylabel('Conceptual Intensity (0–10)')
plt.title('Feudalism vs. Techno-feudalism — Conceptual Intensity by Aspect')
plt.legend()
plt.tight_layout()
plt.savefig('visuals/intensity_grouped_bars.png', dpi=200)
plt.close()

print('Charts regenerated in visuals/.')
