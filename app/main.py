from flask import Flask, request
import json
from selenium import webdriver
import os
# import pandas_datareader.data as web
# from kospi import search_kospi


# 메인 로직!! 
def cals(opt_operator, number01, number02):
    if opt_operator == "addition":
        return number01 + number02
    elif opt_operator == "subtraction": 
        return number01 - number02
    elif opt_operator == "multiplication":
        return number01 * number02
    elif opt_operator == "division":
        return number01 / number02

# 코스피 
def search_kospi(): 
    # # # print("hello")
    # chrome_options = webdriver.ChromeOptions()
    # # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--no-sandbox")

    # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

    # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    # driver.get("https://finance.naver.com/sise/sise_index.naver?code=KOSPI")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    # driver = webdriver.Chrome()
    driver.get("https://finance.naver.com/sise/sise_index.naver?code=KOSPI")



    # ## target1 : 코스피 지수
    fir= "now_value"
    # target1= driver.find_element_by_css_selector(fir).text
    target1 = driver.find_element_by_id(fir).text
    print(target1)

    # # ## target2 : 전일 대비
    # sec= ".fluc"
    # target2= driver.find_elements_by_css_selector(sec)[0].text
    # # print(target2)
    
    # # print(target2.split(" "))
    # # print(target2)
    # target2_split = target2.split(" ")
    # target2_split.insert(0, target1)
    # print(target2_split)


  
    # # # 종료 단계
    driver.close()

    return target1
    # print("kospi end...")
    # target2_split = "test3"

    # return target2_split
# search_kospi()

# 코스닥
def search_kosdaq(): 
    # print("kosdaq hello")

    driver = webdriver.Chrome()
    driver.get("https://finance.naver.com/sise/sise_index.naver?code=KOSDAQ")

    ## target1 : 코스닥 지수
    fir= "now_value"
    # target1= driver.find_element_by_css_selector(fir).text
    target1 = driver.find_element_by_id(fir).text
    print(target1)

    ## target2 : 전일 대비
    sec= ".fluc"
    target2= driver.find_elements_by_css_selector(sec)[0].text
    # print(target2)
    
    # print(target2.split(" "))
    # print(target2)
    target2_split = target2.split(" ")
    target2_split.insert(0, target1)
    print(target2_split)

    # # 종료 단계
    driver.close()


    print("kosdaq end...")
# search_kosdaq()

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Worlds3!!'

# 카카오톡 텍스트형 응답
@app.route('/api/sayHello', methods=['POST'])
def sayHello():
    body = request.get_json() # 사용자가 입력한 데이터
    print(body)
    print(body['userRequest']['utterance'])

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "안녕 hello I'm Ryan"
                    }
                }
            ]
        }
    }

    return responseBody


# 카카오톡 이미지형 응답
@app.route('/api/showHello', methods=['POST'])
def showHello():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleImage": {
                        "imageUrl": "https://t1.daumcdn.net/friends/prod/category/M001_friends_ryan2.jpg",
                        "altText": "hello I'm Ryan"
                    }
                }
            ]
        }
    }

    return responseBody


# 카카오톡 Calculator 계산기 응답
@app.route('/api/calCulator', methods=['POST'])
def calCulator():
    body = request.get_json()
    print(body)
    params_df = body['action']['params']
    print(type(params_df))
    opt_operator = params_df['operators']
    number01 = json.loads(params_df['sys_number01'])['amount']
    number02 = json.loads(params_df['sys_number02'])['amount']

    print(opt_operator, type(opt_operator), number01, type(number01))

    answer_text = str(cals(opt_operator, number01, number02))

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": answer_text
                        # "text": "answer_text"
                    }
                }
            ]
        }
    }

    return responseBody

# 코스피 크롤링 
@app.route('/api/kospi', methods=['POST'])
def kospi():
    # body = request.get_json()
    # print(body)
    # print(body['userRequest']['utterance'])
    ans_text = str(search_kospi())



    responseBody = {
        "version": "2.0",
        "template": {
             "outputs": [
                {
                    "simpleText": {
                        "text": ans_text
                    }
                }
            ]
        }
    }

    return responseBody

# 카카오톡 크롤링 응답
@app.route('/api/crawling', methods=['POST'])
def crawling():
    body = request.get_json() # 사용자가 입력한 데이터
    # print(body)
    # print(body['userRequest']['utterance'])

    # # 국내 주식 검색
    # # naver finance에서 추출
    item_code = "005930"
    # target_data = web.DataReader(item_code, 'naver')
    # last = (target_data.shape[0])
    # now_data = target_data.iloc[last - 1]
    # now_data = now_data.loc["Close"]
    # print(now_data)
    # now_data = "현재 주식의 가격은 " + now_data + "원입니다."

    responseData = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        # "text": now_data
                        "text": "now_data"
                    }
                }
            ]
        }
    }

    return responseData