import subprocess
import os
subprocess.run('pip install -r requirements.txt', shell=True)
if not os.path.exists('./login_data.py'):
    username = "USERNAME_HERE"
    password = "PASSWORD_HERE"
    proxy_user = "USERNAME_HERE"
    proxy_password = "PASSWORD_HERE"
    user = "Default"
    with open('login_data.py', 'w') as login_file:
        login_file.write("username = '" + username + "'\n")
        login_file.write("password = '" + password + "'\n")
        login_file.write("proxy_user = '" + proxy_user + "'\n")
        login_file.write("proxy_password = '" + proxy_password + "'\n")
        login_file.write("user = '" + user + "'\n")

if not os.path.exists('./config.py'):
    side_of_window = 'r'
    proxy_for_source = "http://ch.proxymesh.com:31280/"
    user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/88.0"
    settings_json = {
        "LOG_LEVEL": "DEBUG",
        "COOKIES_ENABLED": False,
        "USER_AGENT": user_agent
    }
    with open('config.py', 'w') as config_file:
        config_file.write("side_of_window = '" + side_of_window + "'\n")
        config_file.write("proxy_for_source = '" + proxy_for_source + "'\n")
        config_file.write("user_agent = '" + user_agent + "'\n")
        config_file.write("settings_json = " + repr(settings_json) + "\n")
print("Enter your details in login_data.py")
print("Adjust your settings in config.py")