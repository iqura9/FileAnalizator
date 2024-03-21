import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

file_sizes = pd.read_csv('file_sizes.txt', header=None, names=['size'])

intervals = [0, 1024, 1024*1024, 10*1024*1024, 100*1024*1024, 1024*1024*1024, float('inf')]
labels = ['<1KB', '1KB-1MB', '1MB-10MB', '10MB-100MB', '100MB-1GB', '>1GB']

file_sizes['size_interval'] = pd.cut(file_sizes['size'], bins=intervals, labels=labels, right=False)

file_size_counts = file_sizes['size_interval'].value_counts().sort_index()

total_sizes_mb = file_sizes.groupby('size_interval')['size'].sum() / (1024 * 1024)
total_sizes_gb = total_sizes_mb / 1024

fig, ax = plt.subplots(figsize=(10, 9))
bar_plot = ax.bar(file_size_counts.index, file_size_counts.values, color='skyblue')
ax.set_title(f'Гістограма кількості файлів за їх розміром (усього {len(file_sizes)} файлів)')
ax.set_xlabel('Розмір файлу (байт)')
ax.set_ylabel('Кількість файлів')
ax.grid(axis='y')
ax.set_xticklabels(labels=file_size_counts.index, rotation=0, ha='center')

for i, v in enumerate(file_size_counts.values):
    ax.text(i, v, str(v), ha='center', va='bottom', rotation=0) 

ax_slider = plt.axes([0.15, 0.01, 0.7, 0.03])
slider = Slider(ax_slider, 'Кількість файлів', 25, max(file_size_counts), valinit=max(file_size_counts), valstep=25)

def update(val):
    max_val = int(slider.val)
    ax.set_ylim(0, max_val)
    plt.draw()

slider.on_changed(update)

conclusions = []
for interval, count in zip(labels, file_size_counts.values):
    percentage = count / len(file_sizes) * 100
    conclusion = f"Переважна більшість файлів ({percentage:.2f}%) має розміри у діапазоні {interval}. Загальний обсяг: {total_sizes_mb[interval]:.2f} MB ({total_sizes_gb[interval]:.2f} GB)"
    conclusions.append((interval, percentage, conclusion))

conclusions.sort(key=lambda x: x[1], reverse=True)

with open('conclusions.txt', 'w') as f:
    for _, _, conclusion in conclusions:
        f.write(conclusion + '\n')

plt.show()
