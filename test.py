import streamlit as st
import google.generativeai as genai
from googletrans import Translator
import time

def app():

    # CSS 스타일 정의
    st.markdown(
        """
        <style>
        .reportview-container {
            background: url("https://www.example.com/background.jpg");
            background-size: cover;
        }
        .sidebar .sidebar-content {
            background: #f0f0f5;
        }
        .css-1d391kg p {
            font-size: 20px;
            color: #333333;
        }
        .title-container {
            text-align: center;  /* 제목을 중앙 정렬로 변경 */
        }
        .title-container h1 {
            font-size: 39px;  /* 기존 크기보다 1.3배 크게 조정 */
            display: inline-block;
        }
        .input-container h2 {
            font-size: 18px;
            text-align: center;
            line-height: 1.5;
        }
        .input-container {
            max-width: 50%;
            margin: 0 auto;
        }
        .input-container input[type="text"] {
            width: 75%;  /* 입력창의 크기를 1.5배로 키웠습니다 */
            margin: 0 auto;
            display: block;
            padding: 10px;
            border: 2px solid #ff69b4;
            border-radius: 5px;
        }
        .input-container input[type="text"]::placeholder {
            color: #ff69b4;  /* 입력창의 색깔을 핑크색으로 변경했습니다 */
        }
        .button-container {
            text-align: center;  /* 버튼을 중앙 정렬로 변경 */
        }
        .button-container button {
            background-color: #87CEEB;  /* 버튼 색상을 하늘색으로 변경 */
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Google AI API 키 설정
    GOOGLE_API_KEY = "AIzaSyBvmKfof-audrEt56gzpXbJsoiyT9OE38c"
    genai.configure(api_key=GOOGLE_API_KEY)

    # Streamlit 애플리케이션 시작
    image_url = "https://i.imgur.com/7cBH3fu.png"
    st.image(image_url)
    st.markdown('<div class="title-container"><h1>냉장고를 부탁해~ 셰프봇! 🧑‍🍳</h1></div>', unsafe_allow_html=True)

    # 고정된 텍스트
    user_input = "철희님의 냉장고에 있는 재료를 적어주세요. 단 15분 동안 맛있는 요리를 같이 만들어볼까요?"

    # 입력 텍스트를 영어로 번역
    translator = Translator()
    user_input_en = translator.translate(user_input, src='ko', dest='en').text

    # 모델에 사용자 입력 전달하여 응답 생성
    if st.button("메시지 전송"):
        try:
            response = genai.generate_text(prompt=user_input_en, model="models/text-bison-001")
            response_text_en = response['candidates'][0]['output']
            response_text_ko = translator.translate(response_text_en, src='en', dest='ko').text
            st.write(response_text_ko)

            # 타이머 시작 버튼
            if st.button("타이머 시작"):
                st.write("타이머가 시작되었습니다!")
                with st.empty():
                    for seconds in range(15*60, 0, -1):
                        mins, secs = divmod(seconds, 60)
                        timer = '{:02d}:{:02d}'.format(mins, secs)
                        st.write(f"남은 시간: {timer}")
                        time.sleep(1)
                    st.write("시간이 다 되었습니다! 요리가 완성되었나요?")

        except Exception as e:
            st.write(f"오류가 발생했습니다: {e}")

if __name__ == "__main__":
    app()
