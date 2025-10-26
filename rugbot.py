from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from datetime import datetime
import json, os

# =========================
# CONFIG
# =========================
TOKEN = "8057747412:AAFiqeMJvSIoLU-gSfyq3QN6Sj8vd-hs7aY"  # <-- paste your BotFather token
ADMIN_USERNAME = "@Rugcryptadmin"
WALLET_ADDRESS = "8biE1yocuwo6JVstyFzab9qjcUqc8UmqatZTGCKh9mmf"
DATA_FILE = "users.json"

BOT_HANDLE = "@Rugcryptbot"

# =========================
# STATIC CONTENT (edit to match your screenshots exactly)
# =========================
WELCOME_FMT = (
    "👋 Welcome to {bot}!\n\n"
    "🪪 **User ID:** {uid}\n"
    "👤 **Username:** {uname}\n"
    "📅 **Date & Time:** {now}\n"
    "💳 **Current Plan:** {plan}\n\n"
    "For help or inquiries, contact {admin}"
)

SUB_REQUIRED = "⚠️ **Subscription required.**\n\nTo purchase a license, go to **Purchase & Pricing**."

PRICING_TEXT = (
    "🛒 **Purchase & Pricing**\n\n"
    "🥇 1 Month License: **1 SOL**\n"
    "🥈 6 Month License: **3 SOL**\n"
    "💎 Lifetime License: **5 SOL**\n\n"
    "💰 **Send SOL to:**\n`{wallet}`\n\n"
    "After payment, DM {admin} for activation."
)

# Pressing a specific plan shows the same instructions + plan name
PLAN_SELECTED_FMT = (
    "✅ **{plan} selected**\n\n"
    "💰 **Send SOL to:**\n`{wallet}`\n\n"
    "After payment, DM {admin} for activation."
)

MORE_INFO_TEXT = (
    "ℹ️ **More Info**\n\n"
    "This bot provides crypto automation tools and dashboards.\n"
    f"For any questions, DM {ADMIN_USERNAME}."
)

VOUCHES_TEXT = (
    "✅ **Vouches**\n\n"
    "Trusted users can leave testimonials here.\n"
    f"Questions? DM {ADMIN_USERNAME}."
)

# Features page – mirror your screenshots’ sections/labels
FEATURES_TEXT = (
    "🔥 **Features**\n\n"
    "💎 **Volume Modes**\n"
    "• Simulate organic activity\n"
    "• Configurable intensity\n"
    "• Targeted sessions\n\n"
    "🧠 **Bundler**\n"
    "• Generate wallets for projects\n"
    "• Batch operations, labels\n\n"
    "💬 **Comments**\n"
    "• Automated messaging\n"
    "• Prebuilt templates\n\n"
    "📈 **Bump It**\n"
    "• Boost engagement instantly\n"
)

# My Earnings (static template; edit to mirror your screenshot)
MY_EARNINGS_TEXT = (
    "📊 **My Earnings**\n\n"
    "You currently have **0.0000 SOL** in earnings.\n"
)

# Top Earners (static leaderboard; edit to match your screenshot exactly)
TOP_EARNERS_TEXT = (
    "🏆 **Top Earners**\n\n"
    "1) User: 843002911 — Earnings: **£70,482.23**\n"
    "2) User: 720118457 — Earnings: **£65,741.56**\n"
    "3) User: 912574830 — Earnings: **£59,388.42**\n"
    "4) User: 631209785 — Earnings: **£53,974.11**\n"
    "5) User: 777408291 — Earnings: **£49,820.97**\n"
    "6) User: 854197302 — Earnings: **£45,113.54**\n"
    "7) User: 942781009 — Earnings: **£41,228.09**\n"
    "8) User: 693451220 — Earnings: **£36,445.77**\n"
    "9) User: 888114563 — Earnings: **£31,986.42**\n"
    "10) User: 725908144 — Earnings: **£27,603.58**"
)


# =========================
# DATA STORAGE
# =========================
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        users = json.load(f)
else:
    users = {}

def save_users():
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)

def safe_username(u):
    return ("@" + u) if u else "(no username)"

# =========================
# KEYBOARDS
# =========================
def kb_main():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⚙️ Dashboard", callback_data="menu:dashboard")],
        [InlineKeyboardButton("🔥 Features", callback_data="menu:features")],
        [InlineKeyboardButton("🛒 Purchase & Pricing", callback_data="menu:pricing")],
        [InlineKeyboardButton("ℹ️ More Info", callback_data="menu:info")],
        [InlineKeyboardButton("✅ Vouches", callback_data="menu:vouches")],
    ])

def kb_dashboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Launch Token", callback_data="act:launch_token")],
        [InlineKeyboardButton("🧪 Generate Bundler Wallets", callback_data="act:bundler")],
        [InlineKeyboardButton("📊 My Earnings", callback_data="show:earnings")],
        [InlineKeyboardButton("🏆 Top Earners", callback_data="show:top")],
        [InlineKeyboardButton("💰 Cashout Profits", callback_data="act:cashout")],
        [InlineKeyboardButton("🔙 Back", callback_data="back:main")],
    ])

