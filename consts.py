from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardButton

#STATUSES
STATUS_ADMIN_SET_CATEGORY = 'admin_set_category'
STATUS_ADMIN_SET_NAME_AND_DESCRIPTION = 'admin_set_name_and_description'
STATUS_ADMIN_SEND_FILE = 'admin_send_file'

STATUS_ADMIN_SET_CATEGORY_FAST = 'admin_set_category_fast'
STATUS_ADMIN_SEND_FILE_FAST = 'admin_send_file_fast'
STATUS_NONE = 'None'


#LABELS
LABEL_NEXT_PAGE= '▶️ صفحه بعد'
LABEL_PREVIOUS_PAGE = 'صفحه قبل ◀️'
LABEL_BOOK = '📚 کتاب'
LABEL_SOLUTION = '🧐 حل المسائل'
LABEL_NOTE_AND_EXAMPLE = '📑 جزوه و نمونه سوال'
LABEL_DOWNLOAD = '📥 download: '
LABEL_SEPRATOR = '- - - - - - - - - - - - - - - - -'
LABEL_REQUEST = '📨 درخواست'
LABEL_EXIT = '▶️ بازگشت'
LABEL_HELP = '🆘 راهنما'
LABEL_BACK_TO_CATEGORIES = 'بازگشت به موارد پیدا شده'

#MESSAGES
MESSAGE_ADMIN_WRITE_ID = 'باید بعدش ایدی طرف رو بنویسی.'
MESSAGE_ADMIN_DONE = 'ثبت شد.'
MESSAGE_ADMIN_WRITE_FILE_ID = 'باید بعدش ایدی فایل رو بفرستی.'
MESSAGE_ADMIN_WRITE_DESCRIPTION = 'باید بعدش ایدی و بعدش متن پیام رو بنویسی.'
MESSAGE_DELETED = 'پاک شد.'
MESSAGE_SEND_FILE = 'فایل را بفرستید.'
MESSAGE_SEND_TEXT_AGAIN = 'متن اشتباه. دوباره تلاش کنید.'
MESSAGE_FILE_ADDED_SUCCESSFUL = 'ثبت شد.'
MESSAGE_SEND_FILE_DESCRIPTION = 'اسم و متن و اطلاعات فایل را بفرستید.'
MESSAGE_DID_NOT_FIND_LINK = 'لینک دانلود مورد نظر, یافت نشد.'
MESSAGE_DID_NOT_FIND_FILE = 'هیچ موردی یافت نشد.'
MESSAGE_WRONG_TEXT = 'پیام اشتباه!'
MESSAGE_REQUEST_SENT = 'درخواست شما برای فایل زیر ثبت شد.'
MESSAGE_SENT_TEXT = 'پیام فرستاده شد.'
MESSAGE_USE_START_COMMAND = 'برای شروع استفاده از بات، از دستور زیر استفاده کنید.\n /start'

MESSAGE_HELP_HEAD_ADMIN = '''/add_admin ID
/remove_admin ID
/send_message_to_all REPLY_TO_MESSAGE
/delete_file DOWNLOAD_FILE_ID
/send_message_to_user NEW_LINE ID NEW_LINE TEXT
/edit_file_description NEW_LINE FILE_ID NEW_LINE TEXT
/backup
'''

MESSAGE_REQUEST_IN_QUEUE = '''درخواست شما در صف قرار گرفت.
.در صورت اضافه شدن فایل, به شما اطلاع رسانی خواهد شد.
بازگشت به حالت عادی...'''

MESSAGE_ADD_FILE_TO_DATABASE = '''در حال اضافه کردن فایل به دیتابیس...
لطفا نوع فایل خود را مشخص کنید'''

MESSAGE_HELP_ADMIN = '''۲ تا کار میشه انجام داد.
/add_file :
که اینجا توی ۳ مرحله یه فایل رو میتونی اد کنی.
۱ : دستش رو مشخص میکنی
۲ : اسم و نام و توضیحات و ... برای فایل مینویسی.(حواست باشه که موقع سرچ, این متن رو در نظر میگیرم.)
۳ : فایل رو میفرستی.

/add_file_fast :
اینجا توی ۲ تا مرحله کار رو انجام میدی.
۱ : دستش رو مشخص میکنی
۲ : فایل رو میفرستی و من متنش رو به عنوان اسم و توضیحات و مشخصاتش در نظر میگیرم.
'''

