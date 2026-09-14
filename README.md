# Data Vortex Aaruush '26 – Social Engine's Data Recovery, Cleaning & EDA 

## Overview

This was completed as part of the Data Vortex Aaruush '26 challenge.

The main task was to work with a deliberately corrupted Social Engine dataset and prepare it for further analysis. We first inspected the dataset to understand the different types of corruption and data quality issues. We then cleaned the data using methods that could be explained and justified from the available information.

The main work carried out in this project includes:

- Checking the overall quality of the dataset
- Finding missing values
- Finding duplicate records
- Investigating unusual values
- Cleaning text data
- Standardizing timestamps
- Handling corrupted engagement values
- Validating the cleaned dataset
- Performing exploratory data analysis
- Creating graphs to understand the data

## Dataset

The main dataset used for the project is:

`Social_Engine_Posts_Corrupted.csv`

It contains information about social media posts with the following columns:

| Column | Description |
|---|---|
| `post_id` | ID used to identify a post |
| `user_id` | ID of the user who created the post |
| `platform` | Social media platform of the post |
| `text_content` | Text written in the post |
| `timestamp` | Date and time associated with the post |
| `likes` | Number of likes received by the post |
| `shares` | Number of times the post was shared |
| `comments` | Number of comments received |

The original dataset contained **12,360 rows and 8 columns**.

After removing exact duplicate records, the cleaned dataset contains **12,000 rows and 8 columns**.

## Problems Found in the Dataset

During the initial inspection, we found several issues that needed to be handled before performing EDA.

### Duplicate Records

There were **360 completely duplicated rows** in the original dataset.

We removed these records because keeping them would cause the same post to be counted more than once during the analysis.

After removing the duplicates, the dataset contained **12,000 rows**.

### Missing Platform Values

The original dataset contained **1,846 missing values** in the `platform` column.

We investigated whether these missing platform values could be recovered from other information in the dataset.

First, we checked whether the text content could be used to identify the platform. Out of the 1,846 records with a missing platform, **1,606 had text content available**. However, only **13 records could be matched exactly with another record where the platform was known**. This meant that text matching could not reliably recover the platform for the remaining records.

We also checked the platform history of the affected users. All affected users had some known platform history. However, **1,822 of the affected users had activity across multiple platforms**, while only **24 users had a single known platform**.

Because most affected users had used multiple platforms, assigning their missing post to one of their previously used platforms would be an assumption. For example, if a user had posts on Instagram, Facebook and YouTube, we could not determine which platform belonged to the particular post with the missing value.

We also checked whether the `post_id` values provided a reliable platform-specific pattern, but no suitable pattern was found for recovering the missing platforms.

Therefore, instead of guessing the platform and introducing potentially incorrect information, we replaced the missing platform values with:

`Unknown`

After removing duplicate records, **1,784 records remained in the `Unknown` category**.

This allowed us to keep the affected records while clearly indicating that their original platform could not be reliably determined from the available evidence.

### Missing Text Content

The original dataset contained **1,746 missing values** in `text_content`.

We checked whether the missing text could be recovered from other records using the available identifiers and timestamps. There was no reliable duplicate record containing the missing text.

Therefore, we kept these values as missing instead of creating replacement text.

After duplicate removal, **1,688 text values remained missing**.

### Negative Likes

Some records contained negative values in the `likes` column.

Since likes represent an engagement count, negative values are not normally expected.

There were **525 negative likes in the original dataset**. After removing duplicate records, **509 negative values remained**.

We treated these negative values as possible sign-flip corruption and converted them to their absolute values.

For example:

`-2500 → 2500`

This is a documented assumption because we cannot prove with complete certainty that the original value was the positive magnitude.

### Mixed Timestamp Formats

The `timestamp` column contained different types of date and time representations.

The formats included:

- ISO datetime values such as `2025-04-13T20:12:18`
- Unix timestamps
- Dates in `DD-MM-YYYY` format

We converted these different formats into a common datetime representation so that the timestamps could be used consistently during analysis.

