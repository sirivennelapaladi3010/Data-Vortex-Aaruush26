import pandas as pd
import matplotlib.pyplot as plt


# Reading the cleaned dataset which was generated after completing
# all the required data cleaning steps. I am using the cleaned file
# here because the purpose of this script is to perform EDA on the
# final processed data rather than on the corrupted dataset.
df = pd.read_csv("Social_Engine_Posts_Cleaned.csv")


# The timestamp column may not automatically be treated as a date
# when the CSV file is loaded. Converting it into datetime format
# allows us to perform operations such as grouping the posts by month
# and studying how the posting activity changes over time.
df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    errors="coerce"
)


# Printing the basic details of the dataset first so that I can
# confirm that the cleaned dataset has been loaded correctly.
print("=" * 60)
print("EDA - SOCIAL ENGINE")
print("=" * 60)


# Checking the number of rows and columns present in the cleaned
# dataset. This also helps in verifying that the cleaning process
# did not accidentally remove or add unwanted columns.
print("\nDataset shape:")
print(df.shape)


# Displaying all the column names available in the dataset.
# This helps in understanding which fields are available for
# further analysis.
print("\nColumns:")
print(df.columns.tolist())


# Calculating descriptive statistics for the main engagement
# columns. The describe() function gives information such as
# count, mean, standard deviation, minimum, maximum and quartiles.
#
# These values help us get an initial understanding of how likes,
# shares and comments are distributed in the dataset.
print("\nBasic statistics:")
print(
    df[["likes", "shares", "comments"]].describe()
)


# Counting the number of posts belonging to each platform.
# value_counts() is used here because I want to compare the
# number of records available for each platform.
#
# The "Unknown" category is also included because some platform
# values could not be reliably recovered during the cleaning stage.
platform_counts = df["platform"].value_counts()

print("\nPosts by platform:")
print(platform_counts)


# Creating a bar chart from the platform counts.
# A bar chart is suitable here because the platforms are separate
# categories and we want to compare their number of posts.
plt.figure(figsize=(9, 5))

platform_counts.plot(kind="bar")

plt.title("Number of Posts by Platform")
plt.xlabel("Platform")
plt.ylabel("Number of Posts")

# Rotating the platform names so that they do not overlap
# and remain easy to read in the final graph.
plt.xticks(rotation=45)

plt.tight_layout()

# Saving the graph as an image so that it can later be included
# in the EDA report and GitHub repository.
plt.savefig("01_posts_by_platform.png")

# Closing the current figure after saving it.
# This prevents unnecessary figures from remaining open when
# the script continues to create the next graph.
plt.close()


# Calculating the average number of likes, shares and comments
# separately for each platform.
#
# The groupby operation allows us to compare engagement between
# platforms instead of looking at the complete dataset as one group.
platform_engagement = df.groupby("platform")[
    ["likes", "shares", "comments"]
].mean()

print("\nAverage engagement by platform:")
print(platform_engagement.round(2))


# Creating a bar chart for the average engagement values.
# This makes it easier to visually compare likes, shares and
# comments between the different platforms.
platform_engagement.plot(
    kind="bar",
    figsize=(10, 6)
)

plt.title("Average Engagement by Platform")
plt.xlabel("Platform")
plt.ylabel("Average Count")

# Rotating the platform names to improve readability.
plt.xticks(rotation=45)

plt.tight_layout()

# Saving the average engagement graph for use in the report.
plt.savefig("02_average_engagement_by_platform.png")

plt.close()


# Creating a boxplot for likes, shares and comments.
#
# A boxplot is useful for understanding the spread of the data
# and identifying values that are much higher or lower than
# most of the observations.
plt.figure(figsize=(9, 6))

df[["likes", "shares", "comments"]].boxplot()

plt.title("Distribution of Engagement Metrics")
plt.ylabel("Count")

plt.tight_layout()

# Saving the boxplot so that the distribution of engagement
# can be discussed in the EDA report.
plt.savefig("03_engagement_distribution.png")

plt.close()


# Grouping the posts according to the month in which they were
# created. The timestamp column was converted to datetime earlier,
# so the dt.to_period("M") operation can be used to extract the
# year and month together.
#
# This allows us to study whether posting activity increased,
# decreased or fluctuated during the period covered by the dataset.
monthly_posts = df.groupby(
    df["timestamp"].dt.to_period("M")
).size()

print("\nPosts per month:")
print(monthly_posts)


# Creating a line graph to show the change in the number of posts
# over time. A line graph is suitable because the months have
# a natural chronological order.
plt.figure(figsize=(10, 5))

monthly_posts.plot(
    kind="line",
    marker="o"
)

plt.title("Number of Posts Over Time")
plt.xlabel("Month")
plt.ylabel("Number of Posts")

# Rotating the month labels because there may be several months
# displayed along the x-axis.
plt.xticks(rotation=45)

plt.tight_layout()

# Saving the time-based graph for the final EDA report.
plt.savefig("04_posts_over_time.png")

