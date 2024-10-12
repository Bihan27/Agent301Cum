import requests
import urllib.parse
import time
import json
import os
import sys
import random
from colorama import Fore, Style
from datetime import datetime
from fake_useragent import UserAgent

red = Fore.LIGHTRED_EX
wht = Fore.LIGHTWHITE_EX
grn = Fore.LIGHTGREEN_EX
yel = Fore.LIGHTYELLOW_EX
blu = Fore.LIGHTBLUE_EX
reset = Style.RESET_ALL
blc = Fore.LIGHTBLACK_EX
last_log_message = None

def countdown_timer(seconds):
    while seconds:
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        h = str(h).zfill(2)
        m = str(m).zfill(2)
        s = str(s).zfill(2)
        print(f"{wht}please wait until {h}:{m}:{s} ", flush=True, end="\r")
        seconds -= 1
        time.sleep(1)
    print(f"{wht}please wait until {h}:{m}:{s} ", flush=True, end="\r")


def log(message):
    now = datetime.now().isoformat(" ").split(".")[0]
    print(f"{blc}[{now}]{wht} {message}{reset}")

try:
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    log("File 'config.json' not found.")

claim_tasks = config.get("claim_tasks", False)
claim_tickets = config.get("claim_tickets", False)
use_free_tickets = config.get("use_free_tickets", False)
min_spin_delay = int(config.get("min_spin_delay", 5))
max_spin_delay = int(config.get("max_spin_delay", 20))
account_delay = config.get("account_delay", 5)
countdown_loop = config.get("countdown_loop", 28800)

now = datetime.now().strftime("%Y-%m-%d %H:%M")

def _banner():
    banner = r"""
  _____   _    _    _____   _    _   __  __   ____    ______   _____  
 / ____| | |  | |  / ____| | |  | | |  \/  | |  _ \  |  ____| |  __ \ 
| |      | |  | | | |      | |  | | | \  / | | |_) | | |__    | |__) |
| |      | |  | | | |      | |  | | | |\/| | |  _ <  |  __|   |  _  / 
| |____  | |__| | | |____  | |__| | | |  | | | |_) | | |____  | | \ \ 
 \_____|  \____/   \_____|  \____/  |_|  |_| |____/  |______| |_|  \_\ """
    print(Fore.GREEN + Style.BRIGHT + banner + Style.RESET_ALL)
    print(grn + f" DuckChainCum Telegram Bot")
    print(red + f" FREE TO USE = Join us on {wht}t.me/cucumber_scripts")
    print(red + f" before start please '{grn}git pull{red}' to update bot")
    log_line()

def _clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def log_line():
    print(wht + "~" * 60)


def extract_username(authorization):
    try:
        # Split the query string
        parsed_data = urllib.parse.parse_qs(authorization)
        user_data_json = parsed_data.get('user', [''])[0]

        # Decode URL encoded string into JSON
        user_data = json.loads(urllib.parse.unquote(user_data_json))

        # Get the username from JSON
        username = user_data.get('username', 'unknown')
        return username
    except (json.JSONDecodeError, KeyError):
        return 'unknown'


def load_authorizations_with_usernames(file_path):
    with open(file_path, 'r') as file:
        authorizations = file.readlines()

    auth_with_usernames = [{'authorization': auth.strip(), 'username': extract_username(auth)} for auth in
                           authorizations]
    return auth_with_usernames

def get_balance(headers):
    url = 'https://api.agent301.org/getMe'
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        json_response = response.json()
        if json_response.get("ok"):
            result = json_response.get("result", {})
            balance = result.get("balance", 0)
            tickets = result.get("tickets", 0)
            return balance, tickets


def get_tasks(headers):
    url = 'https://api.agent301.org/getTasks'
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        json_response = response.json()
        if json_response.get("ok"):
            result = json_response.get("result", {})
            tasks = result.get("data", 0)
            return tasks


def spin(headers):
    url = 'https://api.agent301.org/wheel/spin'
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        json_response = response.json()
        if json_response.get("ok") == True:
            result = json_response.get("result", {})
            balance = result.get("balance", 0)
            tickets = result.get("tickets", 0)
            reward = result.get("reward", 0)
            notcoin = result.get("notcoin", 0)
            toncoin = result.get("toncoin", 0)
            return balance, tickets, reward, notcoin, toncoin
    else:
        log(red + f'Failed to spin due to error. increase min_spin_delay!')
        return None, None, None, None, None

def load(headers):
    url = 'https://api.agent301.org/wheel/load'
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        json_response = response.json()
        if json_response.get("ok"):
            result = json_response.get("result", {})
            tasks = result.get("tasks", 0)
            notcoin = result.get("notcoin", 0)
            toncoin = result.get("toncoin", 0)
            return tasks, notcoin, toncoin


def claim_ticket(task, headers):
    url = 'https://api.agent301.org/wheel/task'
    data = json.dumps({"type": task})
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        json_response = response.json()
        if json_response.get("ok"):
            result = json_response.get("result", {})
            tickets = result.get("tickets", 0)
            return tickets


def transform_reward(reward):
    if reward.startswith('tc'):
        return f"{reward[2:]} TON" # Remove 'tc' and label as TON
    if reward.startswith('t'):
        return f"{reward[1:]} Ticket"  # Remove 't' and label as Tickets
    elif reward.startswith('c'):
        return f"{reward[1:]} AP"  # Remove 'c' and label as AP
    elif reward.startswith('nt'):
        return f"{reward[2:]} NOT"  # Remove 'nt' and label as NOT
    else:
        return f"Unknown Reward: {reward}"

