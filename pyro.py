import re
from math import ceil
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, CallbackQuery

import database
from functions import *
from variables import *
from consts import *

app = Client(
    session_name = BOT_NAME,
    api_id= API_ID,
    api_hash= API_HASH,
    bot_token= BOT_TOKEN
)


def give_searched_word_buttons(word):
    '''Returns a list of buttons'''
    result = search_number_of_results(word)

    buttons = []
    for key,value in result.items():
        if value != 0:
            buttons.append(
            [
                InlineKeyboardButton(f'{key} : ({value})',
                    callback_data=key
                )
            ]
        )
    return buttons


@app.on_callback_query(filters.create(func= lambda _,__,callback_query: callback_query.data in [LABEL_NEXT_PAGE,LABEL_PREVIOUS_PAGE]))
def go_next_or_previous_page(client, callback_query):
    #print(callback_query)

    message_data = callback_query.data

    text = str(callback_query.message.text).split('\n')[:3]
    searched_word = text[0].split(' : ')[1]

    page_title_numbers = re.split(r'از|صفحه',text[1])[1:]
    current_page = int(fa2en( page_title_numbers[0]))
    n_all_page = int(fa2en( page_title_numbers[1]))

    category = text[2].split(' : ')[1]
    

    result = search(
        text= searched_word,
        category=category
    )

    if message_data == LABEL_NEXT_PAGE:
        result = result[(current_page)*5:(current_page+1)*5]
    else:
        result = result[(current_page-2)*5:(current_page-1)*5]

    body= []
    for ID,description in result:
        #print(ID)
        body.append(str(description) + '\n' + LABEL_DOWNLOAD + '/dl_' + str(ID))
    
    next_page = current_page + 1 if message_data == LABEL_NEXT_PAGE else current_page - 1
    page_title_string = f'صفحه {en2fa(next_page)} از {en2fa(n_all_page)}'

    body.insert(0,text[0] + '\n' + page_title_string + '\n' + 'دسته : ' + category)
    body = f'\n{LABEL_SEPRATOR}\n\n'.join(body)


    
    if next_page == n_all_page:
        buttons = BUTTON_PREVIOUS_PAGE

    elif next_page == 1:
        buttons = BUTTON_NEXT_PAGE
    else:
       buttons = BUTTON_NEXT_AND_PREVIOUS_PAGE


    app.edit_message_text(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        text=body,
        #parse_mode=None,
        reply_markup= InlineKeyboardMarkup(
            [
                buttons,
                BUTTON_BACK_TO_CATEGORIES
            ]
        )
    )

    app.answer_callback_query(
        callback_query.id
    )

    

@app.on_callback_query(filters.create(
    func = lambda _,__,callback_query: callback_query.data in [LABEL_NOTE_AND_EXAMPLE,LABEL_BOOK,LABEL_SOLUTION]
        )
    )
def send_list(client,callback_query):
    #print(callback_query)
    user_id = callback_query.from_user.id

    searched_word = str(callback_query.message.text).split(' : ')[1]
    #print(searched_word)

    category = callback_query.data

    result = search(
        text= searched_word,
        category=category
    )

    body = []

    if len(result) > 5:
        for i in range(5):
            body.append( str(result[i][1]) + '\n' + LABEL_DOWNLOAD + '/dl_' + str(result[i][0]))
        n_all_pages = en2fa(str( ceil( len(result) / 5) ) )

        page_title_string = f'صفحه ۱ از {n_all_pages}'

        body.insert(0,f'نتایج جستوجو برای : **{searched_word}**' + '\n' + page_title_string + '\n' + 'دسته : ' + category)
        body = f'\n{LABEL_SEPRATOR}\n\n'.join(body)


        app.edit_message_text(
            chat_id=user_id,
            message_id=callback_query.message.message_id,
            text=body,
            #parse_mode=None,
            reply_markup=InlineKeyboardMarkup(
                [
                    BUTTON_NEXT_PAGE,
                    BUTTON_BACK_TO_CATEGORIES
                ]
            )
        )

    else:

        for item in result:
            body.append(str(item[1]) + '\n' + LABEL_DOWNLOAD + '/dl_' + str(item[0]))
        body.insert(0,f'نتایج جستوجو برای : **{searched_word}**' + '\n' + 'دسته : ' + category)
        body = f'\n{LABEL_SEPRATOR}\n\n'.join(body)

        app.edit_message_text(
            chat_id=user_id,
            message_id=callback_query.message.message_id,
            text=body,
            reply_markup= InlineKeyboardMarkup(
                [
                    BUTTON_BACK_TO_CATEGORIES
                ]
            )
            #parse_mode=None
        )
    
    app.answer_callback_query(
            callback_query.id
        )

