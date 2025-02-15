# 🚀 Discord Faucet Auto Claim Bot

This bot is designed to automatically claim faucets by sending messages to configured Discord channels. It also handles rate limits and slow mode automatically.

## 📌 Features

- 🔑 Uses **DISCORD_TOKENS** from `.env` for security. Can use multiple Discord tokens.
- 💬 Sends messages to multiple configured channels.
- ⏳ Automatically manages **Slow Mode** & **Rate Limits**.
- 📝 Allows users to add new faucets directly from the CLI.
- 🔄 Uses multi-threading to handle slow mode without blocking other processes.
- 💜 Logs all bot activity in **bot.log**.
- 🔁 **Auto-resends messages** based on user-defined intervals.

---

## 💞 Installation

### 1. Obtain Your Discord Token

Ensure you are logged into your Discord account.

1. Open Developer Tools (`F12` or `Ctrl + Shift + I`).
2. Navigate to the **Console** tab.
3. Paste the following code into the Console and press `Enter`:

```javascript
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

4. Your Discord token will be displayed in the console. Save it securely!

### 2. Clone the Repository

```bash
git clone https://github.com/sam-xode/Discord-auto-claim-faucet.git
cd Discord-auto-claim-faucet
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. First-Time Run

The script will automatically create a `.env`:

```bash
python sam.py
```

---

## 🛠 How to Use

### Running the Bot:

```bash
python sam.py
```

### Menu Options:

1️⃣ **CLAIM ALL FAUCETS** - Claims all configured faucets.

2️⃣ **Add a new faucet claim message** - Adds a new message to claim faucet and saves it in `.env`. Follow these steps:

1. Enter **Discord Tokens**, separated by commas. Example:
   ```
   TOKEN_1,TOKEN_2,TOKEN_3
   ```
2. Enter the **faucet name** you want to add.
3. Enter the **Channel ID** where the message will be sent.
4. Enter the **message** corresponding to each Discord token, separated by `|`. Ensure the order matches the token order. Example:
   ```
   Hello, this is Token_1|Claiming now from Token_2|Token_3 here to claim!
   ```
5. Enter the **auto-claim interval**, e.g.:
   - `6h` → Bot will resend the message every **6 hours**.
   - `30m` → Bot will resend the message every **30 minutes**.
6. Confirm and save the settings.
7. To activate the auto-claim feature, select **1️⃣ CLAIM ALL FAUCETS** in the main menu.

3️⃣ **View channels affected by slow mode** - Displays channels under slow mode and their respective wait times before the next claim attempt.

4️⃣ **Exit** - Quits the program.

---

## 📌 How to Mention Users or Channels in Messages

To include mentions in your faucet messages, use the following format:

### 🔹 Mentioning Users

Use `<@user_id>` format. To get a **user ID**:

1. Open **Discord** and enable **Developer Mode**:
   - **User Settings** → **Advanced** → Enable **Developer Mode**.
2. Right-click the **user profile** you want to mention.
3. Select **Copy ID**.
4. Insert it in your message, e.g.:
   ```
   <@123456789012345678> 0x1232141512123321
   ```

The bot will send a message mentioning the user, e.g.:
```
@faucetbot 0x1232141512123321
```

### 🔹 Getting a Channel ID

To get a **channel ID**:

1. Enable **Developer Mode** as shown above.
2. Right-click the **channel** you want to mention.
3. Select **Copy ID**.
4. Insert it in the "Enter Channel ID" input, e.g.:
   ```
   987654321098765432
   ```

With this format, the bot will send messages that directly mention the specified users or channels.

### 🎥 Video Tutorial
Watch the tutorial on how to mention users or channels in messages here: [YouTube Tutorial]([https://www.youtube.com/](https://www.youtube.com/watch?v=2PfA-Y02TlA))

---

## 👤 Join Our Telegram Group!

Join our Telegram group for more bot scripts and discussions:

➡️ [Join Telegram Group](https://t.me/sam_xode)

---

## 💌 Contact

For questions or contributions, reach out via:

- **GitHub**: [samxode](https://github.com/sam-xode)
- **Twitter**: [@Sam_xode](https://twitter.com/Sam_xode)

