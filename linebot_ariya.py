from flask import Flask, request, abort
import os
from linebot import (
   LineBotApi, WebhookHandler
)
from linebot.exceptions import (
   InvalidSignatureError
)
from linebot.models import (
   MessageEvent, TextMessage, TextSendMessage, FollowEvent,
   ImageMessage, AudioMessage,
)
import wikipedia
import requests
from googletrans import Translator
import pya3rt

translator = Translator()

app = Flask(__name__)

 #環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

 #APIの設定
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

wikipedia.set_lang("ja")

 #テスト用
@app.route("/")
def hello_world():
   return "hello world!"

 #Webhookからのリクエストをチェック
@app.route("/callback", methods=['POST'])
def callback():
   signature = request.headers['X-Line-Signature']
   body = request.get_data(as_text=True)
   app.logger.info("Request body: " + body)
   try:
       handler.handle(body, signature)
   except InvalidSignatureError:
       abort(400)
   return 'OK'

 #応答プログラム
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    send_message = event.message.text
    if send_message == '機能説明':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='実装済みの機能は下記のとおりです。\n\n'
                                 'ウィキペディア検索(ワード：ウィキペディア)\n'
                                 '翻訳（ワード：翻訳）\n'
                                 '石（ワード：石野郎）\n'
                                 '中央省庁へのアクセス（ワード：中央省庁）\n'
                                 '施行中の法律を調べる（ワード：法律検索）\n'
                                 'それ以外のメッセージが送られた場合は会話を行います。'))
    elif send_message == 'ウィキペディア':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='検索用語を入力して用語にwiki!を追加して送信してください。\n\n'
                                 '例：ダイヤモンドwiki!'))
    elif send_message == '天気1':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='下記形式に沿って調べたい市町村の名前を入力し地名の前にweather1を入力して送信してください。\n\n'
                                 '例：weather1Tokyo'))
    elif send_message == '天気2':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='下記形式に沿って調べたい市町村の名前を入力し地名の前にweather2を入力して送信してください。\n\n'
                                 '例：weather2Tokyo'))
    elif send_message == '天気3':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='下記形式に沿って調べたい市町村の名前を入力し地名の前にweather3を入力して送信してください。\n\n'
                                 '例：weather3Tokyo'))
    elif send_message == '翻訳':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='現在対応しているのは日本語→英語と英語→日本語です。翻訳したい内容を書いたうえで下記の用語を書き足して送信してください。\n\n'
                                 '日本語→英語：jptoen\n'
                                 '英語→日本語：entojp'))
    elif send_message == '石野郎':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='石の名前を調べる→search-stonesと入力して送ってください。\n\n'
                                 '石を買う→buy-stonesと入力して送ってください。\n\n'
                                 'ミネラルショーのイベント情報→event_mineralshowと入力して送ってください。\n\n'
                                 '開発者のオリジナルサイトもよろしければどうぞ。\n'
                                 'http://scientisturanus.com/mineralogist/'))
    elif send_message == '中央省庁':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='2020年現在の12省庁及び国税庁と宮内庁の公式サイトを表示します。アクセスしたい省庁//のURLを展開してください。\n\n'
                                 '①総務省：https://www.soumu.go.jp/\n\n'
                                 '②法務省：http://www.moj.go.jp/\n\n'
                                 '③財務省：https://www.mof.go.jp/\n\n'
                                 '④厚生労働省：https://www.mhlw.go.jp/index.html\n\n'
                                 '⑤外務省：https://www.mofa.go.jp/mofaj/\n\n'
                                 '⑥農林水産省：https://www.maff.go.jp/\n\n'
                                 '⑦文部科学省：https://www.mext.go.jp/\n\n'
                                 '⑧経済産業省：https://www.meti.go.jp/\n\n'
                                 '⑨国土交通省：https://www.mlit.go.jp/\n\n'
                                 '⑩防衛省：https://www.mod.go.jp/\n\n'
                                 '⑪環境省：https://www.env.go.jp/\n\n'
                                 '⑫復興庁：https://www.reconstruction.go.jp/\n\n'
                                 '⑬宮内庁：https://www.kunaicho.go.jp/\n\n'
                                 '⑭国税庁：https://www.nta.go.jp/'))
    elif send_message == '法律検索':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='e-govのURLを表示します。下記URLより進み法律を検索してください。\n\n'
                                 'https://elaws.e-gov.go.jp/search/elawsSearch/elaws_search/lsg0100/'))
    elif send_message == '神主仕事用':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='祝詞を参照します。現在登録済みの祝詞は下記のとおりです。参照したい祝詞をメッセージとして送ってください。\n\n'
                                 '大祓詞\n'
                                 '例祭祝詞\n'
                                 '地鎮祭祝詞'))
    elif "wiki!" in send_message:
        value = send_message.replace('wiki!', '')
        # 正常に検索結果が返った場合
        try:
            wikipedia_page = wikipedia.page(value)
            # wikipedia.page()の処理で、ページ情報が取得できれば、以下のようにタイトル、リンク、サマリーが取得できる。
            wikipedia_title = wikipedia_page.title
            wikipedia_url = wikipedia_page.url
            wikipedia_summary = wikipedia.summary(value)
            reply_message = '【' + wikipedia_title + '】\n' + wikipedia_summary + '\n\n' + '【詳しくはこちら】\n' + wikipedia_url
        # ページが見つからなかった場合
        except wikipedia.exceptions.PageError:
            reply_message = '【' + send_message + '】\nについての情報は見つかりませんでした。'
        # 曖昧さ回避にひっかかった場合
        except wikipedia.exceptions.DisambiguationError as e:
            disambiguation_list = e.options
            reply_message = '複数の候補が返ってきました。以下の候補から、お探しの用語に近いものを再入力してください。\n\n'
            for word in disambiguation_list:
                reply_message += '・' + word + '\n'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(reply_message)
        )
    elif "weather1" in send_message:
        city_name = send_message.replace('weather1', '')
        try:
            app_id = os.environ["app_id"]
            # &units=metricで摂氏温度を求める
            URL = "https://api.openweathermap.org/data/2.5/weather?q={0},jp&units=metric&lang=ja&appid={1}".format(
                city_name, app_id)
            response = requests.get(URL)
            data = response.json()
            # 天気情報
            weather = data["weather"][0]["description"]  # 最高気温
            temp_max = data["main"]["temp_max"]  # 最低気温
            temp_min = data["main"]["temp_min"]  # 寒暖差
            diff_temp = temp_max - temp_min  # 湿度
            humidity = data["main"]["humidity"]
            answer = "天気：" + weather + "\n最高気温：" + str(temp_max) + "℃\n最低気温：" + str(temp_min) + "℃\n寒暖差：" + str(
                diff_temp) + "℃\n湿度：" + str(humidity) + "%"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=answer))
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='該当する地名が見つかりませんでした。'))
    elif "weather2" in send_message:
        city_name = send_message.replace('weather2', '')
        try:
            app_id = os.environ["app_id"]
            # &units=metricで摂氏温度を求める
            url = "https://api.openweathermap.org/data/2.5/forecast?q={0},jp&units=metric&lang=ja&appid={1}".format(
                city_name, app_id)
            response = requests.get(url)
            data = response.json()
            # 天気情報
            weather1 = data["list"][0]["weather"][0]["description"]
            weather2 = data["list"][1]["weather"][0]["description"]
            weather3 = data["list"][2]["weather"][0]["description"]
            weather4 = data["list"][3]["weather"][0]["description"]
            weather5 = data["list"][4]["weather"][0]["description"]
            weather6 = data["list"][5]["weather"][0]["description"]
            weather7 = data["list"][6]["weather"][0]["description"]
            weather8 = data["list"][7]["weather"][0]["description"]
            weather9 = data["list"][8]["weather"][0]["description"]
            answer = city_name + "の現在の天気：" + weather1 + "\n3時間後の天気：" + weather2 + "\n6時間後の天気：" + weather3 + "\n9時間後の天気：" + weather4 + "\n12時間後の天気：" + weather5 + "\n15時間後の天気：" + weather6 + "\n18時間後の天気：" + weather7 + "\n21時間後の天気：" + weather8 + "\n24時間後の天気：" + weather9
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=answer))
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='該当する地名が見つかりませんでした。'))
    elif "weather3" in send_message:
        city_name = send_message.replace('weather3', '')
        try:
            app_id = os.environ["app_id"]
            # &units=metricで摂氏温度を求める
            url = "https://api.openweathermap.org/data/2.5/forecast?q={0},jp&units=metric&lang=ja&appid={1}".format(
                city_name, app_id)
            response = requests.get(url)
            data = response.json()
            # 天気情報
            weather1 = data["list"][0]["weather"][0]["description"]
            weather2 = data["list"][8]["weather"][0]["description"]
            weather3 = data["list"][16]["weather"][0]["description"]
            weather4 = data["list"][24]["weather"][0]["description"]
            weather5 = data["list"][32]["weather"][0]["description"]
            answer = "現在の天気：" + weather1 + "\n明日の天気：" + weather2 + "\n明後日の天気：" + weather3 + "\n明々後日の天気：" + weather4 +"\n4日後の天気：" + weather5
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=answer))
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='該当する地名が見つかりませんでした。'))
    elif "jptoen" in send_message:
        sentence = send_message.replace('jptoen', '')
        try:
            trans_sentence = translator.translate(sentence, dest='en', src='ja')
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=trans_sentence.text))
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='翻訳に失敗しました。google翻訳にアクセスをお願いします。\n'
                                     'https://translate.google.co.jp/?hl=ja'))
    elif "entojp" in send_message:
        sentence = send_message.replace('entojp', '')
        try:
            trans_sentence = translator.translate(sentence, dest='ja', src='en')
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=trans_sentence.text))
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='翻訳に失敗しました。google翻訳にアクセスをお願いします。\n'
                                     'https://translate.google.co.jp/?hl=ja&sl=en&tl=ja&op=translate'))
    elif "search-stones" in send_message:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='九州大学の鉱物リストを表示します。下記URLからアクセスしてください。\n\n'
                                 'http://www.museum.kyushu-u.ac.jp/specimen/kouhyouhon/engref.html'))
    elif "buy-stones" in send_message:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='石のネット販売をしているサイトをいくつか表示します。\n\n'
                                 '東昇天然石：https://shopping.geocities.jp/tosho-stones/\n\n'
                                 'ストーンキャッスル：http://www.stone-castle.com/\n\n'
                                 'vec stone club：https://www.vecstone.jp/?yclid=YSS.1000430854.EAIaIQobChMIuamq6rm47AIVUwVgCh07NAXDEAAYASAAEgILCPD_BwE\n\n'
                                 'エヌズミネラル：https://www.ns-mineral.co.jp/\n\n'
                                 'Art Crystal：https://www.art-crystal.jp/?yclid=YSS.1000013492.EAIaIQobChMIuamq6rm47AIVUwVgCh07NAXDEAEYASAAEgIGePD_BwE'))
    elif "event_mineralshow" in send_message:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='国内と海外のミネラルショーイベント情報のURLを表示します。\n\n'
                                 '国内：https://www.tucson-gemshow.com/%E3%83%9F%E3%83%8D%E3%83%A9%E3%83%AB%E3%82%B7%E3%83%A7%E3%83%BC-2020-%E3%82%B9%E3%82%B1%E3%82%B8%E3%83%A5%E3%83%BC%E3%83%AB-%E5%9B%BD%E5%86%85%E7%89%88/\n'
                                 '海外：https://www.tucson-gemshow.com/%E3%83%9F%E3%83%8D%E3%83%A9%E3%83%AB%E3%82%B7%E3%83%A7%E3%83%BC-2020-%E3%82%B9%E3%82%B1%E3%82%B8%E3%83%A5%E3%83%BC%E3%83%AB-%E6%B5%B7%E5%A4%96%E7%89%88/'))
    elif send_message == '大祓詞':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='高天原に神留り坐す皇親神漏岐・神漏美の命以て、八百万神等を神集へに集へ賜ひ\n'
                                 '神議りに議り賜ひて、我が皇御孫の命は\n'
                                 '豊葦原の水穂の国を、安国と平けく知し食せと事依さし奉りき\n'
                                 '如此依さし奉りし国中に、荒振神等をば\n'
                                 '神問はしに問はし賜ひ、神掃ひに掃ひ賜ひて\n'
                                 '語問ひし磐根・樹立(こだち)・草の垣葉をも語止めて\n'
                                 '天の磐座放ち、天の八重雲をいつのち別きにち別きて、天降し依さし奉りき\n'
                                 '如此依さし奉りし四方の国中と、大倭日高見の国を安国と定め奉りて\n'
                                 '下つ磐根に宮柱太敷き立て、高天原に千木高知りて\n'
                                 '皇御孫の命のみづの御舎仕え奉りて、天の御蔭・日の御蔭と隠り坐して\n'
                                 '安国と平けく知し食さむ国中に、成り出でむ天の益人等が、過ち犯しけむ雑雑の罪事は\n'
                                 '天つ罪と、畔放(あはなち)・溝埋(みぞうめ)・樋放(ひはなち)・頻蒔(しきまき)・串刺・生剝(いきはぎ)・逆剝(さかはぎ)・屎戸(くそと)\n'
                                 'ここだくの罪を天の罪と法り別けて、国つ罪と\n'
                                 '生膚断(いきはだだち)・死膚断(しはだたち)・白人(しらひと)・胡久美(こくみ)・己が母犯す罪・己が子犯す罪・母と子と犯す罪・子と母と犯す罪・畜犯す罪・昆虫(はふむし)の災・高津神の災・高津鳥の災・畜倒し蠱物(まじもの)する罪、ここだくの罪出でむ\n'
                                 '如此出でば、天つ宮事以て、大中臣、天つ金木を本打切り末打断ちて\n'
                                 '千座の置座に置き足らはして、天つ菅曽を本刈り断ち末刈り切りて\n'
                                 '八針に取辟きて、天津祝詞の太祝詞事を宣れ\n\n'
                                 '如此のらば、天つ神は天磐門を押し披きて、天の八重雲をいつの千別きに千別きて聞こし食さむ\n'
                                 '国つ神は高山の末・短山の末に上り坐して、高山のいほり・短山のいほりをかきわけて聞こし食さむ\n'
                                 '如此聞こし食してば、皇御孫の命の朝廷(みかど)をはじめて\n'
                                 '天下四方国には、罪という罪は在らじと\n'
                                 '科戸の風の八重雲を吹き放つ事の如く、朝の御霧・夕の御霧を、朝風・夕風の吹き掃ふ事の如く\n'
                                 '大津辺に居る大船を、へ解き放ちとも解き放ちて、大海原に押し放つ事の如く\n'
                                 'かなたの繁木が本を、焼鎌の敏鎌以て打ち掃ふ事の如く\n'
                                 '遺る罪はあらじと、祓ひ給ひ清め給ふ事を\n'
                                 '高山の末・短山の末より、さくなだりに落ちたぎつ速川の瀬に坐す瀬織津姫といふ神、大海原に持ち出でなむ\n'
                                 '如此持ち出で往なば、荒塩の塩の八百道(やおぢ)の八塩道の八百会(やほあひ)に坐す早秋津姫といふ神、持ちかか呑みてむ\n'
                                 '如此かか呑みてば、気吹戸(いぶきど)に坐す気吹戸主という神、根国底の国に気吹き放ちてむ\n'
                                 '如此気吹き放ちてば、根国底の国に坐すはやさすらひめといふ神、持ちさすらひ失ひてむ\n'
                                 '如此失ひてば、罪といふ罪はあらじと、祓給ひ清め給ふ事を天つ神、国つ神、八百万神等共に聞食せと白す'))
    elif send_message == '例祭祝詞':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='掛けまくも畏き〇〇神社の大前に○○○○恐み恐みも白さく\n'
                                 '此の大宮を静宮の常宮と鎮り坐す\n'
                                 '大神の高き尊き御恵を仰奉り称奉る御氏子崇敬者\n'
                                 '諸大前に参集はり侍りて御縁深き今日の生日の足日に\n'
                                 '年毎の例の随に一年に一度の御祭仕奉ると\n'
                                 '斎まはり清まはりて献奉る御食御酒を始めて\n'
                                 '海川山野の種種の味物を(机代に)置足らはし\n'
                                 '(又神社本庁より幣帛献奉り)て称辞竟奉る状を\n'
                                 '平けく安らけく聞食し\n'
                                 '(大前に奏で奉る歌舞(うたまひ)の技をも米具(めぐ)し宇牟加(うむが)しと見曽奈波(みそなは)し)\n'
                                 'て天皇の大御代を手長の御代の厳御代と\n'
                                 '堅磐に常磐に斎(いは)ひ奉り幸へ奉り給ひ\n'
                                 '御氏子崇敬者を始めて天下四方の国民に至るまでに\n'
                                 '大神の広き厚き恩頼をいや遠永に蒙らしめ給ひ\n'
                                 '各も各も清き明き直き正しき真心以ちて\n'
                                 '負持つ職業に勤み励み互に睦び和みつつ\n'
                                 'いや益益に世の人人の幸福を進めしめ給ひ\n'
                                 '子孫の八十続五十橿八桑枝の如く\n'
                                 '立栄えしめ給へと恐み恐みも白す'))
    elif send_message == '地鎮祭祝詞':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='此の○○(地名)の里の佳所(よきところ)を祓ひ清め\n'
                                 '神籬(ひもろぎ)立て招(お)ぎ奉り坐せ奉る産土大神(うぶすなのおほかみ)・大地主大神(おほとこぬしのおほかみ)等の大前に恐み恐みも白さく\n'
                                 '此度○○○○(祈願者氏名)い此の所に新室(にひむろ)清く麗しく建て設(まうけ)むと\n'
                                 '今日の生日の足日の朝日の豊栄昇(とよさかのぼり)に地鎮祭(とこしづめのみまつり)仕へ奉らむとす\n'
                                 '是(ここ)を以ちて大前に御食・御酒・種々の物を献奉りて乞ひ祈み奉らくは\n'
                                 '大神等の高き尊き神徳(みうつくしび)・広き厚き恩頼を蒙り奉りて\n'
                                 '工事(たくみのわざ)過つ事無く\n'
                                 '直く正しく迅く速けく事竣(ことを)へしめ給ひ\n'
                                 '掘り穿ち行かむ大地(おほとこ)の\n'
                                 '底つ岩根の極み据え置ける百千(ももち)の礎動き傾く事無く\n'
                                 '取り上ぐる棟・桁・梁・戸・窓の交錯(さか)ひ動き鳴る事無く\n'
                                 '此の工事に従ふ手人(たびと)らに手の躓(まがひ)・足の躓無く\n'
                                 '唯只管(ただひたすら)に仕へ奉らしめ給へと\n'
                                 '恐み恐みも乞ひ祈み奉らくと白す'))
    else:
        reply_text = talkapi_response(send_message)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text))

#A3RTのTalkAPIにより応答
def talkapi_response(text):
    apikey = os.environ["apikey"]
    client = pya3rt.TalkClient(apikey)
    response = client.talk(text)
    return ((response['results'])[0])['reply']

 #友達追加時イベント
@handler.add(FollowEvent)
def handle_follow(event):
   line_bot_api.reply_message(
       event.reply_token,
       TextSendMessage(text='友達追加ありがとう！よろしくお願いします！\n\n'
                            '私が何をできるか知りたかったら「機能説明」と入力してメッセージを送ってください！'))

if __name__ == "__main__":
   port = int(os.getenv("PORT"))
   app.run(host="0.0.0.0", port=port)