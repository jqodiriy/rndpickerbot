import telebot
from telebot import types

import MemberController
import config
import db_manager
from MemberController import addMemberDB
from MemberController import getMembers
from user_model import UserModel

bot = telebot.TeleBot(config.TOKEN)

MEMBER_ADD = 1
MEMBER_LIST = 2
MEMBER_SELECT = 3

bot.set_my_commands([
    telebot.types.BotCommand("/start", "Boshlash"),
    telebot.types.BotCommand("/add", "Yangi user qo'shish"),
    telebot.types.BotCommand("/list", "Ro'yxatni ko'rish"),
    telebot.types.BotCommand("/select", "Random uchun ro'yxatladab belgilash")
])

@bot.message_handler(commands=['start'])
def start(message):
    user = db_manager.get_user(message.chat.id)

    if user is None:
        user = UserModel(0, message.chat.id, message.from_user.username, 0)
        welcome(user)
    else:
        bot.send_message(message.chat.id, "Hello")


@bot.message_handler(commands=['add'])
def add(message):
    user = db_manager.get_user(message.chat.id)
    if user is None:
        user = UserModel(0, message.chat.id, message.from_user.username, 0)
        welcome(user)
    bot.send_message(user.chat_id, "Yangi user ismini kiriting: ")
    user.status = MEMBER_ADD
    db_manager.updateStatus(user)
    return


@bot.message_handler(commands=['list'])
def commandList(message):
    user = db_manager.get_user(message.chat.id)
    if user is not None:
        showMembersForRemove(user)
        user.status = MEMBER_LIST
        db_manager.updateStatus(user)


@bot.message_handler(commands=['select'])
def selectList(message):
    user = db_manager.get_user(message.chat.id)
    user.status = MEMBER_SELECT
    db_manager.updateStatus(user)
    showMembersForSelect(user,True)


@bot.message_handler(commands=['random'])
def selectRandom(user):
    # user = db_manager.get_user(message.chat.id)
    user.status = 0
    db_manager.updateStatus(user)
    member = MemberController.getRandom(user.chat_id)
    bot.send_message(user.chat_id, "Random tanlangan: " + member.name)


@bot.callback_query_handler(func=lambda callback: callback.data)
def callBackHandler(callback):
    chat_id = callback.from_user.id
    message_id = callback.message.id
    user = db_manager.get_user(chat_id)
    member_id = int(callback.json["data"])

    if user.status == MEMBER_LIST and member_id > 0:
        MemberController.removeMember(member_id)
        bot.delete_message(user.chat_id, message_id)
        showMembersForRemove(user)

    elif user.status == MEMBER_SELECT and member_id > 0:
        MemberController.toggleMember(member_id)
        bot.delete_message(user.chat_id, message_id)
        showMembersForSelect(user)

    elif member_id == 0 and user.status == MEMBER_SELECT:
        selectRandom(user)
    else:
        bot.delete_message(user.chat_id, message_id)


def showMembersForRemove(user):
    kb = types.InlineKeyboardMarkup(row_width=1)
    members = getMembers(user, False)
    for member in members:
        kb.add(types.InlineKeyboardButton(text=member.name + "   ✖️", callback_data=str(member.id)))
    bot.send_message(user.chat_id, text="Sizning ro'yxatingiz", reply_markup=kb)


def showMembersForSelect(user, refresh=False):
    kb = types.InlineKeyboardMarkup(row_width=1)
    members = MemberController.getMembers(user, refresh)
    for member in members:
        if member.selected:
            kb.add(types.InlineKeyboardButton(text=member.name + " ✅ ", callback_data=str(member.id)))
        else:
            kb.add(types.InlineKeyboardButton(text=member.name, callback_data=str(member.id)))

    kb.add(types.InlineKeyboardButton(text="Random tanlash", callback_data="0"))
    bot.send_message(user.chat_id, text="Tanlang:", reply_markup=kb)


@bot.message_handler(content_types=['text'])
def receiveText(message):
    user = db_manager.get_user(message.from_user.id)
    if user.status == MEMBER_ADD:
        addMember(user, message.json["text"])


def welcome(user):
    db_manager.addUser(user)
    bot.send_message(user.chat_id, "Welcome message")


def addMember(user, member):
    addMemberDB(user, member)
    user.status = 0
    db_manager.updateStatus(user)
    bot.send_message(user.chat_id, "sizning ro'yaxatingizga {} qo'shildi".format(member))


bot.polling(none_stop=True)
