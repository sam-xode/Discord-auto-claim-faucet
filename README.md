# Discord-auto-claim-faucet
This code uses a user token instead of a bot token. use it wisely

# 🚀 Discord Auto Claim Faucet

This code is used to automatically claim faucets by sending messages to multiple configured Discord channels. It also handles **rate limits** and **slow mode** automatically.

## 📌 Key Features
- 🔑 **Uses Token from `.env`** for security.
- 💬 **Sends messages to multiple channels** based on configuration.
- ⏳ **Handles Slow Mode & Rate Limits** automatically.
- 📝 **Allows users to add new channels directly from the CLI**.
- 🔄 **Multi-threading** to handle slow mode without blocking other processes.
- 📜 **Logs** all bot activity in `bot.log`.

---

## 📥 Installation
0. Retrieve Your Discord Token
   Using JavaScript Console

   1. Ensure you are **logged into your Discord account**.
   2. Open **Developer Tools** (`F12` or `Ctrl + Shift + I`).
   3. Navigate to the **Console** tab.
   4. Paste the following JavaScript code and press `Enter`:
   
      ```js
      (
          webpackChunkdiscord_app.push(
              [
                  [''],
                  {},
                  e => {
                      m=[];
                      for(let c in e.c)
                          m.push(e.c[c])
                  }
              ]
          ),
          m
      ).find(
          m => m?.exports?.default?.getToken !== void 0
      ).exports.default.getToken()
      ```
   
    Your Discord token will be displayed in the console.


1. Clone this repository:
   ```sh
   git clone https://github.com/username/repo-name.git
   cd repo-name
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the bot for the first time. It will automatically create a `.env` file and prompt you to enter your **DISCORD_TOKEN**, which will then be saved in the `.env` file:
   ```sh
   python bot.py
   ```

---

## 🛠 How to Use

1. Run the bot:
   ```sh
   python auto.py
   ```
2. Select an option from the menu:
   - `1`: Sends messages to all configured channels.
   - `2`: Adds a new channel to `.env` and immediately sends a message.
   - `3`: Exits the bot.

---

## 📌 Important Notes
- Ensure the user has **permissions** to send messages in the selected channels.
- If **rate limited**, the code will wait before resending messages.
- Selecting **Option 2** allows users to add a new channel, which will be automatically saved in `.env`.

---

## 📜 License
This project is licensed under **MIT**. Feel free to use and modify as needed.

---

## 📧 Contact
For questions or contributions, reach out via:
- GitHub: [samxode](https://github.com/sam-xode)
- Twitter: [Sam_xode](https://x.com/sam_xode)