plt.close()


# Calculating the correlation between likes, shares and comments.
#
# Correlation values help us understand whether two engagement
# measures tend to increase or decrease together. A value closer
# to 1 indicates a strong positive relationship, while a value
# closer to -1 indicates a strong negative relationship.
correlation = df[
    ["likes", "shares", "comments"]
].corr()

print("\nCorrelation matrix:")
print(correlation.round(3))


# Creating a visual representation of the correlation matrix.
# This makes the relationships between the engagement variables
# easier to compare instead of looking only at the numerical table.
plt.figure(figsize=(7, 6))

plt.imshow(correlation)

# Adding the column names to the x-axis.
plt.xticks(
    range(len(correlation.columns)),
    correlation.columns
)

# Adding the same variable names to the y-axis.
plt.yticks(
    range(len(correlation.columns)),
    correlation.columns
)

plt.title("Correlation Between Engagement Metrics")

# Adding a color scale so that the correlation values can be
# interpreted from the graph.
plt.colorbar()

plt.tight_layout()

# Saving the correlation graph for the EDA report.
plt.savefig("05_engagement_correlation.png")

plt.close()


# Finding the 10 posts which received the highest number of likes.
#
# This is useful because it helps identify the posts with the
# highest like-based engagement and gives us a closer look at
# the most successful posts in terms of likes.
top_likes = df.nlargest(
    10,
    "likes"
)[
    [
        "post_id",
        "user_id",
        "platform",
        "likes",
        "shares",
        "comments"
    ]
]

print("\nTop 10 posts by likes:")
print(top_likes.to_string(index=False))


# Finding the 10 posts with the highest number of shares.
#
# Shares can be useful for identifying content that users found
# interesting enough to distribute to other users or audiences.
top_shares = df.nlargest(
    10,
    "shares"
)[
    [
        "post_id",
        "user_id",
        "platform",
        "likes",
        "shares",
        "comments"
    ]
]

print("\nTop 10 posts by shares:")
print(top_shares.to_string(index=False))


# Finding the 10 posts with the highest number of comments.
#
# A high number of comments can indicate that a particular post
# generated more discussion or interaction among users.
top_comments = df.nlargest(
    10,
    "comments"
)[
    [
        "post_id",
        "user_id",
        "platform",
        "likes",
        "shares",
        "comments"
    ]
]

print("\nTop 10 posts by comments:")
print(top_comments.to_string(index=False))


# Counting how many posts were created by each user.
# The value_counts() function gives the number of records
# associated with every user ID.
#
# Selecting the first 10 records helps us identify the users
# who were the most active in terms of number of posts.
user_post_counts = df["user_id"].value_counts().head(10)

print("\nTop 10 users by number of posts:")
print(user_post_counts)


# Checking for possible outliers in the engagement columns.
#
# I am using the IQR method because it is a common way of
# identifying unusually high or low values without assuming
# that the data follows a normal distribution.
print("\n" + "=" * 60)
print("OUTLIER ANALYSIS")
print("=" * 60)


# Running the same outlier calculation separately for likes,
# shares and comments.
for column in ["likes", "shares", "comments"]:

    # Calculating the first quartile, which represents the
    # point below which approximately 25% of the observations fall.
    Q1 = df[column].quantile(0.25)

    # Calculating the third quartile, which represents the
    # point below which approximately 75% of the observations fall.
    Q3 = df[column].quantile(0.75)

    # Finding the interquartile range by subtracting Q1 from Q3.
    # The IQR represents the middle 50% of the observations.
    IQR = Q3 - Q1

    # Calculating the lower limit used for identifying potential
    # outliers. Values below this limit are treated as unusually low.
    lower = Q1 - 1.5 * IQR

    # Calculating the upper limit used for identifying potential
    # outliers. Values above this limit are treated as unusually high.
    upper = Q3 + 1.5 * IQR

    # Selecting all records that fall outside the calculated
    # lower and upper limits.
    outliers = df[
        (df[column] < lower) |
        (df[column] > upper)
    ]

    print(f"\n{column}")

    # Printing the quartile values so that the outlier calculation
    # can be verified from the output.
    print("Q1:", round(Q1, 2))
    print("Q3:", round(Q3, 2))

    # Printing the IQR value used for calculating the boundaries.
    print("IQR:", round(IQR, 2))

    # Printing the calculated lower and upper boundaries.
    print("Lower bound:", round(lower, 2))
    print("Upper bound:", round(upper, 2))

    # Printing the total number of values identified as
    # potential outliers for the current engagement metric.
    print("Number of outliers:", len(outliers))


# Printing a final message after completing all the EDA operations.
# At this point, the required graphs and analysis results have
# been generated and are ready to be used in the report.
print("\nEDA analysis completed successfully.")

print("\nGraphs created:")
print("01_posts_by_platform.png")
print("02_average_engagement_by_platform.png")
print("03_engagement_distribution.png")
print("04_posts_over_time.png")
print("05_engagement_correlation.png")