@app.on_callback_query(filters.regex(pattern=r'{}'.format(LABEL_BACK_TO_CATEGORIES)))
def back_to_categories(client,callback_query):
    #print(callback_query)

    word = str(callback_query.message.text).split('\n')[0]
    word = word.split(' : ')[1]
    #print(word)

    buttons = give_searched_word_buttons(word)

    app.edit_message_text(
        chat_id = callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        text = 'موارد پیدا شده برای : ' + word,
        reply_markup= InlineKeyboardMarkup(
            buttons
        )
    )

    app.answer_callback_query(
            callback_query.id
        )


@app.on_callback_query(filters.regex(pattern=r'^send_your_request_added'))
def send_person_request_added(client,callback_query):
    text = str(callback_query.message.text).split('\n')
    user_id = text[0]
    user_text = ' '.join(text[1:])

    try:
        app.send_message(
        user_id,
        MESSAGE_REQUEST_SENT + '\n' + user_text
        )

        app.edit_message_text(
        chat_id= HEAD_ADMIN_ID,
        message_id=callback_query.message.message_id,
        text='ثبت شده'
        )

    except Exception as e:
        app.send_message(
            HEAD_ADMIN_ID,
            str(e)
        )
    
    app.answer_callback_query(
            callback_query.id
    )

#head_admin
@app.on_message(filters.command('add_admin'))
def add_admin(client,message):
    #global admin_IDs
    user_id = str(message.from_user.id)

    if user_id == HEAD_ADMIN_ID:
        text = message.text.split()
        if len(text) == 1:
            app.send_message(
                user_id,
                MESSAGE_ADMIN_WRITE_ID
            )
            return
        ID = text[1]

        #insert_person(ID)
        add_admin_in_database(ID)

        app.send_message(
            user_id,
            MESSAGE_ADMIN_DONE,
            reply_markup=KEYBOARD_HELP
        )


@app.on_message(filters.command('remove_admin'))
def remove_addmin(client,message):

    if str(message.from_user.id) == HEAD_ADMIN_ID:
        text = message.text.split()
        if len(text) == 1:
            app.send_message(
                HEAD_ADMIN_ID,
                MESSAGE_ADMIN_WRITE_ID
            )
            return
        ID = text[1]

        remove_admin(ID)

        app.send_message(
            HEAD_ADMIN_ID,
            MESSAGE_DELETED
        )
        
@app.on_message(filters.command('send_message_to_all'))
def send_message_to_all(client,message):
    

    if str(message.from_user.id) == HEAD_ADMIN_ID:

        if not message.reply_to_message:
            app.send_message(
                chat_id= HEAD_ADMIN_ID,
                text='باید این دستور رو به یه پیام ریپلای کنی.'
            )
            return
        
        message_id_to_send = message.reply_to_message.message_id
        from_chat_ID = message.chat.id

        user_ids = get_user_ids()
        #print(user_ids)

        for ID in user_ids:
            #print(ID)
            try:
                app.forward_messages(
                    chat_id= ID,
                    from_chat_id= from_chat_ID,
                    message_ids= message_id_to_send,
                    as_copy= True
                )
            except Exception as e:
                print('Error at: ',e)
        
        app.send_message(
            chat_id= HEAD_ADMIN_ID,
            text= 'Done'
        )

@app.on_message(filters.command('delete_file'))
def delete(client,message):

    if str(message.from_user.id) == HEAD_ADMIN_ID:
        text = message.text.split()
        if len(text) == 1:
            app.send_message(
                message.from_user.id,
                MESSAGE_ADMIN_WRITE_FILE_ID
            )
            return
        file_id = text[1]

        delete_file(file_id)

        app.send_message(
            HEAD_ADMIN_ID,
            MESSAGE_DELETED
        )

@app.on_message(filters.command('edit_file_description'))
def edit_description(client,message):

    if HEAD_ADMIN_ID == str(message.from_user.id):
        text = (message.text).split('\n')
        if len(text) < 3 :
            app.send_message(
                HEAD_ADMIN_ID,
                'آیدی و بعد متن رو بده'
            )
            return
        else:
            ID = text[1]
            description = '\n'.join(text[2:])
            edit_file_description(
                ID=ID,
                description=description
            )
            app.send_message(
                HEAD_ADMIN_ID,
                'تغییر کرد.'
            )



