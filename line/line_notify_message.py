#pip
# pip
import requests



def lineNotifyMessage(token='lkGIyFAxVcJcW9qswWggKzarqaTGQJu9QkqjksmcdKD', msg='Notify from LINE, HELLO WORLD'):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code




def main():

    lineNotifyMessage(token='zqTJF3vTvJbTHwkmKs9J74PPdX8iuNwwM9ix8SGKGqG')

if __name__ == '__main__':

    main()
    print('Complete!!!!!!!!!!')