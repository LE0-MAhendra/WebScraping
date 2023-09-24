import json

with open("xPageScrapped.json", "r") as file:
    json_data = json.load(file)

title_count = {}

# Check for duplicate titles
for item in json_data:
    title = item["title"]
    if title in title_count:
        title_count[title] += 1
    else:
        title_count[title] = 1
time = 0
# Print duplicate titles and their counts
for title, count in title_count.items():
    if count > 1:
        time += 1
        # pages = [item["page"] for item in json_data if item["title"] == title]
        print(
            f"Title: {title}, Count: {count}")
print(time)
# import json

# with open("aud_total.json", "r") as file:
#     json_data = json.load(file)

# title_count = {}
# unique_data = []  # Create a new list for unique items

# # Iterate through the JSON data and check for duplicate titles
# for item in json_data:
#     title = item["title"]
#     if title in title_count:
#         title_count[title] += 1
#     else:
#         title_count[title] = 1
#         unique_data.append(item)  # Add unique items to the new list

# # Write the unique data back to a JSON file
# with open("unique_aud_total.json", "w") as outfile:
#     json.dump(unique_data, outfile, indent=4)

# print("Duplicates removed, and unique data saved to 'unique_aud_total.json'")
