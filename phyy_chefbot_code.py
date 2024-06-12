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
            text-align: center;
        }
        .title-container h1 {
            font-size: 39px;
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
            width: 75%;
            margin: 0 auto;
            display: block;
            padding: 10px;
            border: 2px solid #ff69b4;
            border-radius: 5px;
        }
        .input-container input[type="text"]::placeholder {
            color: #ff69b4;
        }
        .button-container {
            text-align: center;
        }
        .button-container button {
            background-color: #87CEEB;
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
        .button-container .red-button {
            background-color: #FF6347;
        }
        .timer {
            font-size: 150px;
            text-align: center;
            color: #333;
        }
        .fireworks {
            position: fixed;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            display: none;
        }
        .firework {
            width: 5px;
            height: 5px;
            background-color: #ff0;
            position: absolute;
            animation: fireworks 1s linear infinite;
        }
        @keyframes fireworks {
            0% { transform: scale(1); opacity: 1; }
            100% { transform: scale(0.1); opacity: 0; }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Google AI API 키 설정
    GOOGLE_API_KEY = "AIzaSyBvmKfof-audrEt56gzpXbJsoiyT9OE38c"
    genai.configure(api_key=GOOGLE_API_KEY)

    if 'page' not in st.session_state:
        st.session_state['page'] = 'input_name'

    if st.session_state['page'] == 'input_name':
        image_url = "https://i.imgur.com/7cBH3fu.png"
        st.image(image_url)
        st.markdown('<div class="title-container"><h1>냉장고를 부탁해~ 셰프봇! 🧑‍🍳</h1></div>', unsafe_allow_html=True)
        st.session_state['user_name'] = st.text_input("이름을 입력하세요", key='name_input')

        if st.button("이름 전송"):
            if st.session_state['user_name']:
                st.session_state['page'] = 'input_ingredients'

    elif st.session_state['page'] == 'input_ingredients':
        userName = st.session_state['user_name']
        st.markdown(f"### {userName}님의 냉장고를 부탁해~ 셰프봇! 🧑‍🍳")

        # 사용자 입력 받기
        user_input = st.text_input(f"{userName}님의 냉장고 속 재료를 적어주세요. 15분동안 맛있는 요리를 같이 만들어볼까요?", key='ingredients_input')

        if user_input:
            # 번역기 설정
            translator = Translator()

            # '메시지 전송' 버튼 클릭 시 동작
            if st.button("메시지 전송", key='send_message'):
                try:
                    # 입력 텍스트를 영어로 번역
                    user_input_en = translator.translate(user_input, src='ko', dest='en').text

                    # 모델에 사용자 입력 전달하여 응답 생성
                    response = genai.generate_text(prompt=user_input_en, model="models/text-bison-001")
                    response_text_en = response.candidates[0]['output']
                    response_text_ko = translator.translate(response_text_en, src='en', dest='ko').text

                    # 생성된 응답 출력 형식화
                    st.write(response_text_ko.replace("\\n", "\n"))
                except Exception as e:
                    st.write(f"오류가 발생했습니다: {e}")

            # '요리 만들기 시작' 버튼 클릭 시 동작
            if st.button("요리 시작", key='start_cooking'):
                st.session_state['page'] = 'timer'

    elif st.session_state['page'] == 'timer':
        st.markdown('<div class="title-container"><h1>타이머</h1></div>', unsafe_allow_html=True)
        st.write("타이머가 시작되었습니다!")

        if 'timer_start' not in st.session_state:
            st.session_state['timer_start'] = time.time()

        with st.empty():
            while True:
                elapsed_time = int(time.time() - st.session_state['timer_start'])
                remaining_time = max(15*60 - elapsed_time, 0)
                mins, secs = divmod(remaining_time, 60)
                timer = '{:02d}:{:02d}'.format(mins, secs)
                st.markdown(f'<div class="timer">{timer}</div>', unsafe_allow_html=True)
                time.sleep(1)

                if remaining_time == 0 or st.button("요리 완성", key='complete_cooking'):
                    st.session_state['page'] = 'fireworks'
                    break

    elif st.session_state['page'] == 'fireworks':
        st.markdown('<div class="title-container"><h1>축하합니다! 요리가 완성되었습니다! 🎉</h1></div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="fireworks">
                <div class="firework" style="top: 50%; left: 50%;"></div>
                <div class="firework" style="top: 30%; left: 70%;"></div>
                <div class="firework" style="top: 80%; left: 20%;"></div>
                <div class="firework" style="top: 60%; left: 80%;"></div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.write("다시 시작하려면 페이지를 새로고침하세요.")

if __name__ == "__main__":
    app()
