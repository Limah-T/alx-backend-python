import functools
import sqlite3
import time

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("user.db")
        try:
            args = (conn, *args) # Prepend connection, so other args will not be lost
            return func(*args, **kwargs)
        finally:
            conn.close()
    return wrapper

def retry_on_failure(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result:
            print("Success")
        else:
            delay, retries = int(kwargs.get("delay")), int(kwargs.get("retries"))
            try:
                if delay and retries:
                    delay, retries = abs(delay), abs(retries)
                    print(delay, retries)
                    if delay != 0 and retries != 0:
                        time.sleep(delay)
                        while True:
                            result = func(*args, **kwargs)
                            retries -= 1
                            if retries == 0:
                                break
                else:
                    raise ValueError
            except ValueError:
                print("DELAY AND RETRIEVES MUST BE NUMBERS AND NOT EQUAL TO 0")

        return result
    return wrapper
                
@with_db_connection
@retry_on_failure
def fetch_users_with_retry(conn, retries, delay):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user")
    result = cursor.fetchall()
    if not result:
        print("No result")
    else:
        print("Result")
    print(result)
    return result

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry(retries=-3, delay=-10)
# def retry_on_failure(func, retries, delay):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         args = (func, *args)
#         result = func(*args, **kwargs)
#         if result:
#             print("Success")
#         else:
#             try:
#                 delay, retries = abs(int(retries)), abs(int(delay))   
#                 print(delay, retries)
#                 if delay != 0 and retries != 0:
#                     time.sleep(delay)
#                     while True:
#                         result = func(*args, **kwargs)
#                         retries -= 1
#                         if retries == 0:
#                             break
#                 else:
#                     raise ValueError
#             except ValueError:
#                 print("DELAY AND RETRIEVES MUST BE NUMBERS AND NOT EQUAL TO 0")
#         return result
#     return wrapper
                
# @with_db_connection
# @retry_on_failure(retries=3, delay=1)
# def fetch_users_with_retry(conn):
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM user")
#     result = cursor.fetchall()
#     if not result:
#         print("No result")
#     else:
#         print("Result")
#     print(result)
#     return result

# #### attempt to fetch users with automatic retry on failure

# users = fetch_users_with_retry(retries=-3, delay=-10)
