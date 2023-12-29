from helper import load_counter_pickle
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, StrMethodFormatter
import numpy as np

coprus_words_counter = load_counter_pickle("corpus/word_counter2.pickle")

counts = list(coprus_words_counter.values())

print(f"counts {len(counts)}")

print(min(counts))
print(max(counts))
bins = list(range(10)) + [round(x) for x in np.logspace(1, np.ceil(np.log10(max(counts))), num=50)]
# bins = [0, 1, 2, 3, 10, 100, 1000, 10000]
print(bins)
print(f"np.arrange {len(counts)}")

plt.xscale('log')
plt.yscale('log')

plt.gca().xaxis.set_major_formatter(StrMethodFormatter("{x:.0f}"))
plt.gca().yaxis.set_major_formatter(StrMethodFormatter("{x:.0f}"))

# fig1, ax1 = plt.subplots()
# ax2 = ax1.twinx()
# ax1.ticklabel_format(axis="x", style="plain")
# ax2.ticklabel_format(axis="y", style="plain")

# plt.gca().xaxis.ticklabel_format = 'plain'
# plt.gca().yaxis.ticklabel_format = 'plain'

# Creating a histogram using Matplotlib
plt.hist(counts, bins=bins, color='blue')


print("bar")

# Adding labels and title
plt.xlabel('Words')
plt.ylabel('Counts')
plt.title('Histogram of Words Counter')

# Saving the plot as a PNG file
plt.savefig('histogram.png')

# Displaying the plot
plt.show()
