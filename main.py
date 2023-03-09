import random

import telebot
from telebot import types

import FileController
import config

bot = telebot.TeleBot(config.TOKEN)

MEMBER_ADD = 1
MEMBER_LIST = 2
MEMBER_SELECT = 3

bot.set_my_commands([
    telebot.types.BotCommand("/start", "Boshlash"),
    telebot.types.BotCommand("/add", "Yangi user qo'shish"),
    telebot.types.BotCommand("/select", "Random uchun ro'yxatdan tanlash")
])


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello")


@bot.message_handler(commands=['add'])
def add(message):
    bot.send_message(message.chat.id, "Yangi user ismini kiriting: ")
    FileController.setStatus(MEMBER_ADD)
    return


@bot.message_handler(commands=['list'])
def commandList(message):
    chat_id = message.chat.id
    showMembersForRemove(chat_id)
    FileController.setStatus(MEMBER_LIST)


@bot.message_handler(commands=['select'])
def selectList(message):
    FileController.setStatus(MEMBER_SELECT)
    showMembersForSelect(message.chat.id)


# @bot.message_handler(commands=['random'])
def selectRandom(chat_id):
    members = FileController.getMembers()

    selected = list(filter(lambda member: member.selected == 1, members))
    if len(selected) > 0:
        x = random.randint(0, len(selected) - 1)
        member = selected[x]
        bot.send_message(chat_id, "Random tanlangan user: " + member.name)
    else:
        bot.send_message(chat_id, "Bironta ham user tanlanmadi !!!")


@bot.callback_query_handler(func=lambda callback: callback.data)
def callBackHandler(callback):
    chat_id = callback.from_user.id
    message_id = callback.message.id
    member = callback.json["data"]

    status = FileController.getStatus()

    if status == MEMBER_LIST and member != "0":
        FileController.removeMember(member)
        markup = editMarkupMembersList()
        bot.edit_message_reply_markup(chat_id, message_id, reply_markup=markup)

    elif status == MEMBER_SELECT and member != "0":
        FileController.updateMember(member)
        markup = editMarkupMembersSelect()
        bot.edit_message_reply_markup(chat_id, message_id, reply_markup=markup)

    elif status == MEMBER_SELECT and member == "0":
        bot.edit_message_reply_markup(chat_id, message_id, reply_markup=None)
        selectRandom(chat_id)
    else:
        bot.edit_message_reply_markup(chat_id, message_id, reply_markup=None)
        return


def editMarkupMembersList():
    kb = types.InlineKeyboardMarkup(row_width=1)
    members = FileController.getMembers()
    for member in members:
        kb.add(types.InlineKeyboardButton(text=member.name + "   ✖️", callback_data=str(member.name)))
    return kb


def editMarkupMembersSelect():
    kb = types.InlineKeyboardMarkup(row_width=1)
    members = FileController.getMembers()
    for member in members:
        if int(member.selected) == 1:
            kb.add(types.InlineKeyboardButton(text=member.name + " ✅ ", callback_data=str(member.name)))
        else:
            kb.add(types.InlineKeyboardButton(text=member.name, callback_data=str(member.name)))

    kb.add(types.InlineKeyboardButton(text="Random tanlash", callback_data="0"))
    return kb


def showMembersForRemove(chat_id):
    kb = types.InlineKeyboardMarkup(row_width=1)
    members = FileController.refreshSelects()
    for member in members:
        kb.add(types.InlineKeyboardButton(text=member.name + "   ✖️", callback_data=str(member.name.strip())))

    bot.send_message(chat_id, text="Sizning ro'yxatingiz", reply_markup=kb)


def showMembersForSelect(chat_id):
    kb = types.InlineKeyboardMarkup(row_width=1)
    members = FileController.refreshSelects()

    for member in members:
        if member.selected == 0:
            kb.add(types.InlineKeyboardButton(text=member.name + " ✅ ", callback_data=str(member.name)))
        else:
            kb.add(types.InlineKeyboardButton(text=member.name, callback_data=str(member.name)))

    kb.add(types.InlineKeyboardButton(text="Random tanlash", callback_data="0"))
    bot.send_message(chat_id, text="Tanlang:", reply_markup=kb)


@bot.message_handler(content_types=['text'])
def receiveText(message):
    status = FileController.getStatus()
    if status == MEMBER_ADD:
        member = message.json["text"].strip()
        FileController.addMember(member)
        bot.send_message(message.chat.id, "ro'yxatga {} qo'shildi".format(member))


bot.polling(none_stop=True)
