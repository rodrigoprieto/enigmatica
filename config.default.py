import os
from os.path import join

# File Configuration
base_path = os.path.dirname(os.path.abspath(__file__))
data_path = join(base_path, 'data')

if not os.path.exists(data_path):
    os.mkdir(data_path)

# Telegram
telegram_token = ""  # Update your token
telegram_bot_name = ""  # Optional

# User data
user_data = join(data_path, 'users_data.db')

# Enigmas
enigmas_data = join(data_path, 'enigmas.csv')
