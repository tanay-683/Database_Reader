import re
import pandas as pd


def remove_unnecessary_columns(dataframe):
    col_to_remove = []
    for col in dataframe.columns:
        if re.search(pattern="Is|Id", string=col):
            col_to_remove.append(col)
        elif re.search(pattern="create|modify", string=col, flags=re.IGNORECASE):
            col_to_remove.append(col)
    return col_to_remove


def date_columns_to_parse(dataframe):
    columns_to_parse = []
    for column in dataframe.columns:
        if re.search(pattern=".*date.*", string=column, flags=re.IGNORECASE):
            columns_to_parse.append(column)
    return columns_to_parse


def data_preprocessing(data):
    # starting table index from 1
    data.index = data.index + 1

    # removing extra columns which contain ID, etc
    extra_columns = remove_unnecessary_columns(data)
    data.drop(extra_columns, axis=1, inplace=True)

    # removing columns which contain 85% none values
    threshold = 0.85
    data = data.loc[:, data.isnull().mean() <= threshold]

    # connverting int64 to int16
    int64_columns = data.select_dtypes(include=["int64"]).columns
    data[int64_columns] = data[int64_columns].astype("int16")

    # Identify columns with float64 data type and convert to float16
    float64_columns = data.select_dtypes(include=["float64"]).columns
    data[float64_columns] = data[float64_columns].astype("float32")

    # parsing date columns from sql to pandas
    date_columns = date_columns_to_parse(data)
    for column in date_columns:
        data[column] = pd.to_datetime(data[column]).dt.strftime("%Y-%m-%d")
        print(data[column])

    return data


def query_to_df(chain, connection, chunksize):
    sql_query = chain["result"]

    # removing TOP and LIMIT keyword from query
    print(f"sql query before processing :::: {sql_query}")

    sql_query = re.sub("(?i)top ([0-9])* ", "", sql_query)
    sql_query = re.sub("LIMIT .*", "", sql_query)

    print(f"sql query after processing :::: {sql_query}")

    data = pd.read_sql(sql=sql_query, con=connection, chunksize=chunksize)
    return data
