# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import numpy as np
from PIL import Image

# --- CONFIGURAÇÃO GERAL ---
fps = 30
circle_radius = 0.04
circle_positions = [
    (0.9, 0.45), (0.81, 0.53), (0.9, 0.61), (0.81, 0.69), (0.65, 0.69),
]
connections = [(0, 1), (1, 2), (2, 3), (3, 4)]
texto_logo = "PEXP"

cores = {
    'original': {'fundo': 'black', 'logo': 'white'},
    'azul_branco': {'fundo': 'white', 'logo': '#007BFF'},
    'azul_transparente': {'fundo': 'transparent', 'logo': '#007BFF'},
    'laranja_branco': {'fundo': 'white', 'logo': '#FF6600'},
    'laranja_transparente': {'fundo': 'transparent', 'logo': '#FF6600'},
    'neon': {'fundo': 'black', 'logo': '#39FF14'}
}

# --- TIMINGS DA ANIMAÇÃO ---
velocidade = 0.1204 / 0.4
circle_draw_duration = (2 * np.pi * circle_radius) / velocidade
line4_draw_duration = 0.228 / velocidade
line_draw_duration_default = 0.4
final_extra_delay = 2.0

circle_start_times = [circle_draw_duration * i for i in range(5)]
last_circle_end = circle_start_times[-1] + circle_draw_duration
line_start_times = [last_circle_end + line_draw_duration_default * i for i in range(3)]
line_start_times.append(line_start_times[-1] + line_draw_duration_default)
line_draw_durations = [line_draw_duration_default] * 3 + [line4_draw_duration]
fill_start_base = line_start_times[-1] + line_draw_durations[-1] + 0.2
fill_start_times = [fill_start_base + i * 0.4 for i in range(4)]
circle5_flicker_start = fill_start_times[-1] + 0.4
line4_retract_start = circle5_flicker_start + 0.6
thicken_start = line4_retract_start + line4_draw_duration + 0.5
text_start = thicken_start + 0.5
duration = text_start + final_extra_delay
frames = int(duration * fps)

# --- ANIMAÇÃO ---
fig, ax = plt.subplots(figsize=(8, 8), dpi=128)
ax.set_facecolor("black")
fig.patch.set_facecolor("black")
plt.axis('off')
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

circle_objs = [patches.Circle(pos, 0.0, edgecolor='white', facecolor='none', lw=2.5) for pos in circle_positions]
for c in circle_objs:
    ax.add_patch(c)
line_objs = [None] * len(connections)
text_obj = ax.text(0.76, 0.46, "", fontsize=110, color="white", fontweight='bold', ha='right', alpha=0)
filled = [False] * 5
flicker_times = [0.0, 0.1, 0.2, 0.4, 0.6]

def animate(i):
    t = i / fps
    # Crescer círculos
    for idx, circle in enumerate(circle_objs):
        start = circle_start_times[idx]
        if start <= t < start + circle_draw_duration:
            p = (t - start) / circle_draw_duration
            circle.set_radius(p * circle_radius)
        elif t >= start + circle_draw_duration:
            circle.set_radius(circle_radius)
    # Linhas
    for j, (a, b) in enumerate(connections):
        start = line_start_times[j]
        duration = line_draw_durations[j]
        x0, y0 = circle_positions[a]
        x1, y1 = circle_positions[b]
        dx, dy = x1 - x0, y1 - y0
        dist = np.hypot(dx, dy)
        ux, uy = dx / dist, dy / dist
        sx0, sy0 = x0 + ux * circle_radius, y0 + uy * circle_radius
        ex1, ey1 = (x1 - ux * circle_radius, y1 - uy * circle_radius) if j < 3 else (x1, y1)
        if t >= start:
            p = min((t - start) / duration, 1)
            new_x = sx0 + (ex1 - sx0) * p
            new_y = sy0 + (ey1 - sy0) * p
            if line_objs[j] is None:
                line, = ax.plot([sx0, new_x], [sy0, new_y], color='white', lw=2.5)
                line_objs[j] = line
            else:
                line_objs[j].set_data([sx0, new_x], [sy0, new_y])
    # Preencher primeiros círculos
    for idx in range(4):
        if not filled[idx] and t >= fill_start_times[idx]:
            circle_objs[idx].set_facecolor("white")
            filled[idx] = True
    # Piscar último círculo
    if circle5_flicker_start <= t < circle5_flicker_start + flicker_times[-1]:
        step = sum(t - circle5_flicker_start >= ft for ft in flicker_times)
        circle_objs[4].set_visible(step % 2 == 0)
    elif t >= circle5_flicker_start + flicker_times[-1]:
        circle_objs[4].set_visible(False)
    # Retrair última linha
    if t >= line4_retract_start:
        idx = 3
        x0, y0 = circle_positions[connections[idx][0]]
        x1, y1 = circle_positions[connections[idx][1]]
        dx, dy = x1 - x0, y1 - y0
        dist = np.hypot(dx, dy)
        ux, uy = dx / dist, dy / dist
        sx0, sy0 = x0 + ux * circle_radius, y0 + uy * circle_radius
        p = max(1 - (t - line4_retract_start) / line4_draw_duration, 0)
        new_x = sx0 + (x1 - sx0) * p
        new_y = sy0 + (y1 - sy0) * p
        if line_objs[idx] is not None:
            line_objs[idx].set_data([sx0, new_x], [sy0, new_y])
    # Engrossar primeiras linhas
    if t >= thicken_start:
        for l in line_objs[:3]:
            if l is not None:
                l.set_linewidth(8)
    # Mostrar texto
    if t >= text_start:
        text_obj.set_text(texto_logo)
        text_obj.set_alpha(min((t - text_start), 1))
    return circle_objs + [l for l in line_objs if l is not None] + [text_obj]

