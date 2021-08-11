import telegram

token = "1853540243:AAH5xBB6arBk6Ggu1YTCa7gSO3vPxDo_AWM"

bot = telegram.Bot(token=token)

print(bot.get_me())
txt = "EMACross: <b>{symbol}</b> Time: <b>{time} IST</b> ".format(symbol="DUMMY1",
                                                                  time="00-00-0000 00:00:00")
txt1 = "EMACross: <b>{symbol}</b> Time: <b>{time} IST</b> ".format(symbol="DUMMY2",
                                                                   time="00-00-0000 00:00:00")
rtxt = txt + txt1
try:
    res = bot.send_message(chat_id="-562712042", text=rtxt, parse_mode="HTML")
except Exception as e:
    print("error", e.__class__)
    print("msg: ", e.message)
print(res)
