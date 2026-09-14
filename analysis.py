import pandas as pd
import re
import html

# Loading the original corrupted dataset
df = pd.read_csv("Social_Engine_Posts_Corrupted.csv")

# Checking the basic shape of the dataset
print(df.shape)

# Checking the column names
print(df.columns)

# Viewing the first few rows of the dataset
print(df.head())


# Checking for missing values in each column
print("\nMissing values:")
print(df.isnull().sum())


# Checking for completely duplicated rows
# Removing these later because they can affect the analysis
print("\nDuplicate rows:")
print(df.duplicated().sum())


# Checking for repeated post IDs
print("\nDuplicate post IDs:")
print(df["post_id"].duplicated().sum())


# Checking for negative values in the likes column
# Likes should normally be zero or positive
print("\nNegative likes:")
print((df["likes"] < 0).sum())


# Checking the minimum engagement values
print("\nMinimum values:")
print(df[["likes", "shares", "comments"]].min())


# Checking the maximum engagement values
print("\nMaximum values:")
print(df[["likes", "shares", "comments"]].max())


# Viewing some negative likes for understanding the corruption
print("\nSample negative likes:")
print(
    df[df["likes"] < 0][
        ["post_id", "likes", "shares", "comments"]
    ].head(10)
)


# Removing exact duplicate rows
# Keeping duplicates would count the same post more than once
df = df.drop_duplicates().copy()

print("\nRows after removing duplicates:")
print(len(df))


# Handling missing platform values
# Not guessing the platform because that could create false information
# Using Unknown so the original records are still retained
df["platform"] = df["platform"].fillna("Unknown")

print("\nPlatform distribution:")
print(df["platform"].value_counts())


# Correcting negative likes
# Assuming the negative sign is due to sign-flip corruption
# Using absolute values to keep the engagement count non-negative
df["likes"] = df["likes"].abs()

print("\nNegative likes after correction:")
print((df["likes"] < 0).sum())


# Checking the number of posts with missing text
print("\nMissing text content:")
print(df["text_content"].isna().sum())


# Defining a function for cleaning the text content
def clean_text(value):

    # Keeping missing text as it is instead of creating new content
    if pd.isna(value):
        return value

    # Converting HTML entities such as &amp; into normal characters
    value = html.unescape(str(value))

    # Removing extra spaces, tabs and line breaks
    value = re.sub(r"\s+", " ", value)

    # Removing unnecessary spaces from the beginning and end
    value = value.strip()

    return value


# Applying the text cleaning function to the text column
df["text_content"] = df["text_content"].apply(clean_text)


# Defining a function for handling the different timestamp formats
def parse_timestamp(value):

    # Keeping missing timestamps as missing
    if pd.isna(value):
        return pd.NaT

    # Removing unnecessary spaces around the timestamp
    value = str(value).strip()

    # Identifying Unix timestamp values
    if re.fullmatch(r"\d+", value):
        return pd.to_datetime(
            int(value),
            unit="s",
            errors="coerce"
        )

    # Identifying dates written in DD-MM-YYYY format
    if re.fullmatch(r"\d{2}-\d{2}-\d{4}", value):
        return pd.to_datetime(
            value,
            format="%d-%m-%Y",
            errors="coerce"
        )

    # Converting the remaining timestamp formats
    # such as ISO datetime values
    return pd.to_datetime(value, errors="coerce")


# Applying the timestamp conversion to the complete column
df["timestamp"] = df["timestamp"].apply(parse_timestamp)


# Checking whether any timestamps failed during conversion
print("\nTimestamp conversion failures:")
print(df["timestamp"].isna().sum())


# Saving the cleaned dataset as a separate CSV file
# Keeping the original corrupted dataset unchanged for comparison
df.to_csv("Social_Engine_Posts_Cleaned.csv", index=False)


# Performing final validation after all cleaning steps
print("\nCLEANING COMPLETE")
print("Final shape:", df.shape)

# Checking whether any duplicate rows are still present
print("Remaining duplicate rows:", df.duplicated().sum())

# Checking whether any negative likes are still present
print("Remaining negative likes:", (df["likes"] < 0).sum())

# Confirming that the cleaned dataset has been saved
print("File saved: Social_Engine_Posts_Cleaned.csv")