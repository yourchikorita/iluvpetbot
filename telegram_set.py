from urllib.request import Request, urlopen

## https://core.telegram.org/bots/api#getupdates

API_KEY = '764462849:AAER9m2z9X4jRkQ4SYycPUo91o16fXxIzhk'  #iluvpet
WEBHOOK_URL = 'https://iluvpet.herokuapp.com'# iluvpet
#API_KEY = '916473331:AAHDtuAaRcGM8FlPRFUYDGRzY6mgyDWacuo' #gonnabeok
#WEBHOOK_URL = 'https://d6ed15e7.ap.ngrok.io'
BOT_INFO_URL = 'https://api.telegram.org/bot{API_KEY}/getMe'.format(API_KEY=API_KEY)
BOT_UPDATE_URL = 'https://api.telegram.org/bot{API_KEY}/getUpdates?offset=1'.format(API_KEY=API_KEY)
BOT_SET_WEBHOOK_URL = 'https://api.telegram.org/bot{API_KEY}/setWebhook?url={WEBHOOK_URL}'\
    .format(API_KEY=API_KEY, WEBHOOK_URL=WEBHOOK_URL)
BOT_DELETE_URL = 'https://api.telegram.org/bot{API_KEY}/deleteWebhook'.format(API_KEY=API_KEY)
BOT_GET_INFO_URL='https://api.telegram.org/bot{API_KEY}/getWebhookInfo'.format(API_KEY=API_KEY)

def bot_info_call():
    """
    bot 의 정보를 출력하는 함수 
    """
    request = Request(BOT_INFO_URL)
    request.get_method = lambda: 'GET'
    response_body = urlopen(request).read().decode('utf-8')
    print(response_body)


def bot_update_call():
    """
    bot 의 업데이트 정보를 출력하는 함수 
    """
    request = Request(BOT_UPDATE_URL)
    request.get_method = lambda: 'GET'
    response_body = urlopen(request).read().decode('utf-8')
    print(response_body)


def bot_set_webhook_call():
    """
    bot 의 Webhook 을 세팅하는 함수
    """
    request = Request(BOT_SET_WEBHOOK_URL)
    request.get_method = lambda: 'GET'
    response_body = urlopen(request).read().decode('utf-8')
    print(response_body)


def delete_webhook():
    """
    bot 의 Webhook 을 제거하는 함수
    """
    request = Request(BOT_DELETE_URL)
    request.get_method = lambda: 'GET'
    response_body = urlopen(request).read().decode('utf-8')
    print(response_body)

def get_webhook_info():
    """
    bot 의 Webhook 인포 함수
    """
    request = Request(BOT_GET_INFO_URL)
    request.get_method = lambda: 'GET'
    response_body = urlopen(request).read().decode('utf-8')
    print(response_body)
    
    
#bot_set_webhook_call()
bot_set_webhook_call()


#이전데이타 지우는법
#1.delete하고
#2. offset=1로해서  update() 실행하고,offset=1이면 첨부터 다보는것..
#2-1, 맨마지막 결과에서 위에걸로 update_id 번호 복사해서 offset=번호 로 하고 , 
#3. update 다시실행하고 , get_webhook_info 실행해서 결과 확인 