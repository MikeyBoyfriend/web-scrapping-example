from flask import Flask
import requests
import json

app = Flask(__name__)


def clean_req_win_output(res_text: str):
    output = 0
    count = 0
    line_result = 0
    per_line = res_text.splitlines()
    for line_index, line in enumerate(per_line):
        if line.find("₪") != -1:
            count = count + 1
            if count == 3:
                line = line.strip()
                line_result = line[29:line.find("₪")]
                output = output + int(line_result)
                count = 0
    return output

@app.route("/lotto-check/<current_lotto>")
def lotto_check(current_lotto):

    FIRST_LOTTO_PARTICIPATION = 3000
    CURRENT_LOTTO_PARTICIPATION = current_lotto
    MY_LOTTO_NUMBERS = [8,19,26,28,34,36,6]

    cookies = {
        'BIGipServerpaisfront': '890611904.20480.0000',
        'TS0181cbe7': '01400e68b2ba8ef0e7581dc755203c1db75b3d15f9d2ffd1ec27e2dbed7f47eb75061f3c3ea56269f21652b29b8e4d084918473ca5',
        '_gcl_au': '1.1.1755554378.1678895285',
        '_gid': 'GA1.3.63045263.1678895285',
        '_ga': 'GA1.1.496120336.1678895285',
        'outbrain_cid_fetch': 'true',
        '_ga_YZ88Z2NRSN': 'GS1.1.1678895285.1.1.1678895313.0.0.0',
        '_ga_NY9B0P1RZD': 'GS1.1.1678895285.1.1.1678895313.0.0.0',
    }

    headers = {
        'Host': 'www.pais.co.il',
        # 'Content-Length': '380',
        'Sec-Ch-Ua': '"Chromium";v="111", "Not(A:Brand";v="8"',
        'Accept': '*/*',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Sec-Ch-Ua-Mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.65 Safari/537.36',
        'Sec-Ch-Ua-Platform': '"Linux"',
        'Origin': 'https://www.pais.co.il',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.pais.co.il/lotto/lottowincheck/lottowininput.aspx',
        # 'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Connection': 'close',
        # 'Cookie': 'BIGipServerpaisfront=890611904.20480.0000; TS0181cbe7=01400e68b2ba8ef0e7581dc755203c1db75b3d15f9d2ffd1ec27e2dbed7f47eb75061f3c3ea56269f21652b29b8e4d084918473ca5; _gcl_au=1.1.1755554378.1678895285; _gid=GA1.3.63045263.1678895285; _ga=GA1.1.496120336.1678895285; outbrain_cid_fetch=true; _ga_YZ88Z2NRSN=GS1.1.1678895285.1.1.1678895313.0.0.0; _ga_NY9B0P1RZD=GS1.1.1678895285.1.1.1678895313.0.0.0',
    }

    params = {
        'startIndex': '0',
        'amount': '200',
    }

    data = {
        'formIndex': '0',
        'amount': '200',
        'MainGameType': 'Lotto',
        'startDate': '',
        'endDate': '',
        'startNum': FIRST_LOTTO_PARTICIPATION,
        'endNum': CURRENT_LOTTO_PARTICIPATION, # Translate later into a variable
        'gameSubType': '11',
        'gameSubTypeInputs': '1',
        'tbl-1_number-1': MY_LOTTO_NUMBERS[0],
        'tbl-1_number-2': MY_LOTTO_NUMBERS[1],
        'tbl-1_number-3': MY_LOTTO_NUMBERS[2],
        'tbl-1_number-4': MY_LOTTO_NUMBERS[3],
        'tbl-1_number-5': MY_LOTTO_NUMBERS[4],
        'tbl-1_number-6': MY_LOTTO_NUMBERS[5],
        'tbl-1_strong-1': MY_LOTTO_NUMBERS[6],
        'tbl-2_number-1': MY_LOTTO_NUMBERS[0],
        'tbl-2_number-2': MY_LOTTO_NUMBERS[1],
        'tbl-2_number-3': MY_LOTTO_NUMBERS[2],
        'tbl-2_number-4': MY_LOTTO_NUMBERS[3],
        'tbl-2_number-5': MY_LOTTO_NUMBERS[4],
        'tbl-2_number-6': MY_LOTTO_NUMBERS[5],
        'tbl-2_strong-1': MY_LOTTO_NUMBERS[6],
    }

    req_res = requests.post(
        'https://www.pais.co.il/lotto/LottoWinCheck/WinCheckForm.aspx',
        params=params,
        cookies=cookies,
        headers=headers,
        data=data,
        verify=False,
    )

    accamulated_wins = 0
    accamulated_wins = accamulated_wins + clean_req_win_output(res_text=req_res.text)
    message = '{"Accumulated wins:":"'+accamulated_wins.__str__()+'"}'
    return json.loads(message)

@app.route("/")
def welcome():
    message = '{"Mike":"Hello World","the current server is":"operational"}'
    return json.loads(message)
