# import os
# import django
# from telegram import Update
# from telegram.ext import Updater, CommandHandler, CallbackContext
# from django.db import models

# # Set the DJANGO_SETTINGS_MODULE environment variable
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "people_search_engine.settings")

# # Configure Django settings
# django.setup()

# # Django models
# class BasicInformation(models.Model):
#     personorder = models.IntegerField(primary_key=True)
#     identity_number = models.IntegerField()
#     name = models.CharField(max_length=45)
#     sex = models.CharField(max_length=5)
#     dob = models.DateField()
#     nationality = models.CharField(max_length=45)
#     placeoforigin = models.TextField()
#     placeofresident = models.TextField()
#     personalid = models.TextField()
#     iddate = models.DateField()
#     provider = models.TextField()

# class ContactInfo(models.Model):
#     idnumber = models.IntegerField(primary_key=True)
#     phone = models.IntegerField(null=True)
#     gmail = models.TextField(null=True)
#     usedplatforms = models.IntegerField(null=True)

# # Define command handlers
# def search_cccd(update: Update, context: CallbackContext) -> None:
#     cccd_number = context.args[0]
#     try:
#         result = BasicInformation.objects.get(identity_number=cccd_number)
#         response = f"Name: {result.name}, Date of Birth: {result.dob}, Nationality: {result.nationality}"
#     except BasicInformation.DoesNotExist:
#         response = "CCCD number not found in the database"
#     update.message.reply_text(response)

# def search_phonenumber(update: Update, context: CallbackContext) -> None:
#     phone_number = context.args[0]
#     try:
#         result = ContactInfo.objects.get(phone=phone_number)
#         response = f"Name: {result.name}, Identity Number: {result.idnumber}"
#     except ContactInfo.DoesNotExist:
#         response = "Phone number not found in the database"
#     update.message.reply_text(response)

# def main() -> None:
#     # Set up the Telegram bot
#     updater = Updater("7086978759:AAEpwfTwit1J7hqG6qxRXRxiJVi6HL-xJ_0", use_context=True)

#     # Get the dispatcher to register handlers
#     dispatcher = updater.dispatcher

#     # Register command handlers
#     dispatcher.add_handler(CommandHandler("search_cccd", search_cccd))
#     dispatcher.add_handler(CommandHandler("search_phonenumber", search_phonenumber))

#     # Start the Bot
#     updater.start_polling()
#     updater.idle()

# if __name__ == '__main__':
#     main()

#test version
import os
import django
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from django.db import models
# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "people_search_engine.settings")

# Configure Django settings
django.setup()

# Define command handlers
def search_cccd(update: Update, context: CallbackContext) -> None:
    cccd_number = context.args[0]
    try:
        result = BasicInformation.objects.get(identity_number=cccd_number)
        response = f"Name: {result.name}, Date of Birth: {result.dob}, Nationality: {result.nationality}"
    except BasicInformation.DoesNotExist:
        response = "CCCD number not found in the database"
    update.message.reply_text(response)

def search_phonenumber(update: Update, context: CallbackContext) -> None:
    phone_number = context.args[0]
    try:
        result = ContactInfo.objects.get(phone=phone_number)
        response = f"Name: {result.name}, Identity Number: {result.idnumber}"
    except ContactInfo.DoesNotExist:
        response = "Phone number not found in the database"
    update.message.reply_text(response)

def main() -> None:
    # Set up the Telegram bot
    updater = Updater("7086978759:AAEpwfTwit1J7hqG6qxRXRxiJVi6HL-xJ_0")  
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("search_cccd", search_cccd))
    dispatcher.add_handler(CommandHandler("search_phonenumber", search_phonenumber))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
