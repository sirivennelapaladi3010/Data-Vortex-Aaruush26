import pandas as pd

# Loading the cleaned Users and Posts datasets
users = pd.read_csv("Social_Engine_Users_Cleaned.csv")
posts = pd.read_csv("Social_Engine_Posts_Cleaned.csv")

# Merging both datasets using user_id
# One user can have many posts, so we keep all posts
combined = posts.merge(
    users,
    on="user_id",
    how="left",
    validate="many_to_one"
)

# Saving the merged dataset as a new CSV file
combined.to_csv("Social_Engine_Combined.csv", index=False)

print("Files merged successfully!")
print("Users rows:", len(users))
print("Posts rows:", len(posts))
print("Combined rows:", len(combined))
print("Combined columns:", len(combined.columns))
print("Saved as: Social_Engine_Combined.csv")