@app.on_message(filters.command('send_message_to_user'))
def send_message_to_user(client,message):
    
    if str(message.from_user.id) == HEAD_ADMIN_ID:
        text = message.text
        if text == '/send_message_to_user':
            app.send_message(
                HEAD_ADMIN_ID,
                MESSAGE_ADMIN_WRITE_DESCRIPTION
            )
            return
        else:
            text = text.split('\n')
            ID = text[1]
            description = '\n'.join(text[2:])

            try:
                app.send_message(
                ID,
                description
                )

                app.send_message(
                    HEAD_ADMIN_ID,
                    MESSAGE_SENT_TEXT
                )
            except Exception as e:
                app.send_message(
                    HEAD_ADMIN_ID,
                    str(e)
                )

@app.on_message(filters.command('help_head_admin'))
def help_head_admin(client,message):
    user_id = str(message.from_user.id)

    if user_id == HEAD_ADMIN_ID:
        app.send_message(
            HEAD_ADMIN_ID,
            MESSAGE_HELP_HEAD_ADMIN
        )

#admin
@app.on_message(filters.command('add_file'))
def add_file(clinet,message):
    user_id = str(message.from_user.id)
    
    if is_admin(user_id):
        app.send_message(
            chat_id= user_id,
            text=MESSAGE_ADD_FILE_TO_DATABASE,
            reply_markup= KEYBOARD_ADMIN_ADD_FILE
        )

        change_admin_status(
            admin_id=user_id,
            status=STATUS_ADMIN_SET_CATEGORY
        )
        data[user_id] = {}

@app.on_message(filters.command('add_file_fast'))
def add_file_fast(client,message):
    user_id = str(message.from_user.id)
    
    if is_admin(user_id):
        app.send_message(
            user_id,
            text=MESSAGE_ADD_FILE_TO_DATABASE,
            reply_markup= KEYBOARD_ADMIN_ADD_FILE
        )

        change_admin_status(
            admin_id=user_id,
            status=STATUS_ADMIN_SET_CATEGORY_FAST
        )

        data[user_id] = {}

@app.on_message(filters.command('help_admin'))
def help_admin(client,message):
    user_id = str(message.from_user.id)

    if is_admin(user_id):
        app.send_message(
            user_id,
            text=MESSAGE_HELP_ADMIN
        )

@app.on_message(filters.command('start'))
def start(client,message):
    
    app.send_message(
        message.from_user.id,
        text=MESSAGE_START,
        reply_markup=KEYBOARD_HELP
    )

    insert_person(str(message.from_user.id))


@app.on_message(filters.regex(r'^/dl_'))
def send_dowload_link(client,message):
    user_id = str(message.from_user.id)

    primary_key = message.text.split('/dl_')[1]

    if not primary_key.isnumeric():
        app.send_message(
            user_id,
            text=MESSAGE_DID_NOT_FIND_LINK
        )
        return
    
    data = get_file_data(primary_key)

    if not data:
        app.send_message(
            user_id,
            text=MESSAGE_DID_NOT_FIND_LINK
        )
    
    else:
        app.send_document(
            user_id,
            document=data[0][2],
            caption=data[0][1]
        )



#normal
@app.on_message(filters.regex(pattern=r'^{}'.format(LABEL_REQUEST)))
def request(client,message):
    #print(message)
    user_id = str(message.from_user.id)

    change_user_status(
        user_id=user_id,
        status='request'
    )

    app.send_message(
        chat_id=user_id,
        text=MESSAGE_REQUEST,
        reply_markup=KEYBOARD_EXIT
    )

    
@app.on_message(filters.regex(pattern=r'^{}'.format(LABEL_EXIT)))
def exitt(client,message):
    user_id = str(message.from_user.id)

    if is_admin(user_id):
        exit_admin(user_id)
    
    exit_user(user_id)

    app.send_message(
        user_id,
        MESSAGE_BACK_TO_NORMAL,
        reply_markup=KEYBOARD_HELP
    )


@app.on_message(filters.regex(pattern=r'^{}'.format(LABEL_HELP)))
def helpp(client,message):
    user_id = str(message.from_user.id)

    app.send_message(
        user_id,
        text=MESSAGE_HELP
    )

