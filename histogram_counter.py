from helper import load_counter_pickle
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, StrMethodFormatter
import numpy as np

coprus_words_counter = load_counter_pickle("corpus/word_counter3.pickle")

counts = list(coprus_words_counter.values())

print(f"counts {len(counts)}")

print(min(counts))
print(max(counts))
bins = sorted(list(set([round(x) for x in np.logspace(0, np.ceil(np.log10(max(counts))), num=200)])))
# bins = [0, 1, 2, 3, 10, 100, 1000, 10000]
print(bins)
print(f"np.arrange {len(counts)}")

plt.xscale('log')
plt.yscale('log')

plt.xlabel('Word Frequency: Rare to Common')
plt.ylabel('Unique Words Count')

# plt.gca().xaxis.set_major_formatter(StrMethodFormatter("{x:.0f}"))
# plt.gca().yaxis.set_major_formatter(StrMethodFormatter("{x:.0f}"))


hist, bin_edges, _ = plt.hist(counts, bins=bins, color='blue')

ax2 = plt.gca().twinx()

# cumulative_sum = np.cumsum(hist * bin_edges[:-1])
multiplied_values = hist * bin_edges[:-1]

ax2.plot(bin_edges[:-1], multiplied_values, color='red', marker='o', linestyle='-', linewidth=2, markersize=4, label='Words')
ax2.set_ylabel('Total Words Count', color='red')
ax2.tick_params(axis='y', labelcolor=   'red')
ax2.set_yscale('log')
# ax2.yaxis.set_major_formatter(StrMethodFormatter("{x:.0f}"))


# Adding labels and title
plt.title('Histogram of Words Counter')

# Saving the plot as a PNG file
plt.savefig('results/histogram_word_counter3.png')

# Displaying the plot
plt.show()
