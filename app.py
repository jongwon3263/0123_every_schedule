import streamlit as st
import gspread
import pandas as pd
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
import os

st.set_page_config(
    page_icon="🐶",
    page_title="에브리홈 스케쥴 0.1",
    layout="wide"
)

st.json({
  "type": "service_account",
  "project_id": "gspreadtest-375317",
  "private_key_id": "2426aad55bdac0d25845b120b2b1350734f4678c",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCedgX/SvaRM9e7\nAaRPoQduK+1eIqHOFJQXlx1YeHRPBkJfk27pHEaVk69a3238IXYwVWOtu3am6nRt\nd9tsG7PPDuKaQ9aDYYCq0/F7JP9SZRYUMUhV105MkAhX+tMgsb/K15XidZZKu498\nYLv3l7RqjgIOQaIdkVY7TmbWQ7HI8Fuo7OGOtGoQOh6m0M/DyV5Lkfg/iYgf/KzG\n1G/fZe65SxDXoOSggoNn7mhfgMNHufNjCG+rtmKmrBDrUPBha9Pg1lgQ3QeUSiiB\nDs1FXm7Zc4HA3igZInocw8m1lVwb57N7v+pl+pIFREDEWdctF/LOlHuNctnWFL2A\noH9+9CDFAgMBAAECggEAA+4meO4JjpFsHOHOCwGR9xwUz5xpSfy9rZYcbrjSHbGo\njMlR22tNnuEiXM0k47eKwGklx0XajApNp/dslFJdk9mpKi1bkTemYtZN64F/6bHD\nKe4M/sAP25tI8bGxceKmwKe3On4zI5hiVzHpB5uWKHxsNaFQHY6gxmjL6S2Vp8ew\nY+e1NyCLHUFPfE3piHgSYDFW9M1zx85AuSSGvAGSr/x8LzBy8z9Lpa+zVYH0x/hG\ncVRs597c272s1K+H6Ac7/iVZH5YcweYVjgpA122zQId7Fg70ELb44xC1458QM0FZ\ndtZRc39lKi/CGJ+ELaDIfvgT6V4XC2YIL9rNt4hOQwKBgQDV8JLmyU8kzatr132i\nEGXVuX49u07RaMLJ55qRlPo0B4fQ3L3+fCL0F6AldmwTFtCwkm8BqLu+w7F9uTBq\nNYA8Vk0u6kohQe/jECUDH7b2mrIE8mIrZZDzruRBKhkBLr9VIKqJoFRpVc+pwSRK\nmpP8LTgdstepke6kjb8qR4QQswKBgQC9nT9sbRTpoe3xKGbPxtKCdzDrZQ+MY5f7\nYM0P5Rs4rVNnuALEzVJEvrrtH9d1OQNW4Ndxlljwzd6wHf131KYOizDYXl3tzPvI\n2M7go7fmIxRjSXpQYYKgVJSncHvVAn1g7MvI5udVjqGCPhe8bTJJCV8QD/68byGs\nnQy1yKPUpwKBgQCm8Sdwt73udh9B89GxWSJd+HUuLq9+cUUu0G+pEpt7ZjTxIo+P\nucZ8usLY+OO0saT/ZAUDQmvenE4wUQYams0KSD3KUkCuWwmaIcr/+QuIu4YWnh1E\nx+ioftzWjMceSSA8iVUKN/YmjDOTv4dWP/EiYxba9eecBqg19/YoQ84mSQKBgQC2\nkzL+tAnu7HywOLbGWitYdGwmPKk8BKnS4uKQ64nKiRpGRGhmF02f5AcZTA+qT7tn\nbBgGxz3coF5MNpRZTeiXGG9v522KDFZkjl6k7v+kGSMIdzfPLhUZTFfW4fhaoosX\nSOrwB2W4fB4HysIQLRS+PsfKL5yY1GkYTCBw6UDXAQKBgFb8ejdjQIxHspQ0EihL\nJ2v8UrcDO9E1999wVgOXR7RETDaqpJn7asd0h6RULeL6krPGkuA0lexvtQOZvEnf\njJudYia1udPdIEmCvnDqiQ4VArEl+FVSk01RjmUulXtCns1kxaVMrNlACjQ6SA7r\nxnfNsl6pG2Xbn9s2KQCXz+KA\n-----END PRIVATE KEY-----\n",
  "client_email": "gspread@gspreadtest-375317.iam.gserviceaccount.com",
  "client_id": "105511259535492147602",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/gspread%40gspreadtest-375317.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
})

scope = [
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive',
]

json_file_name = '/Users/gwonjong-won/Documents/0./Projects/0123_every_schedule/gspreadtest-375317-2426aad55bda.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scopes=scope, token_uri="https://oauth2.googleapis.com/token")

