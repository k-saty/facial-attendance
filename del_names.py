import pickle


# Function to load and save data from/to a pickle file
def load_data(file_path):
    with open(file_path, "rb") as f:
        data = pickle.load(f)
    return data


def save_data(data, file_path):
    with open(file_path, "wb") as f:
        pickle.dump(data, f)


# File path for names and corresponding faces data
names_file_path = "data/names.pkl"
faces_data_file_path = "data/faces_data.pkl"

# Load names and corresponding faces data
names = load_data(names_file_path)
faces_data = load_data(faces_data_file_path)

print("Entry to delete in names.pkl file:")
delname = input("Enter a name: ")

# Initialize lists to store filtered data
filtered_names = []
filtered_faces_data = []

# Iterate through each name and corresponding face data
for name, face_data in zip(names, faces_data):
    if name != delname:
        filtered_names.append(name)
        filtered_faces_data.append(face_data)

# Write the filtered names and faces data back to respective files
save_data(filtered_names, names_file_path)
save_data(filtered_faces_data, faces_data_file_path)

print(
    f"Deleted all entries matching '{delname}' from names.pkl and corresponding entries from faces_data.pkl."
)
