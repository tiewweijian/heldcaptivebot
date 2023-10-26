from telegram.ext.updater import Updater 
from telegram.update import Update 
from telegram.ext.callbackcontext import CallbackContext 
from telegram.ext.commandhandler import CommandHandler 
from telegram.ext.messagehandler import MessageHandler 
from telegram.ext.filters import Filters 
import logging 
import time
import random


hasClueUsed = [False, False, False]
lifeline = 3
clues = ["This is clue 1", "This is clue 2", "This is clue 3"]

updater = Updater("6440137551:AAFlHf-U24tE__yYKUF10cOBytuufyF3QMM", 
				use_context=True) 

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext): 
	update.message.reply_text("Where... am I?")
	time.sleep(2)
	update.message.reply_text("...")
	time.sleep(1)
	update.message.reply_text(update.message.from_user.first_name + "...help me... ")	
	time.sleep(2)
	update.message.reply_text("One of the dolls came alive, and the next thing I knew... I woke up to you guys coming in...")
	time.sleep(1)
	update.message.reply_text("Could you help me get out of here?")
	time.sleep(1)
	update.message.reply_text("From GM: It seems that you need to enter a phrase here to proceed out of this room.... \n\nType /submitanswer to enter the final passcode after figuring out the puzzles. Type /help to see the available commands.")


def unknown(update: Update, context: CallbackContext): 
	update.message.reply_text("Please! Get me out of here!!\nType /help to for more information") 

def unknown_text(update: Update, context: CallbackContext): 
	update.message.reply_text("I don't quite understand...") 


def clue(update: Update, context: CallbackContext): 
	global lifeline
	random_number = random.randint(0, 2)

	if lifeline != 0: 
		if hasClueUsed[random_number] == True: 
			while hasClueUsed[random_number] == True: 
				random_number = random.randint(0, 2)
		hasClueUsed[random_number] = True
		update.message.reply_text(clues[random_number]) 
		lifeline = lifeline - 1
	else: 
		update.message.reply_text("Unfortunately... you are out of lifelines...") 

def help(update: Update, context: CallbackContext):
	update.message.reply_text('''Here are the list of commands you may use\n\n/clue -- to get a clue. Note that you can only use this 3 times through the game. You will receive a random clue, and it may or may not be helpful for you\n/livesupport -- contact one of the game masters for help /submitanswer --  Submit your final answer. Only the correct phrase will be accepted.''') 

def submit_answer(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_text(f"Hello, {user.first_name}! Please submit your answer.")

    # Store the user ID to track which user is submitting an answer
    context.user_data['user_id'] = user.id

def process_user_input(update: Update, context: CallbackContext):
	user_id = update.effective_user.id
	if 'user_id' in context.user_data and context.user_data['user_id'] == user_id:
		answer = update.message.text
		response = process_answer(answer)  # Replace with your answer processing logic
		update.message.reply_text(f"Your answer: {answer}\n") 
		if answer == "ABC": 
			update.message.reply_text(f"What's that...? I heard some noise upstairs...\n") 
			time.sleep(1)
			update.message.reply_text(f"Could you help me check it out?\n") 
			time.sleep(1)
			update.message.reply_text(f"Hurry please!\n") 
			update.message.reply_text(f"From GM: You may now exit this room, head to Level 4 into the scare zone.\n") 
		else: 
			update.message.reply_text(f"Your answer is wrong :(\n") 
		context.user_data['user_id'] = None
	else:
		# Handle unrecognized input by sending an error message
		update.message.reply_text("I don't get it...")

def livesupport(update: Update, context: CallbackContext):
	update.message.reply_text(f"Please send a private message to @tiewweijian for live support! \n") 


def process_answer(answer):
    # Replace this function with your custom answer processing logic
    # For simplicity, we'll just echo the answer in this example
    return answer

updater.dispatcher.add_handler(CommandHandler('start', start)) 
updater.dispatcher.add_handler(CommandHandler('clue', clue)) 
updater.dispatcher.add_handler(CommandHandler('help', help)) 
updater.dispatcher.add_handler(CommandHandler('livesupport', livesupport))
updater.dispatcher.add_handler(CommandHandler('submitanswer', submit_answer))

updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, process_user_input))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown)) # Filters out unknown commands 

# Filters out unknown messages. 
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text)) 

updater.start_polling() 