print("🎞️ A gerar animação...")
ani = animation.FuncAnimation(fig, animate, frames=frames, interval=1000/fps, blit=True)
ani.save("pexp_logo.mp4", writer="ffmpeg", fps=fps)
ani.save("pexp_logo.gif", writer="pillow", fps=fps)
plt.close(fig)
print("✅ Guardado: pexp_logo.mp4, pexp_logo.gif")

# --- FUNÇÕES PARA GERAR LOGOS ---
def criar_logo_com_texto(cor_logo='white', fundo='black'):
    fig, ax = plt.subplots(figsize=(8, 8), dpi=128)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_facecolor(fundo if fundo != 'transparent' else 'none')
    fig.patch.set_facecolor(fundo if fundo != 'transparent' else 'none')
    plt.axis('off')
    for idx, pos in enumerate(circle_positions[:-1]):
        circ = patches.Circle(pos, circle_radius, edgecolor=cor_logo, facecolor=cor_logo, lw=2.5)
        ax.add_patch(circ)
    for (a, b) in connections[:3]:
        x0, y0 = circle_positions[a]
        x1, y1 = circle_positions[b]
        ax.plot([x0, x1], [y0, y1], color=cor_logo, lw=8)
    ax.text(0.76, 0.46, texto_logo, fontsize=110, color=cor_logo, fontweight='bold', ha='right')
    return fig

def criar_chain_apenas(cor_logo='white', fundo='black'):
    fig, ax = plt.subplots(figsize=(8, 8), dpi=128)
    # Calcular limites automaticamente para centrar
    xs = [p[0] for p in circle_positions[:-1]]
    ys = [p[1] for p in circle_positions[:-1]]
    margin = 0.08  # margem extra para não cortar
    x_min, x_max = min(xs)-margin, max(xs)+margin
    y_min, y_max = min(ys)-margin, max(ys)+margin

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_facecolor(fundo if fundo != 'transparent' else 'none')
    fig.patch.set_facecolor(fundo if fundo != 'transparent' else 'none')
    plt.axis('off')
    # círculos
    for idx, pos in enumerate(circle_positions[:-1]):
        circ = patches.Circle(pos, circle_radius, edgecolor=cor_logo, facecolor=cor_logo, lw=2.5)
        ax.add_patch(circ)
    # linhas
    for (a, b) in connections[:3]:
        x0, y0 = circle_positions[a]
        x1, y1 = circle_positions[b]
        ax.plot([x0, x1], [y0, y1], color=cor_logo, lw=8)
    return fig

def guardar(fig, nome_base, fundo='black'):
    png_name = f"{nome_base}_512.png"
    fig.savefig(png_name, dpi=512, bbox_inches='tight',
                facecolor='none' if fundo == 'transparent' else fundo,
                transparent=(fundo == 'transparent'))
    print(f"✅ Guardado: {png_name}")
    img = Image.open(png_name)
    ico_name = f"{nome_base}.ico"
    img.save(ico_name, sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256),(512,512)])
    print(f"✅ Guardado: {ico_name}")
    for fmt in ['svg','webp']:
        fig.savefig(f"{nome_base}.{fmt}", format=fmt, bbox_inches='tight',
                    facecolor='none' if fundo=='transparent' else fundo,
                    transparent=(fundo=='transparent'))
        print(f"✅ Guardado: {nome_base}.{fmt}")
    plt.close(fig)

# --- GERAR TUDO ---
print("🖼️ A gerar variantes com texto...")
for nome, cfg in cores.items():
    fig = criar_logo_com_texto(cor_logo=cfg['logo'], fundo=cfg['fundo'])
    guardar(fig, f"pexp_logo_{nome}", fundo=cfg['fundo'])

print("🪟 A gerar favicons só com o bloco/chain...")
for nome, cfg in cores.items():
    fig = criar_chain_apenas(cor_logo=cfg['logo'], fundo=cfg['fundo'])
    guardar(fig, f"pexp_favicon_{nome}", fundo=cfg['fundo'])

print("✅ Tudo criado com sucesso!")
