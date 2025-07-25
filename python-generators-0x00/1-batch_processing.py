# 1-batch_processing.py

import seed  # assuming you have seed.py with stream_users_in_batches defined

def stream_users_in_batches(batch_size):
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    offset = 0
    while True:
        cursor.execute(f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset}")
        batch = cursor.fetchall()
        if not batch:
            break
        yield batch
        offset += batch_size
    cursor.close()
    connection.close()

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if int(user['age']) > 25:
                yield user  # yield filtered users

# No explicit return needed because generators implicitly return None when done
