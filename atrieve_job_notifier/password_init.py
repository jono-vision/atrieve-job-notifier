import toml
from pathlib import Path

# Get the absolute path of the current file
current_file_path = Path(__file__).resolve()

# Get the parent directory of the current file
parent_directory = current_file_path.parent

# Get the parent directory of the parent directory
grand_parent_directory = parent_directory.parent

# Join the grand parent directory and the config file name
config_file_path = grand_parent_directory/ "config.toml"

# Load the toml file
try:
    with open(config_file_path, 'r') as f:
        config = toml.load(f)
except FileNotFoundError:
    print('Config file not found, creating config file from template...')
    print('Manually edit the resulting config.toml file if boards presented do not apply to you')
    with open(grand_parent_directory/"config_template.toml", 'r') as f:
        config = toml.load(f)

config_data = config['boards']
# print(config_data['blackgold'])

password_is_updated = False

# Loop through each board section
for board in config_data.keys():
    
    # Get the board details
    board_info = config_data[board][0]
    
    board_username = board_info['username']
    board_password = board_info['password']

    if board_password != "":
        # Ask the user if they want to keep the existing password or update it
        print(board_password)
        change_password = input(f'Password already exists for {board}. Would you like to update it? (y/n): ')
            
    if board_password == "" or change_password.lower() == 'y':
        # Ask the user to enter their password for the board
        board_password = input(f'Enter password for {board}: ')
        password_is_updated = True

        # Save the password using keyring
        config['boards'][board][0]['password'] = board_password

if password_is_updated == True:
    with open(config_file_path, 'w') as f:
        toml.dump(config, f)
    print('Passwords saved')
else:
    print('No passwords updated')