import requests
import pandas as pd
import numpy as np
import time
import telebot

# === CẤU HÌNH TELEGRAM BOT ===
BOT_TOKEN = "8381481309:AAGB8_RmphHYcgTnZTdqzr57x1S1Tq1ulrE"
CHAT_ID = "1621861804"
bot = telebot.TeleBot(BOT_TOKEN)

# === HÀM LẤY DỮ LIỆU GIÁ BTC/USDT TỪ BINANCE ===
def get_klines(symbol="BTCUSDT", interval="4h", limit=200):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    data = requests.get(url).json()
    frame = pd.DataFrame(data, columns=[
        'time','open','high','low','close','volume','close_time','quote_asset_volume',
        'num_trades','taker_buy_base_asset_volume','taker_buy_quote_asset_volume','ignore'
    ])
    frame['close'] = frame['close'].astype(float)
    return frame

# === HÀM TÍNH EMA ===
def EMA(df, period):
    return df['close'].ewm(span=period, adjust=False).mean()

# === HÀM TÍNH RSI ===
def RSI(df, period=14):
    delta = df['close'].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window=period).mean()
    avg_loss = pd.Series(loss).rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# === PHÂN TÍCH VÀ GỬI THÔNG BÁO ===
def analyze_and_notify():
    df = get_klines()
    df['EMA11'] = EMA(df, 11)
    df['EMA34'] = EMA(df, 34)
    df['EMA89'] = EMA(df, 89)
    df['EMA200'] = EMA(df, 200)
    df['RSI'] = RSI(df)

    last = df.iloc[-1]

    msg = (
        f"📊 BTC/USDT 4H Update\n\n"
        f"💰 Giá hiện tại: {last['close']:.2f} USDT\n"
        f"📈 EMA11: {last['EMA11']:.2f}\n"
        f"📈 EMA34: {last['EMA34']:.2f}\n"
        f"📈 EMA89: {last['EMA89']:.2f}\n"
        f"📈 EMA200: {last['EMA200']:.2f}\n"
        f"💡 RSI(14): {last['RSI']:.2f}"
    )

    bot.send_message(CHAT_ID, msg)
    print("Đã gửi báo cáo Telegram:", msg)

# === CHẠY LIÊN TỤC MỖI 4 GIỜ ===
print("Bot đang chạy... (cập nhật mỗi 4 tiếng)")
while True:
    try:
        analyze_and_notify()
        time.sleep(4 * 60 * 60)  # 4 giờ
    except Exception as e:
        print("Lỗi:", e)
        time.sleep(60)
BOT_TOKEN = "8381481309:AAGB8_RmphHYcgTnZTdqzr57x1S1Tq1ulrE"
CHAT_ID = "1621861804"
