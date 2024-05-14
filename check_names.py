import pickle
from collections import Counter

# Load the names from the names.pkl file
with open("data/names.pkl", "rb") as f:
    names = pickle.load(f)

# Use Counter to count occurrences of each name
name_counts = Counter(names)

# Print the counts for each unique name
print("Number of entries for each unique name in names.pkl file:")
for name, count in name_counts.items():
    print(f"{name}: {count}")