def kb_features():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 Volume Modes", callback_data="f:volume")],
        [InlineKeyboardButton("🧠 Bundler", callback_data="f:bundler")],
        [InlineKeyboardButton("💬 Comments", callback_data="f:comments")],
        [InlineKeyboardButton("📈 Bump It", callback_data="f:bump")],
        [InlineKeyboardButton("🔙 Back", callback_data="back:main")],
    ])

def kb_pricing():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🥇 1 Month", callback_data="plan:1m")],
        [InlineKeyboardButton("🥈 6 Months", callback_data="plan:6m")],
        [InlineKeyboardButton("💎 Lifetime", callback_data="plan:lifetime")],
        [InlineKeyboardButton("🔙 Back", callback_data="back:main")],
    ])

def kb_back_to_dashboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="menu:dashboard")]])

def kb_back_to_features():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="menu:features")]])

# =========================
# HANDLERS
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    uid = str(u.id)
    if uid not in users:
        users[uid] = {
            "username": u.username,
            "first_name": u.first_name,
            "joined_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "subscription": "None",
        }
        save_users()

    text = WELCOME_FMT.format(
        bot=BOT_HANDLE,
        uid=uid,
        uname=safe_username(u.username),
        now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        plan=users[uid]["subscription"],
        admin=ADMIN_USERNAME,
    )
    await update.message.reply_text(text, reply_markup=kb_main(), parse_mode="Markdown")

async def on_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    data = q.data
    await q.answer()

    # MAIN MENUS
    if data == "menu:dashboard":
        await q.edit_message_text("⚙️ **Dashboard**", reply_markup=kb_dashboard(), parse_mode="Markdown")
        return

    if data == "menu:features":
        await q.edit_message_text("🔥 **Features**", reply_markup=kb_features(), parse_mode="Markdown")
        return

    if data == "menu:pricing":
        await q.edit_message_text(PRICING_TEXT.format(wallet=WALLET_ADDRESS, admin=ADMIN_USERNAME),
                                  reply_markup=kb_pricing(), parse_mode="Markdown")
        return

    if data == "menu:info":
        await q.edit_message_text(MORE_INFO_TEXT, reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Back", callback_data="back:main")]]), parse_mode="Markdown")
        return

    if data == "menu:vouches":
        await q.edit_message_text(VOUCHES_TEXT, reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Back", callback_data="back:main")]]), parse_mode="Markdown")
        return

    # BACK
    if data == "back:main":
        await q.edit_message_text("🏠 **Main Menu**", reply_markup=kb_main(), parse_mode="Markdown")
        return

    # DASHBOARD ACTIONS
    if data in ("act:launch_token", "act:bundler", "act:cashout"):
        await q.edit_message_text(SUB_REQUIRED, reply_markup=kb_back_to_dashboard(), parse_mode="Markdown")
        return

    if data == "show:earnings":
        await q.edit_message_text(MY_EARNINGS_TEXT, reply_markup=kb_back_to_dashboard(), parse_mode="Markdown")
        return

    if data == "show:top":
        await q.edit_message_text(TOP_EARNERS_TEXT, reply_markup=kb_back_to_dashboard(), parse_mode="Markdown")
        return

    # FEATURES SECTIONS (text + back)
    if data == "f:volume":
        await q.edit_message_text("💎 **Volume Modes**\n\n• Simulate organic activity\n• Configurable intensity\n• Targeted sessions",
                                  reply_markup=kb_back_to_features(), parse_mode="Markdown")
        return
    if data == "f:bundler":
        await q.edit_message_text("🧠 **Bundler**\n\n• Generate wallets for projects\n• Batch operations, labels",
                                  reply_markup=kb_back_to_features(), parse_mode="Markdown")
        return
    if data == "f:comments":
        await q.edit_message_text("💬 **Comments**\n\n• Automated messaging\n• Prebuilt templates",
                                  reply_markup=kb_back_to_features(), parse_mode="Markdown")
        return
    if data == "f:bump":
        await q.edit_message_text("📈 **Bump It**\n\n• Boost engagement instantly",
                                  reply_markup=kb_back_to_features(), parse_mode="Markdown")
        return

    # PRICING PLANS
    if data == "plan:1m":
        await q.edit_message_text(PLAN_SELECTED_FMT.format(plan="🥇 1 Month License (1 SOL)", wallet=WALLET_ADDRESS, admin=ADMIN_USERNAME),
                                  reply_markup=kb_pricing(), parse_mode="Markdown")
        return
    if data == "plan:6m":
        await q.edit_message_text(PLAN_SELECTED_FMT.format(plan="🥈 6 Month License (3 SOL)", wallet=WALLET_ADDRESS, admin=ADMIN_USERNAME),
                                  reply_markup=kb_pricing(), parse_mode="Markdown")
        return
    if data == "plan:lifetime":
        await q.edit_message_text(PLAN_SELECTED_FMT.format(plan="💎 Lifetime License (5 SOL)", wallet=WALLET_ADDRESS, admin=ADMIN_USERNAME),
                                  reply_markup=kb_pricing(), parse_mode="Markdown")
        return

# =========================
# APP
# =========================
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(on_cb))
    print("✅ RugBot v2 is running...")
    app.run_polling()

if __name__ == "__main__":
    main()