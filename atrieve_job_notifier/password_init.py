import keyring
import toml, os

# Get the absolute path of the current file
current_file_path = os.path.abspath(__file__)
# Get the parent directory of the current file
parent_directory = os.path.dirname(current_file_path)
# Get the parent directory of the parent directory
grand_parent_directory = os.path.dirname(parent_directory)

# Join the grand parent directory and the config file name
config_file_path = os.path.join(grand_parent_directory, "config.toml")

# Load the toml file
with open(config_file_path, 'r') as f:
    config = toml.load(f)

config_data = config['boards']
print(config_data)

# Loop through each board section
for board_name, board_info in config_data.items():
    # Get the board details
    print(board_name)
    board_username = board_info[0]['username']
    board_login_name = f"atrieve_{board_name}"

    # Check if the password already exists in the keyring
    existing_password = keyring.get_password(board_login_name, board_username)
    if existing_password is not None:
        # Ask the user if they want to keep the existing password or update it
        keep_password = input(f'Password already exists for {board_name}. Do you want to keep it? (y/n): ')
        if keep_password.lower() == 'y':
            # Keep the existing password
            board_password = existing_password
        else:
            # Ask the user to enter their password for the board
            board_password = input(f'Enter password for {board_name}: ')

            # Save the password using keyring
            keyring.set_password(board_login_name, board_username, board_password)
    else:
        # Ask the user to enter their password for the board
        board_password = input(f'Enter password for {board_name}: ')

        # Save the password using keyring
        keyring.set_password(board_login_name, board_username, board_password)

print('Passwords saved using keyring.')
