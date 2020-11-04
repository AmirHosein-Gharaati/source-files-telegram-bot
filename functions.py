from database import exe_query
from consts import STATUS_NONE, LABEL_BOOK, LABEL_SOLUTION, LABEL_NOTE_AND_EXAMPLE

def is_admin(user_id):
    res = exe_query('''SELECT is_admin FROM users WHERE user_id = ?''',(user_id,))

    if not res:
        return None
    else:
        res = res[0][0]
        return True if res == 1 else False

def insert_person(user_id):
    exe_query('''INSERT OR IGNORE INTO users VALUES(?,?,?)''',(user_id,STATUS_NONE,0) )

def add_admin_in_database(user_id):
    exe_query('''UPDATE users SET is_admin = 1 WHERE user_id = ? ''',(user_id,))

def remove_admin(user_id):
    exe_query('''UPDATE users SET is_admin = 0 WHERE user_id = ? ''',(user_id,))

def delete_file(file_id):
    exe_query('''DELETE from files WHERE id = ?''',(file_id,))

def edit_file_description(ID,description):
    exe_query('''UPDATE files SET description = ? WHERE id = ?''',(description,ID))

def get_user_ids():
    return [user_id for user_id, in exe_query('SELECT user_id FROM users')]

def change_admin_status(status,admin_id):
    exe_query(
        '''UPDATE users SET user_status =(?) WHERE user_id =(?) AND is_admin = 1''',
        (status,admin_id)
    )

def change_user_status(user_id,status):
    exe_query('''UPDATE users SET user_status = (?) WHERE user_id = (?)''',(status,user_id))

def get_admin_status(user_id):
    return exe_query(f'''SELECT user_status FROM users WHERE user_id = (?) AND is_admin = 1''',(user_id,))[0][0]

def get_user_status(user_id):
    res = exe_query(f'''SELECT user_status FROM users WHERE user_id = (?)''',(user_id,))
    
    if not res:
        return None
    else:
        return res[0][0]

def exit_admin(user_id):
    exe_query('UPDATE users SET user_status = (?) WHERE user_id = (?) AND is_admin = 1',(STATUS_NONE,user_id))

def exit_user(user_id):
    exe_query('UPDATE users SET user_status = (?) WHERE user_id = (?)',(STATUS_NONE,user_id))


def add_file_to_database(data):
    exe_query(
        '''INSERT OR IGNORE INTO files(category,description,file_id)
        VALUES (:category,:description,:file_id)''',
        data
    )

def search_number_of_results(text):
    text = '%' + '%'.join(text.split()) + '%'
    book = exe_query(f'''SELECT COUNT(*) FROM files WHERE category = "{LABEL_BOOK}" AND description LIKE ? ''',(text,))[0][0]
    solutions = exe_query(f'''SELECT COUNT(*) FROM files WHERE category = "{LABEL_SOLUTION}" AND description LIKE ? ''',(text,))[0][0]
    examples_and_notes = exe_query(f'''SELECT COUNT(*) FROM files WHERE category = "{LABEL_NOTE_AND_EXAMPLE}" AND description LIKE ? ''',(text,))[0][0]

    return {LABEL_BOOK :book,LABEL_SOLUTION :solutions, LABEL_NOTE_AND_EXAMPLE:examples_and_notes}

def search(text,category):
    '''returns list of tuples: (id,description)'''
    text = '%' + '%'.join(text.split()) + '%'
    return exe_query(f'''SELECT id,description FROM files WHERE category = "{category}" AND description LIKE ? ''',(text,))

def get_file_data(primary_key):
    primary_key = int(primary_key)
    return exe_query('''SELECT id,description,file_id FROM files WHERE id =(?) ''',(primary_key,))

def fa2en(text):
    text = str(text)
    new_text = ''
    for char in text:
        if '۰' <= char <= '۹':
            new_text += str(ord(char) - ord('۰'))
        else:
            new_text += char
    return new_text

def en2fa(text):
    text = str(text)
    new_text = ''
    for char in text:
        if '0' <= char <= '9':
            new_text += chr(int(char) + ord('۰'))
        else:
            new_text += char
    return new_text



def format_search_word(word):
    return word.replace('ي','ی').replace('ك','ک')