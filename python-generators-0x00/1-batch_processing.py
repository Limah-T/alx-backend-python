from seed import connect_db

def stream_users_in_batches(batch_size:int):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("USE ALX_prodev")
    offset = 0
    while True:
        cursor.execute(f"SELECT user_id, name, email, age FROM user_data LIMIT {batch_size} OFFSET {offset}")
        rows = cursor.fetchall()
        if not rows:
            break
        batch = [{ "user_id": row[0], "name": row[1], "email": row[2], "age": int(row[3])} for row in rows ]
        yield batch

        offset += int(batch_size)

    cursor.close()

def batch_processing(batch_size:int):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("USE ALX_prodev")
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                yield user
    cursor.close()

# for x in batch_processing("5"):
#     print(x)