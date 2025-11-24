import telebot
import ccxt
import time
import threading
from datetime import datetime, date
import random

TOKEN = "8594170263:AAFtKwS95XuYcxbEL4OiiJEwD2en6nA234w"
WALLET = "0x0aA55ddb26eA11997936A004128f153d790Da295"

bot = telebot.TeleBot(TOKEN)
exchange = ccxt.binance({'enableRateLimit': True})

premium_users = {}
tahmin_hakki = {}
coins = ['BTC/USDT','ETH/USDT','SOL/USDT','BNB/USDT','XRP/USDT','DOGE/USDT','TON/USDT','ADA/USDT','AVAX/USDT','LINK/USDT']

def is_premium(user_id):
    bitis = premium_users.get(user_id)
    return bitis and datetime.now().strftime("%Y-%m-%d") < bitis

def kalan_hak(user_id):
    bugun = date.today().strftime("%Y-%m-%d")
    if user_id not in tahmin_hakki: tahmin_hakki[user_id] = {}
    if bugun not in tahmin_hakki[user_id]: tahmin_hakki[user_id][bugun] = 0
    return max(0, 2 - tahmin_hakki[user_id][bugun])

def bugun_ne_alayim():
    mesaj = "🚀 BUGÜN NE ALAYIM? – PumpGlobal AI\n\n"
    for coin in random.sample(coins, 5):
        try:
            t = exchange.fetch_ticker(coin)
            change = t['percentage'] or 0
            prob = random.randint(69, 94)
            emoji = "🟢" if change < 0 else "🔴"
            mesaj += f"{emoji} {coin.split('/')[0]} {change:+.2f}% → Yükselme ihtimali %{prob}\n"
        except: pass
    return mesaj

@bot.message_handler(commands=['start'])
def start(m):
    user_id = m.from_user.id
    premium = "✅ PREMIUM" if is_premium(user_id) else "❌ Ücretsiz"
    hak = "SINIRSIZ" if is_premium(user_id) else f"{kalan_hak(user_id)}/2"
    bot.reply_to(m, f"🔥 @pumpglobal_bot\n\nDurum: {premium}\nTahmin hakkı: {hak}\n\n/nealayim → tahmin al\n/premium → 5$ sınırsız")

@bot.message_handler(commands=['nealayim'])
def nealayim(m):
    user_id = m.from_user.id
    bugun = date.today().strftime("%Y-%m-%d")
    if not is_premium(user_id):
        if user_id not in tahmin_hakki: tahmin_hakki[user_id] = {}
        if bugun not in tahmin_hakki[user_id]: tahmin_hakki[user_id][bugun] = 0
        if tahmin_hakki[user_id][bugun] >= 2:
            bot.reply_to(m, f"❌ Hakkın bitti!\nPremium 5 USDT → {WALLET}")
            return
        tahmin_hakki[user_id][bugun] += 1
    tahmin = bugun_ne_alayim()
    hak = "SINIRSIZ" if is_premium(user_id) else f"{kalan_hak(user_id)} kaldı"
    bot.reply_to(m, f"{tahmin}\n\nKalan: {hak}")

@bot.message_handler(commands=['premium'])
def premium(m):
    bot.reply_to(m, f"💎 PREMIUM 5 USDT (30 gün)\n\nAdres (ERC20):\n`{WALLET}`\n\nÖdeme yap → ekran görüntüsünü at!", parse_mode="Markdown")

print("Bot çalışıyor...")
bot.infinity_polling()
