import pandas as pd
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df


# Step 2: Preprocess Dataset
def preprocess_data(df):
    df.drop_duplicates(inplace = True)
    df.dropna(inplace = True)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["weight"] = df["weight"].astype(int)
    df = df.sort_values("timestamp")
    df.reset_index(drop=True, inplace=True)
    return df

# Step 3: Filter by Time Window
def filter_by_time_window(df, window):
    if(window=="Daily"):
        return dict(tuple(df.groupby(df["timestamp"].dt.date)))
    elif window == "Weekly":
        return dict(tuple(df.groupby(df["timestamp"].dt.to_period("W"))))
    elif window == "Monthly":
        return dict(tuple(df.groupby(df["timestamp"].dt.to_period("M"))))
    else:
        return{}

def dataset_summary(df):
    """
    Display a summary of the dataset.
    """

    print("\n========== DATASET SUMMARY ==========")

    # Total records
    print(f"Total Records   : {len(df)}")

    # Unique users (sender + receiver)
    unique_users = pd.concat([df["sender"], df["receiver"]]).nunique()
    print(f"Unique Users    : {unique_users}")

    # Missing values
    print(f"Missing Values  : {df.isnull().sum().sum()}")

    # Duplicate rows
    print(f"Duplicate Rows  : {df.duplicated().sum()}")

    # Date range
    print(f"Date Range      : {df['timestamp'].min()} to {df['timestamp'].max()}")

    print("====================================\n")

if __name__ == "__main__":

    # Load data
    df = load_data(r"data/communication_data_5000_records.csv")

    # Preprocess data
    df = preprocess_data(df)
    dataset_summary(df) #summary

    # Display first rows
    print(df.head())

    # Display dataset information
    df.info()

    # Split into weekly data
    weekly_data = filter_by_time_window(df, "Weekly")

    # Print total weeks
    print("Total Weeks:", len(weekly_data))

    # Print first week's data
    first_week = list(weekly_data.keys())[0]
    print("First Week:", first_week)
    print(weekly_data[first_week].head())