MESSAGE_START = f'''سلام! 👋
برای پیدا کردن منابع دروس دانشگاهیت, میتونی از این ربات استفاده کنی.

**🔎 چطوری یه فایل رو سرچ کنم؟**
اسم کتاب یا نویسنده یا یک کلمه مربوط به فایل مورد نظرت رو بنویس و برام بفرست.
برای کلمه هایی که توشون عدد وجود داره، عدد رو بدون فاصله کنار کلمه بذار. مثال: __ریاضی۱__

اگر نتونستی فایلت رو پیدا کنی, روی دکمه **{LABEL_REQUEST}** کلیک کن تا بتونیم درخواستت رو پیگیری بکنیم. 
'''

MESSAGE_REQUEST = f'''اطلاعات کتاب یا فایلی که دنبالشی رو بفرست. مثلا:
__کتاب فیزیک ۲ هالیدی رزنیک واکر, فارسی__

برای خارج از این حالت, روی **{LABEL_EXIT}** کلیک کن.
'''

MESSAGE_BACK_TO_NORMAL = '''⭕️ به حالت عادی برگشتی.

برای جستوجو کافیه اسم درس یا کتاب یا نویسنده رو بنویسی.
'''

MESSAGE_HELP = f'''فایل ها شامل دسته های {LABEL_BOOK} و {LABEL_NOTE_AND_EXAMPLE} و {LABEL_SOLUTION} میشن. 

 و همچنین خلاصه نویسی ها رو میشه توی دسته ی {LABEL_NOTE_AND_EXAMPLE} پیدا کرد.

**🔎 چطوری فایل رو سرچ و دانلود کنم؟**
اسم کتاب یا نویسنده یا کلمه های کلیدی مثل __هالیدی__ رو مینویسی و میفرستی.
برای کلمه هایی که توشون عدد وجود داره، عدد رو بدون فاصله کنار کلمه بذار. مثال: __ریاضی۱__
توی نتایج پیدا شده, روی لینک دانلود کلیک میکنی.

**🤷‍♂️ نتونستم فایلی که میخوام رو پیدا کنم.**
اگر نتونستی فایلی که دنبالشی رو پیدا کنی, روی دکمه **{LABEL_REQUEST}** کلیک کن تا بتونیم درخواستت رو پیگیری بکنیم.

**📁 چطوری فایل آپلود کنم؟ **
اگر خواستی فایلی رو آپلود کنی, میتونی با ادمین فایل رو به اشتراک بذاری:
@AG_1380
'''

#KEYBOARDS
KEYBOARD_HELP = ReplyKeyboardMarkup(
    [

        [LABEL_REQUEST,LABEL_HELP] 
    ],
    resize_keyboard=True
)

KEYBOARD_ADMIN_ADD_FILE = ReplyKeyboardMarkup(
    [
        [LABEL_NOTE_AND_EXAMPLE,
        LABEL_BOOK,
        LABEL_SOLUTION],
        [LABEL_EXIT]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

KEYBOARD_EXIT = ReplyKeyboardMarkup(
    [
        [LABEL_EXIT],
    ],
    one_time_keyboard=True,
    resize_keyboard=True,
)

#BUTTONS
BUTTON_PREVIOUS_PAGE = [
    InlineKeyboardButton(LABEL_PREVIOUS_PAGE,callback_data=LABEL_PREVIOUS_PAGE)
]

BUTTON_NEXT_PAGE = [
    InlineKeyboardButton( LABEL_NEXT_PAGE, callback_data=LABEL_NEXT_PAGE )
]

BUTTON_NEXT_AND_PREVIOUS_PAGE = [
    InlineKeyboardButton(LABEL_PREVIOUS_PAGE,callback_data=LABEL_PREVIOUS_PAGE),
    InlineKeyboardButton(LABEL_NEXT_PAGE,callback_data=LABEL_NEXT_PAGE)
]

BUTTON_BACK_TO_CATEGORIES = [
    InlineKeyboardButton(LABEL_BACK_TO_CATEGORIES,callback_data=LABEL_BACK_TO_CATEGORIES)
]