gc = gspread.authorize(credentials)
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1_IXE_zCjUANYAf2wKM0ektMTzqpn4SZIWm8Ct2WJ4xI/edit?usp=sharing'
doc = gc.open_by_url(spreadsheet_url)
worksheet_name = '종원작업용'
worksheet = doc.worksheet(worksheet_name)

data = worksheet.get_all_values()
data = [[col if col != '' else 'EMPTY_COLUMN' for col in row] for row in data]
df = pd.DataFrame(data[1:], columns=[col.strip() for col in data[0]])

st.write(df)
st.markdown("---")

cols = st.columns((1, 1, 1, 1))
    
region = cols[0].text_input('지역', key='시공 지역 선택')
address_ = cols[0].text_input('주소')
product_ = cols[0].text_input('상품군')
detail_ = cols[0].text_input('상세 내역')
start = cols[0].date_input('착수')
finish = cols[0].date_input('마감')
customer_phone = cols[0].text_input('고객 연락처', value=0)
company_ = cols[1].text_input('시공업체')
company_pay = cols[1].number_input('업체단가', value=0)
customer_price = cols[1].number_input('고객단가', value=0)
customer_name = cols[1].text_input('입금자명')
down_payment = cols[1].number_input('계약금', value=50000)
today = str(datetime.today())
today = today[5:11].replace("-", "/")
manager_ = cols[1].radio('담당자', options=['홍진영', '박정재'])
balance = customer_price - down_payment

day_start = str(start)
day_start = day_start.replace("-", "/")
day_start = day_start[5:]

day_finish = str(finish)
day_finish = day_finish.replace("-", "/")
day_finish = day_finish[5:]

customer_info = [region, address_, product_, detail_, day_start, day_finish, customer_phone, company_, company_pay, customer_price, customer_name, down_payment, balance, today, manager_]



message_for_worker = f"[{day_start}] 실수령 ₩ {format(company_pay, ',d')}원 \n"

if company_pay == balance:
    message_for_worker += f"> 고객 잔금 ₩ {format(balance, ',d')}원 수령해 주시고 마무리해 주시면 감사하겠습니다 :)"
elif company_pay > balance:
    message_for_worker += f"> 고객 잔금 ₩ {format(balance, ',d')}원 수령해 주시고 마무리해 주시면 차액 송금드리겠습니다."
else:
    message_for_worker += f"> 고객 잔금 ₩ {format(balance, ',d')}원 수령해 주시고 마무리 후 차액 송금해 주시면 감사하겠습니다."

message_for_worker += f"\n\n{detail_}\n\n{address_}\n{customer_phone} ({customer_name} 고객님)"

cols[2].text_area('메모장', height=500)

work_number = cols[3].text_input("엑셀 번호로 찾기")

work_number_index = int(work_number) - 1
if work_number:
    try:
        work_number_index = int(work_number) - 1
        if 0 <= work_number_index < len(data):
            v_lst = data[work_number_index]
        else:
            st.error(f"Invalid work_number: {work_number}")
    except ValueError:
        st.error(f"Invalid work_number: {work_number}")
else:
    st.error("work_number cannot be an empty string.")


seleceted_region = v_lst[0]
seleceted_address = v_lst[1]
seleceted_product = v_lst[2]
seleceted_detail = v_lst[3]
seleceted_start = v_lst[4]
str_selected_start = str(start)
str_selected_start = str_selected_start.replace("-", "/")
str_selected_start = str_selected_start[5:]
seleceted_finish = v_lst[5]
seleceted_customer_phone = v_lst[6]
seleceted_company = v_lst[7]
seleceted_company_pay = v_lst[8]
seleceted_customer_price = v_lst[9]
seleceted_customer_name = v_lst[10]
seleceted_down_payment = v_lst[11]
seleceted_balance = v_lst[12]
seleceted_contract_date = v_lst[13]
seleceted_manager = v_lst[14]


message_for_worker_2 = f"[{str_selected_start}] 실수령 {seleceted_company_pay}원 \n"

if company_pay == balance:
    message_for_worker_2 += f"> 고객 잔금 {seleceted_balance}원 수령해 주시고 마무리해 주시면 감사하겠습니다 :)"
elif company_pay > balance:
    message_for_worker_2 += f"> 고객 잔금 {seleceted_balance}원 수령해 주시고 마무리해 주시면 차액 송금드리겠습니다."
else:
    message_for_worker_2 += f"> 고객 잔금 {seleceted_balance}원 수령해 주시고 마무리 후 차액 송금해 주시면 감사하겠습니다."

message_for_worker_2 += f"\n\n{seleceted_detail}\n\n{seleceted_address}\n{seleceted_customer_phone} ({seleceted_customer_name} 고객님)"

cols[3].text_area('찾은 일정 메시지', message_for_worker_2, height=500)

if st.button('일정 추가'):
    worksheet.append_row(customer_info)
    cols[3].text_area('신규 일정 메시지', message_for_worker, height=500)