def complete_tasks(authorization, username, account_number):
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'authorization': authorization.strip(),
        'origin': 'https://telegram.agent301.org',
        'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    try:
        balance, tickets = get_balance(headers)
    except:
        log(red + f'Data is broken, Please update query')
        (open("Error.txt", "a", encoding="utf-8").
         write(f"{now} / {account_number} / {username} / Data is broken, Please update query\n"))
        return None, None, None
    log(grn + f"ACCOUNT {wht}{username} | {grn}BALANCE: {wht}{balance} AP")

    if claim_tasks:
        tasks = get_tasks(headers)
        if tasks:
            for task in tasks:
                task_type = task.get("type")
                title = task.get("title")
                is_claimed = task.get("is_claimed")
                count = task.get("count", 0)
                max_count = task.get("max_count")
                if task_type == "stars_purchase" or task_type == 'boost':
                    continue

                if max_count is None and not is_claimed:
                    countdown_timer(1)
                    claim_task(headers, task_type, title)

                elif task_type == "video" and count < max_count:
                    while count < max_count:
                        log(f"{yel}TASK {wht}{task_type} - {title} {yel}PROGRESS: {wht}{count}/{max_count}")
                        countdown_timer(1)
                        if claim_task(headers, task_type, title):
                            count += 1
                        else:
                            break

                elif not is_claimed and count >= max_count:
                    claim_task(headers, task_type, title)
            log(yel + f'All available tasks done')
        else:
            log(red + f"FAILED TO GET TASK. TRY AGAIN.")

    if claim_tickets:
        tasks_wheel, notcoin, toncoin = load(headers)
        if tasks_wheel:
            category_list = list(tasks_wheel.keys())
            for category in category_list:
                if category == 'daily' and tasks_wheel.get(category) != 0:
                    continue
                if category == 'hour':
                    continue
                if tasks_wheel.get(category) == True:
                    continue
                tickets = claim_ticket(category, headers)
                if tickets:
                    log(grn + f'Successfully claim ticket for task {wht}{category}. {grn}Total tickets: {wht}{tickets}')
                else:
                    log(red + f'Failed claim ticket!')
                countdown_timer(1)

    if use_free_tickets:
        if tickets > 0:
            log(yel + f"You have {wht}{tickets} tickets")
            load_whell, notcoin, toncoin = load(headers)
            countdown_timer(1)
            if load_whell:
                i = 1
                while tickets != 0:
                    balance, tickets, reward, notcoin, toncoin = spin(headers)
                    if reward:
                        trans_reward = transform_reward(reward)
                        log(yel + f"SPIN {wht} {i} | {yel}REWARD: {wht}{trans_reward} | {grn}BALANCE: {wht}{balance} AP")
                        i += 1
                        random_spin_delay = random.randint(min_spin_delay, max_spin_delay)
                        countdown_timer(random_spin_delay)
                    else:
                        countdown_timer(10)
            else:
                log(red + f'FAILED load wheel')
        else:
            log(yel + f"You have no tickets")

    try:
        return balance, notcoin, toncoin/100    # Ensure balance is returned after all tasks are processed
    except:
        log(red +f'FAILED return balance')


async def claim_task(headers, task_type, title):
    url = 'https://api.agent301.org/completeTask'
    claim_data = {"type": task_type}
    response = requests.post(url, headers=headers, json=claim_data)

    if response.status_code == 200 and response.json().get("result").get('is_completed') == True:
        result = response.json().get("result", {})
        task_reward = result.get("reward", 0)
        balance = result.get("balance", 0)
        log(yel + f"#TASK {wht}{task_type} - {title} - {yel}REWARD {wht}{task_reward} AP - {grn}BALANCE NOW: {wht}{balance} AP")
        return True
    else:
        log(red + f"TASK {task_type} - {title} - FAILED TO CLAIM!")
        return None



def main():
    auth_data = load_authorizations_with_usernames('query.txt')
    _clear()
    _banner()

    while True:
        total_balance_AP = 0  # Initialize total balance
        total_balance_NOT = 0
        total_balance_TON = 0

        for account_number, data in enumerate(auth_data, start=1):
            authorization = data['authorization']
            username = data['username']

            # Display information about the account currently being processed
            message = f"------------------------------------\n{blu} PROCESSING ACCOUNT № {wht}{account_number}/{len(auth_data)}\n------------------------------------"
            print(message)

            balance, notcoin, toncoin = complete_tasks(authorization, username, account_number)
            if balance:
                total_balance_AP += balance
                total_balance_NOT += notcoin
                total_balance_TON += toncoin
                (open("balance.txt", "a", encoding="utf-8").
                 write(
                    f"{now} / {account_number} / {username} / balance_AP: / {balance} / balance_NOT: / {notcoin} / balance_TON: / {toncoin}\n"))

            countdown_timer(account_delay)
        # Log total balance after processing all accounts
        (open("balance.txt", "a", encoding="utf-8").
         write(f"{now} / total_balance_AP: / {total_balance_AP} / total_balance_NOT: / {total_balance_NOT} / total_balance_TON: / {total_balance_TON}\n"))
        log(f"------------------------------------")
        log(red + f"total_balance_AP: {wht}{total_balance_AP} {red}total_balance_NOT: {wht}{total_balance_NOT} {red}total_balance_TON: {wht}{total_balance_TON}")
        log(f"------------------------------------")
        log(f"Wait for {countdown_loop} seconds")
        countdown_timer(countdown_loop)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log(red + f"Successfully logged out of the bot\n")
        sys.exit()