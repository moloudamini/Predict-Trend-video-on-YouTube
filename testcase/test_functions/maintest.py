import mysql.connector
conn = mysql.connector.connect(user='user', password='password', host='host', database='database')

# count the number of recoreds in csv file
def count_csv_file_records(filename):
    with open(filename, 'r', encoding="utf-8") as file:
        Counter = 0
        Content = file.read()
        Content_List = Content.split("\n")

        for line in Content_List:
            if line:
                Counter += 1
    return Counter

# count the number of rows in a given table
def count_num_records(tableName):
    cur = conn.cursor()
    query = "SELECT COUNT(*) as Numberofrecords FROM {0}".format(tableName)
    cur.execute(query)
    (row_num,) = cur.fetchone()
    return row_num

# count the number of columns in a given table
def count_num_columns(tableName):
    cur = conn.cursor()
    database='db656_s6amini'
    query = """ SELECT COUNT(*) as NumberofColumns FROM INFORMATION_SCHEMA.COLUMNS WHERE table_schema = %s and table_name = %s"""
    cur.execute(query, (database,tableName))
    (col_num,) = cur.fetchone()
    return col_num

# compare the number of rows in a given table with the expected rows(the number of rows in csv file)
def check_import_accuracy(tableName, expected_rows):   
    actual_rows = count_num_records(tableName)
    if (actual_rows == expected_rows):
        isCorrect = "correct" 
    else: 
        isCorrect = "incorrect"
    return actual_rows, isCorrect

# compare the number of columns and rows in a given table 
def check_row_columns_accuracy(tableName, expected_rows, expected_cols):   
    actual_rows = count_num_records(tableName)
    actual_cols = count_num_columns(tableName)
    if (actual_rows == expected_rows and actual_cols == expected_cols):
        isCorrect = "correct rows and columns" 
    elif (actual_rows == expected_rows or actual_cols == expected_cols): 
        isCorrect = "incorrect_rows or columns" 
    else:
        isCorrect = "incorrect_rows and columns"
    return isCorrect, actual_rows, actual_cols



if __name__ == "__main__":

    table_name = 'Views_CA'
    file_name = 'CAviews.csv'

    col_number= count_num_columns(table_name)
    print ("The table {0} has {1} records".format(table_name, col_number))

    row_number = count_num_records(table_name)
    print ("The table {0} has {1} records".format(table_name, row_number))

    expected_records = count_csv_file_records(file_name)
    print("The number of records in file {0} is {1}".format(file_name, expected_records))

    actual_rows, correct = check_import_accuracy(table_name, expected_records)
    print("Import data to table {0} is {1}, Excepted records: {2}, Actual records: {3}"
            .format(table_name, correct, expected_records, actual_rows))

    correct, actual_rows, actual_cols = check_row_columns_accuracy(table_name, row_number, col_number)
    print("There exist {0} in table {1}, Excepted rows,columns: ({2},{3}), Actual rows,columns: ({4},{5})"
         .format(correct, table_name, row_number, col_number, actual_rows, actual_cols))