All timestamp values were successfully converted without conversion failures.

### Text Formatting Issues

Some text values contained HTML entities such as:

`&amp;`

There were also unnecessary spaces and whitespace characters in some records.

We decoded the HTML entities and normalized the extra whitespace while keeping the actual meaning of the post unchanged.

## Data Cleaning Process

We carried out the cleaning process in the following order:

1. Loading the original corrupted dataset.
2. Checking the number of rows and columns.
3. Checking the column names.
4. Checking missing values in each column.
5. Checking for completely duplicated records.
6. Checking for repeated post IDs.
7. Checking for negative values in the likes column.
8. Removing exact duplicate rows.
9. Handling missing platform values using `Unknown`.
10. Cleaning unnecessary whitespace and HTML entities from text.
11. Converting the different timestamp formats into datetime.
12. Converting negative likes using the documented sign-flip assumption.
13. Keeping missing text values as missing.
14. Keeping missing likes as missing.
15. Saving the cleaned dataset as a separate CSV file.
16. Performing final validation on the cleaned data.

## Assumptions Made During Cleaning

Some values could not be recovered with complete certainty. In these cases, we avoided making unsupported guesses.

### Platform

We did not assign missing platforms based on user history because most affected users had used multiple platforms.

Out of the 1,846 records with missing platforms:

- 1,606 had text content available.
- Only 13 could be matched exactly with known-platform text.
- 1,822 affected users had activity across multiple platforms.
- Only 24 affected users had a single known platform.

Therefore:

`Missing platform → Unknown`

This was chosen to preserve the records without incorrectly assigning a platform.

### Likes

Negative likes were treated as possible sign-flip corruption.

Therefore:

`Negative likes → Absolute value`

This is a documented assumption and not a claim that the original value is known with certainty.

### Text

Missing text was left missing because there was no reliable information available to reconstruct the original content.

### Timestamps

The different observed timestamp formats were converted into datetime values.

Unix timestamp values were interpreted as Unix seconds.

## Avoiding Data Fabrication

One of the main principles we followed during the cleaning process was to avoid creating information that was not supported by the dataset.

For example:

- Missing platform values were labelled as `Unknown` instead of being guessed.
- Missing text was left missing.
- Missing likes were left missing.
- No artificial post content was created.
- No user or engagement information was manually invented.

This keeps the cleaned dataset traceable to the original data and makes our assumptions clear.

## Exploratory Data Analysis

After completing the cleaning process, we used the cleaned dataset for exploratory data analysis.

The following analyses were performed.

### Posts by Platform

We counted the number of posts associated with each platform.

A bar chart was created to make it easier to compare the number of posts across platforms.

### Average Engagement by Platform

We calculated the average number of:

- Likes
- Shares
- Comments

for each platform.

This helps us compare engagement levels between the different platforms.

### Engagement Distribution

We created boxplots for likes, shares and comments.

This helps us understand how the engagement values are distributed and identify possible outliers.

### Posts Over Time

We grouped the posts by month using the timestamp.

A line graph was created to observe how posting activity changed over the available time period.

### Engagement Correlation

We calculated the correlation between likes, shares and comments.

This helps us understand whether different engagement measures tend to increase or decrease together.

### Top Posts

We identified the 10 posts with the highest values separately for:

- Likes
- Shares
- Comments

This helps us identify posts with particularly high engagement.

### Most Active Users

We counted the number of posts made by each user.

The top 10 users with the highest number of posts were then identified.

### Outlier Analysis

We used the IQR (Interquartile Range) method to identify potential outliers in:

- Likes
- Shares
- Comments

The Q1, Q3, IQR, lower bound and upper bound were also calculated.

## Reproducible Workflow

The project is designed so that another person can reproduce the cleaning and EDA process using the files in this repository.

### 1. Clone the repository

Open a terminal and run:

```bash
git clone https://github.com/sirivennelapaladi3010/Data-Vortex-Aaruush26.git
