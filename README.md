# Agent301 Telegram Bot

A Python-based automation scripts that uses no API Telegram for interacting with the Agent301 API

[TELEGRAM CHANNEL](https://t.me/cucumber_scripts)

# REGISTRATIONS 

1. Visit : [https://t.me/Agent301Bot/](https://t.me/Agent301Bot/app?startapp=onetime7494064307)
2. Claim card id (enter)
3. Refer friend to AP and tickets

## Features
- Complete and claim available tasks
- Claim available tickets
- Use free tickets
- Configurable through `config.json`.
- Save balance and total balance in balance.txt
- Save bad data (query_id) in Error.txt

### Example Log Output
   ```yaml
------------------------------------
 PROCESSING ACCOUNT № 1/2
------------------------------------
[2024-10-12 23:33:49] ACCOUNT Cool1234567 | BALANCE: 1869995 AP
[2024-10-12 23:33:50] All available tasks done
[2024-10-12 23:33:51] You have 10 tickets
[2024-10-12 23:33:54] SPIN  1 | REWARD: 1 Ticket | BALANCE: 1869995 AP
[2024-10-12 23:34:04] SPIN  2 | REWARD: 1000 AP | BALANCE: 1870995 AP
[2024-10-12 23:34:17] SPIN  3 | REWARD: 1 NOT | BALANCE: 1871995 AP
```

## Installation
1. **Clone the Repository:**

   ```bash
   git clone https://github.com/cucumber-pickle/Agent301Cum.git
   cd Agent301Cum
   ```

2. **Create a virtual environment (optional but recommended)**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

   
3. **Install Dependencies:**

The bot uses Python 3 and requires some external libraries. You can install them using:

  ```bash
    pip install -r requirements.txt
  ```


## Configuration Setup:

Create a config.json file in the project root directory:

   ```json

{
    "claim_tasks": true,
    "claim_tickets": true,
    "use_free_tickets": true,
    "min_spin_delay": 5,
    "max_spin_delay": 15,
    "account_delay": 3,
    "countdown_loop": 28800
}
   ```
- `claim_tasks`: Enable/disable claim_tasks (true/false).
- `claim_tickets`: Enable/disable claim_tasks (true/false).
- `use_free_tickets`: Enable/disable use_free_tickets (true/false).
- `min_spin_delay`: minimum delay (in seconds) between  spins 
- `max_spin_delay`: maximum  delay (in seconds) between spins 
- `account_delay`: delay (in seconds) between processing different accounts
- `countdown_loop`: total duration (in seconds) for which the main loop will run before restarting or stopping

## Query Setup:

Add your Agent301 account tokens to a file named `query.txt` in the root directory. Each token should be on a new line.

Example:
   ```txt
query_id=AA....
user=%7B%22id%....
   ```

## Usage
Run the script with:

   ```bash
python bot.py
   ```

## How to get tgWebAppData (query_id / user_id)

1. Login telegram via portable or web version
2. Launch the bot
3. Press `F12` on the keyboard 
4. Open console
5. Сopy this code in Console for getting tgWebAppData (user= / query=):

```javascript
copy(Telegram.WebApp.initData)
```

6. you will get data that looks like this

```
query_id=AA....
user=%7B%22id%....
```
7. add it to `data.txt` file or create it if you dont have one


## This bot helpfull?  Please support me by buying me a coffee: 

``` 0xc4bb02b8882c4c88891b4196a9d64a20ef8d7c36 ``` - BSC (BEP 20)

``` UQBiNbT2cqf5gLwjvfstTYvsScNj-nJZlN2NSmZ97rTcvKz0 ``` - TON

``` 0xc4bb02b8882c4c88891b4196a9d64a20ef8d7c36 ``` - Optimism

``` THaLf1cdEoaA73Kk5yiKmcRwUTuouXjM17 ``` - TRX (TRC 20)

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
For questions or support, please contact [CUCUMBER TG CHAT](https://t.me/cucumber_scripts_chat)