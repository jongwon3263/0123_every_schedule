import streamlit as st
import gspread
import pandas as pd
from datetime import datetime
from google.oauth2.service_account import Credentials
import json
import os

st.set_page_config(
    page_title="에브리홈 스케쥴 0.1",
    layout="wide"
)


scope = [
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive',
]

json_file_path = os.path.abspath('/Users/gwonjong-won/Documents/0./Projects/0123_every_schedule/gspreadtest-375317-2426aad55bda.json')

st.write(f"Is the file present? {os.path.exists(json_file_path)}")
with open(json_file_path, 'r') as json_file:
    credentials_info = json.load(json_file)

credentials = Credentials.from_service_account_info(credentials_info, scopes=scope)

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