import config
from UserDatabase import UserDatabase
from EnigmasDatabase import EnigmasDatabase
from telegram import Update, error, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, \
    MessageHandler, CallbackQueryHandler, ConversationHandler, filters
import logging
import random

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initiate the Database where we're going to persist user's settings
user_db = UserDatabase(config.user_data)
enigmas_db = EnigmasDatabase(config.enigmas_data)

# Estados de la conversación
ENIGMA, SUCCESS = range(2)

# Mensajes de éxito y aliento
success_messages = ["¡Enhorabuena! Has demostrado tu habilidad, ¡bien hecho!",
                    "¡Excelente trabajo! Estoy impresionado con tus habilidades para resolver enigmas.",
                    "¡Felicitaciones! Has superado el desafío con éxito. ¡A por más!",
                    "¡Bien hecho! Eres realmente bueno en esto, ¡sigue así!"]

encouragement_messages = ["No te desanimes, los enigmas pueden ser difíciles. ¡Estoy seguro de que lo harás mejor en el próximo!",
                          "¡No te preocupes! Recuerda que lo importante es aprender y divertirse. ¡Sigue intentándolo!",
                          "Aún si no acertaste esta vez, tu esfuerzo es lo que cuenta. ¡No te rindas, el próximo enigma puede ser el tuyo!"]

encouraging_messages = [
    "¡Eso fue emocionante! Si estás listo para más desafíos, no dudes en pedir otro enigma con /enigma. 🧩",
    "¡Me encanta tu espíritu! Cuando quieras otro desafío, solo tienes que usar /enigma. 🚀",
    "Tu mente es poderosa. ¿Por qué no pones a prueba tus habilidades de resolución de enigmas una vez más? Usa /enigma cuando estés listo. 🔍",
    "Eres increíble, ¡sigue así! Cuando estés listo para otro enigma, solo tienes que usar /enigma. 👏",
    "¿Listo para la próxima aventura? Cuando quieras otro desafío, simplemente usa /enigma. ¡Vamos a por ello! 🎉"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Return the welcome message
    :param update:
    :param context:
    :return:
    """
    try:
        user = update.message.from_user
        saved_user = user_db.get_user(user.id)
        if saved_user is None:
            user_db.insert_user(user)
        await update.message.reply_text(
            f"¡Hola {user.first_name}! 👋\n\n"
            "¡Bienvenid@ a nuestro intrigante mundo de enigmas y acertijos matemáticos! 🧩\n\n"
            "Estamos encantados de tenerte aquí y esperamos que disfrutes del desafío. Aquí está lo que puedes hacer:\n\n"
            "- Escribe /enigma para recibir un nuevo y emocionante enigma. 🤔\n"
            "- Escribe /respuesta si deseas conocer la respuesta a un enigma previamente planteado. 🧐\n"
            "- Y si alguna vez necesitas ayuda, simplemente escribe /ayuda. 🆘\n\n"
            "¡Ahora, a sumergirnos en el misterio y la diversión! Que te diviertas. 😄")

    except error.TelegramError as e:
        print(f"Telegram Error occurred: {e.message}")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Help
    :param update:
    :param context:
    :return:
    """
    try:
        user = update.message.from_user
        saved_user = user_db.get_user(user.id)
        if saved_user is None:
            user_db.insert_user(user)
        help_message = (
            "Aquí tienes algunos comandos que puedes usar:\n\n"
            "/start - Inicia la conversación con el bot y muestra un mensaje de bienvenida.\n"
            "/enigma - Obtiene un nuevo enigma para resolver.\n"
            "/respuesta - Te permite obtener la respuesta a un enigma anterior. El bot te pedirá que ingreses el número del enigma al que deseas la respuesta.\n"
            "/ayuda - Muestra este mensaje de ayuda.\n\n"
            "Espero que esto te sea de ayuda! Si tienes alguna otra pregunta, no dudes en preguntar. Que te diviertas!"
        )
        await update.message.reply_text(help_message, parse_mode="Markdown")
    except error.TelegramError as e:
        print(f"Telegram Error occurred: {e.message}")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    await update.message.reply_text('Ha ocurrido un error mientras se procesaba tu actualización.')


async def enigma(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    id, enig = enigmas_db.get_random_enigma()
    await update.message.reply_text(f'*Enigma #{id} ~ {enig["titulo"]}*\n\n{enig["descripcion"]}\n\n'
                                    '👉 Cuando quieras conocer la respuesta podrás consultar /respuesta.',
                                    parse_mode="Markdown")


async def respuesta(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Manda la pregunta inicial
    await update.message.reply_text(
        'Veo que tienes interés en conocer la respuesta a un enigma previamente lanzado. '
        'Por favor, escribe el número del enigma. Ej: 12'
    )
    return ENIGMA


async def enigma_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # El usuario escribió el número del enigma, buscar en la base de datos
    enigma_id_str = update.message.text.strip()

    if not enigma_id_str.isdigit():
        await update.message.reply_text('Por favor, asegúrate de ingresar un número de enigma válido.')
        return ConversationHandler.END

    enigma_id = int(enigma_id_str)

    # Leemos de la Base de datos de enigmas
    enig = enigmas_db.get_enigma(enigma_id)

    if enig is None:
        await update.message.reply_text(f'Lo siento, no pude encontrar el enigma #{enigma_id}. Intenta de nuevo.')
        return ENIGMA

    # Aquí tendrías que implementar el método de tu base de datos que busca el enigma.
    await update.message.reply_text(f'La respuesta al *Enigma #{enigma_id} ~ {enig["titulo"]}* '
                                    f'es:\n\n*{enig["respuesta"]}*\n\nLo habías adivinado?',
                                    reply_markup=InlineKeyboardMarkup([[
                                        InlineKeyboardButton("Sí", callback_data='sí'),
                                        InlineKeyboardButton("No", callback_data='no'),
                                    ]]), parse_mode="Markdown")
    return SUCCESS


async def final(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    if query.data == 'sí':
        message = random.choice(success_messages)  # Elegir un mensaje de éxito al azar
    else:
        message = random.choice(encouragement_messages)  # Elegir un mensaje de aliento al azar
    await query.edit_message_text(message)
    await query.message.reply_text(random.choice(encouraging_messages), parse_mode="Markdown")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Adios 👋... esperamos poder verte por aquí de nuevo algún dia!.')
    return ConversationHandler.END


app = ApplicationBuilder().token(config.telegram_token).build()
# Start commands & help
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("enigma", enigma))
# Crea el manejador de la conversación y añade los estados
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('respuesta', respuesta)],
    states={
        ENIGMA: [MessageHandler(filters.TEXT & ~filters.COMMAND, enigma_response)],
        SUCCESS: [CallbackQueryHandler(final)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)
app.add_handler(conv_handler)
app.add_error_handler(error_handler)

# Start listening
try:
    app.run_polling()

except error.TelegramError as e:
    logger.error(f"Telegram Error occurred: {e.message}")
    print(f"Telegram Error occurred: {e.message}")
