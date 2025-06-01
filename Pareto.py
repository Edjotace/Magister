# -*- coding: utf-8 -*-
"""
Created on Sun Jun  1 15:26:53 2025

@author: edjca
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jun  1 15:12:27 2025
Modified on Sun Jun  1 15:XX:XX 2025

@author: edjca (modified by AI)
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

# Asumiendo que tu DataFrame 'df' ya está cargado.
# --- INICIO: Datos de ejemplo (reemplaza esto con tu DataFrame 'df') ---
data = {
    'Deck': ['Dragapult', 'Raging Bolt', 'Gardevoir', 'Gholdengo', 'Joltik Box', 'Tera Box',
             'N\'s Zoroark', 'Archaludon', 'Flareon', 'Charizard', 'Terapagos Noctowl',
             'Hop\'s Zacian', 'Roaring Moon', 'Ancient Box', 'Milotic', 'Ceruledge',
             'Blissey', 'Feraligatr', 'Froslass Munkidori', 'Hydreigon', 'Other',
             'Hydrapple', 'Mamoswine', 'Slowking', 'Chien-Pao Baxcalibur', 'Future Box',
             'Great Tusk Mill', 'Iono\'s Bellibolt', 'Iron Thorns', 'Copperajah', 'Dipplin',
             'Greninja', 'Future Hands', 'Okidogi', 'Tinkaton', 'Tyrranitar'],
    'Dia 1': [266, 201, 174, 118, 117, 80, 47, 39, 31, 30, 21, 17, 14, 13, 10, 8, 7, 7, 5, 5, 5,
              3, 3, 3, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1]
}
df = pd.DataFrame(data)
# --- FIN: Datos de ejemplo ---

# 1. Ordenar los datos de mayor a menor frecuencia
df_sorted = df.sort_values(by='Dia 1', ascending=False).copy() # Usar .copy() para evitar SettingWithCopyWarning

# 2. Calcular el porcentaje individual
total_day1 = df_sorted['Dia 1'].sum()
df_sorted['Porcentaje Individual Dia 1'] = (df_sorted['Dia 1'] / total_day1) * 100

# 3. Calcular Porcentaje Acumulado Descendente
# Corrected calculation for cumulative sum descending for percentage
df_sorted['Porcentaje Acumulado Descendente Dia 1'] = df_sorted['Porcentaje Individual Dia 1'][::-1].cumsum()[::-1]


# --- INICIO: Cálculo de Frecuencias Teóricas para Alfas Fijos ---

# 4. Añadir Rango
# El rango es simplemente la posición después de ordenar por frecuencia
df_sorted['Rank'] = np.arange(1, len(df_sorted) + 1)

# 5. Definir Alfas
alpha_1 = 0.71 # Caso "80/20" (según indicación del usuario)
alpha_2 = 1.96 # Otro caso solicitado

# 6. Calcular Frecuencia Teórica para alpha_1
C1_adj = df_sorted['Dia 1'].iloc[0]  # La frecuencia más alta
df_sorted[f'Frecuencia Teórica Ajustada Alpha {alpha_1:.3f}'] = C1_adj * (df_sorted['Rank'] ** (-alpha_1))
print(f"\nConstante C ajustada para Alpha {alpha_1:.3f} (Rank 1 ajustado): {C1_adj:.3f}")

C2_adj = df_sorted['Dia 1'].iloc[0]  # Mismo ajuste para alpha_2
df_sorted[f'Frecuencia Teórica Ajustada Alpha {alpha_2:.3f}'] = C2_adj * (df_sorted['Rank'] ** (-alpha_2))
print(f"Constante C ajustada para Alpha {alpha_2:.3f} (Rank 1 ajustado): {C2_adj:.3f}")

# --- FIN: Cálculo de Frecuencias Teóricas Ajustadas ---


# Graficar
fig, ax1 = plt.subplots(figsize=(18, 9))  # Tamaño para mejor visualización

color_bars = 'tab:blue'
ax1.set_xlabel('Deck (Ordenado por Frecuencia)')
ax1.set_ylabel('Número de Jugadores (Dia 1)', color=color_bars)
ax1.bar(df_sorted['Deck'], df_sorted['Dia 1'], color=color_bars, alpha=0.6, label='Jugadores Dia 1 (Observado)')
ax1.tick_params(axis='y', labelcolor=color_bars)
ax1.tick_params(axis='x', rotation=90, labelsize=8)

# Graficar las líneas de frecuencia teórica ajustada
ax1.plot(df_sorted['Deck'], df_sorted[f'Frecuencia Teórica Ajustada Alpha {alpha_1:.3f}'], color='red', marker='.', linestyle='--',
         linewidth=2, label=f'Frecuencia Teórica Ajustada (α={alpha_1:.3f})')
ax1.plot(df_sorted['Deck'], df_sorted[f'Frecuencia Teórica Ajustada Alpha {alpha_2:.3f}'], color='purple', marker='x', linestyle=':',
         linewidth=2, label=f'Frecuencia Teórica Ajustada (α={alpha_2:.3f})')

# Eje secundario para porcentaje acumulado
ax2 = ax1.twinx()
color_line_acum = 'tab:green'
ax2.set_ylabel('Porcentaje Acumulado Descendente', color=color_line_acum)
ax2.plot(df_sorted['Deck'], df_sorted['Porcentaje Acumulado Descendente Dia 1'], color=color_line_acum, marker='o', linestyle='-', linewidth=2, label='Porcentaje Acumulado Descendente')
ax2.tick_params(axis='y', labelcolor=color_line_acum)
ax2.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100.0))
ax2.set_ylim(0, 105)

plt.title('Diagrama Pareto con Ajustes Teóricos de Ley de Potencias (Dia 1)', fontsize=16)
fig.tight_layout()

# Leyendas combinadas
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper right', fontsize=10)

plt.grid(True, linestyle='--', alpha=0.7)
plt.show()