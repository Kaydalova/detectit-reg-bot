from django.core.management.base import BaseCommand
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters
from telegram import Bot, ReplyKeyboardMarkup
from telegram_bot.models import Game, Team, Confirmation
from datetime import date
from django.conf import settings


def start(update, context):
    chat_id = update.effective_chat.id
    username = update.message.chat.first_name
    text = f'Привет, {username}! Это бот детективной игры Detectit'
    buttons = ReplyKeyboardMarkup([
                ['/registration'],
                ['/all_games']],
                resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=buttons)


def all_games(update, context):
    chat_id = update.effective_chat.id
    text = 'Расписание игр'
    context.bot.send_message(chat_id=chat_id, text=text)


def make_reg(update, context):
    chat_id = update.effective_chat.id
    info = update.message.text.split('\n')
    team = info[0]
    captain = info[1]
    phone = info[2]
    members = info[3]
    today = date.today()
    next_game = Game.objects.filter(date > today)  # todo
    if Team.objects.filter(game=next_game).exists():
        text = f'Команда {team} уже зарегистрирована на игру {next_game}'
    else:
        Team.objects.create(
            name=team,
            captain=captain,
            phone=phone,
            members=members,
            game=next_game)
        text = f'''Успешная регистрация!
        Команда: {team}
        Капитан: {captain}
        Телефон: {phone}
        Участников: {members}
        '''

    context.bot.send_message(
        chat_id=chat_id,
        text=text)


def registration(update, context):
    today = date.today()
    next_game = Game.objects.filter(date > today)
    chat_id = update.effective_chat.id
    text = f'''Чтобы зарегистрироваться на игру {next_game}
    пришли мне в одном сообщении:
    Название команды
    Имя капитана
    Твой контактный номер телефона
    Количество участников от 2 до 9
    '''
    context.bot.send_message(chat_id=chat_id, text=text)


class Command(BaseCommand):
    help = "Телеграм-бот"

    def handle(self, *args, **options):
        bot = Bot(token=settings.TOKEN)
        updater = Updater(token=settings.TOKEN)
        updater.dispatcher.add_handler(
            CommandHandler('start', start))
        updater.dispatcher.add_handler(
            CommandHandler('all_games', all_games))
        updater.dispatcher.add_handler(
            CommandHandler('registration', registration))
        updater.dispatcher.add_handler(
            MessageHandler(Filters.text, make_reg))
        updater.dispatcher.add_handler(
            CommandHandler('try_again', registration))
        updater.dispatcher.add_handler(
            CommandHandler('registration', registration))
        updater.start_polling()
        updater.idle()