@app.on_message(filters.private)
def send_normal_message(client,message):
    #print(message)
    
    user_id = str(message.from_user.id)

    if is_admin(user_id) and 'admin' in get_admin_status(user_id):
        status = get_admin_status(user_id)

        if message.text and status == STATUS_ADMIN_SET_CATEGORY_FAST:
            if message.text in [LABEL_NOTE_AND_EXAMPLE,LABEL_BOOK,LABEL_SOLUTION]:
                change_admin_status(
                    status=STATUS_ADMIN_SEND_FILE_FAST,
                    admin_id=user_id
                )

                data[user_id]['category'] = message.text

                app.send_message(
                    user_id,
                    text=MESSAGE_SEND_FILE
                )

            else:
                app.send_message(
                    user_id,
                    text=MESSAGE_SEND_TEXT_AGAIN,
                )
        
        elif message.document and status == STATUS_ADMIN_SEND_FILE_FAST:
            file_id = str(message.document.file_id)

            data[user_id]['file_id'] = file_id
            data[user_id]['description'] = format_search_word(str(message.caption))

            change_admin_status(
                    status=STATUS_ADMIN_SET_CATEGORY_FAST,
                    admin_id=user_id
            )

            add_file_to_database(
                data=data[user_id]
            )

            data[user_id] = {}

            app.send_message(
                user_id,
                text= MESSAGE_FILE_ADDED_SUCCESSFUL
            )

            app.send_message(
                user_id,
                text= MESSAGE_ADD_FILE_TO_DATABASE,
                reply_markup=KEYBOARD_ADMIN_ADD_FILE
            )

        elif message.text and status == STATUS_ADMIN_SET_CATEGORY:
            if message.text in [LABEL_NOTE_AND_EXAMPLE,LABEL_BOOK,LABEL_SOLUTION]:
                change_admin_status(
                    status=STATUS_ADMIN_SET_NAME_AND_DESCRIPTION,
                    admin_id=user_id
                )

                data[user_id]['category'] = message.text

                app.send_message(
                    user_id,
                    text= MESSAGE_SEND_FILE_DESCRIPTION
                )

            else:
                app.send_message(
                    user_id,
                    text= MESSAGE_SEND_TEXT_AGAIN,
                )

        elif message.text and status == STATUS_ADMIN_SET_NAME_AND_DESCRIPTION:
            text = format_search_word(message.text)
            data[user_id]['description'] = text
            change_admin_status(
                    status=STATUS_ADMIN_SEND_FILE,
                    admin_id=user_id
            )
            
            app.send_message(
                user_id,
                text= MESSAGE_SEND_FILE
            )
        elif message.document and status == STATUS_ADMIN_SEND_FILE:
            file_id = str(message.document.file_id)

            data[user_id]['file_id'] = file_id

            change_admin_status(
                    status=STATUS_ADMIN_SET_CATEGORY,
                    admin_id=user_id
            )

            add_file_to_database(
                data=data[user_id]
            )

            data[user_id] = {}

            app.send_message(
                user_id,
                MESSAGE_FILE_ADDED_SUCCESSFUL,
            )

            app.send_message(
                user_id,
                text= MESSAGE_ADD_FILE_TO_DATABASE,
                reply_markup= KEYBOARD_ADMIN_ADD_FILE
            )

        else:
            app.send_message(
                user_id,
                text= MESSAGE_WRONG_TEXT
            )

    #normal mode
    else:
        if message.text:
            message_text = message.text
            
            user_status = get_user_status(user_id)
            
            if user_status == None:
                app.send_message(
                    user_id,
                    MESSAGE_USE_START_COMMAND
                )
                return

            if user_status == STATUS_NONE:
                text = message_text.strip()
                text = en2fa(text)
                text = format_search_word(text)

                buttons = give_searched_word_buttons(text)
                    
                if not buttons:
                    app.send_message(
                        user_id,
                        text= MESSAGE_DID_NOT_FIND_FILE
                    )
                
                else:
                    app.send_message(
                        user_id,
                        f'موارد پیدا شده برای : **{text}**',
                        reply_markup=InlineKeyboardMarkup(
                            buttons
                        )
                    )
            
            elif user_status == 'request':
                #print(message_text)
                text = str(message_text).strip()

                app.send_message(
                    chat_id=HEAD_ADMIN_ID,
                    text= f'{user_id}\n{text}',
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton(
                                text='اطلاع برسون که درخواستش ثبت شد.',
                                callback_data='send_your_request_added'
                            )]
                        ]
                    )
                )

                app.send_message(
                    user_id,
                    text=MESSAGE_REQUEST_IN_QUEUE,
                    reply_markup=KEYBOARD_HELP
                )

                change_user_status(
                    user_id=user_id,
                    status=STATUS_NONE
                )
            
        else:
            app.send_message(
                user_id,
                text=MESSAGE_WRONG_TEXT
            )



if __name__ == '__main__':
    #files
    database.create_files_table()


    #users
    database.create_users_table()

    #initial admin
    exe_query('''INSERT OR IGNORE INTO users VALUES(?,?,?)''',(HEAD_ADMIN_ID,STATUS_NONE,1))

    #admin_save_data
    data = {}

    app.run()
