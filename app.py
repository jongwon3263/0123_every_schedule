import streamlit as st
import gspread
import pandas as pd
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
import json

st.set_page_config(
    page_icon="🐶",
    page_title="에브리홈 스케쥴 0.1",
    layout="wide"
)

# jsonFile = os.environ.get("JSON_KEY_PATH")
# st.write(f"JSON_KEY_PATH: {jsonFile}")
jsonFile = 'everyhome01gspread-e4a88aeaed19.json'

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
    ]


credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonFile, scope)
gc = gspread.authorize(credentials)
spreadsheet_key = '1_IXE_zCjUANYAf2wKM0ektMTzqpn4SZIWm8Ct2WJ4xI'
doc = gc.open_by_key(spreadsheet_key)
worksheet_name = '0318_jongwon'
worksheet = doc.worksheet(worksheet_name)

data = worksheet.get_all_values()
data = [[col if col != '' else 'EMPTY_COLUMN' for col in row] for row in data]
columns = [col.strip() for col in data[0]]
df = pd.DataFrame(data[1:], columns=columns)

# 데이터 프레임의 인덱스를 구글 시트의 행 번호로 설정
df.index = [str(i + 1) for i in range(len(df))]


st.header("일정 추가")
cols = st.columns((1, 1, 1, 1))
    
region = cols[0].text_input('지역', key='시공 지역 선택')
address_ = cols[0].text_input('주소')

# 상품군 선택 라디오 버튼 추가
product_group_selection = cols[0].radio('상품군', options=['청소', '직접 입력'])

# 상품군 선택에 따른 상품군 입력 필드 동작 변경
if product_group_selection == '청소':
    product_ = '청소'  # '청소'를 자동으로 입력
else:
    product_ = cols[0].text_input('')  # 사용자가 직접 입력
    
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

work_number = cols[3].text_input("엑셀 번호로 찾기(엑셀의 실제 행 번호 입력)", value=1)

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
    
st.markdown("---")
st.header("일정 조회")



current_year = datetime.now().year
df['마감_변환'] = pd.to_datetime(df['마감'].apply(lambda x: f"{current_year}/{x}"), format='%Y/%m/%d')  # '마감' 컬럼의 날짜 형식에 맞게 조정

# 가장 늦은 마감 날짜 찾기
latest_finish_date = df['마감_변환'].max()
cols2 = st.columns((1, 1, 1, 1))
# 사용자로부터 날짜 범위 입력 받기
start_date = cols2[0].date_input("마감일")
end_date = cols2[1].date_input("", value=latest_finish_date)

# 사용자로부터 검색 키워드 입력 받기
search_query = st.text_input("검색어를 입력하세요")

# '조회' 버튼 추가
if st.button('조회'):
    # 날짜 필터링
    mask_date = (df['마감_변환'] >= pd.Timestamp(start_date)) & (df['마감_변환'] <= pd.Timestamp(end_date))

    # 키워드가 입력되었으면 키워드 필터링 적용
    if search_query:
        mask_keyword = df.apply(lambda row: row.astype(str).str.contains(search_query, case=False, na=False).any(), axis=1)
        mask_combined = mask_date & mask_keyword
    else:
        mask_combined = mask_date

    # 필터링된 데이터 프레임을 표시
    filtered_df = df[mask_combined]
    st.subheader("검색 결과")
    st.dataframe(filtered_df.drop(columns=['마감_변환']), height=1000)  # 임시로 추가한 날짜 변환 컬럼을 제외하고 표시
else:
    st.write("검색어와 날짜 범위를 입력하고 '조회' 버튼을 클릭하면 결과가 표시됩니다.")
    
st.markdown("---")
expander = st.expander("전체 일정 보기")
expander.write(df)