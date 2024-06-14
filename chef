import streamlit as st
import google.generativeai as genai
from googletrans import Translator
import time
import re

def format_recipe(text):
    ingredients_match = re.search(r'재료:\s*(.*?)\s*조리법:', text, re.DOTALL)
    instructions_match = re.search(r'조리법:\s*(.*)', text, re.DOTALL)
    
    formatted_text = ""

    if ingredients_match:
        ingredients = ingredients_match.group(1).strip().split('\n')
        formatted_text += "### 재료:\n"
        for item in ingredients:
            formatted_text += f"- {item.strip()}\n"

    if instructions_match:
        instructions = instructions_match.group(1).strip().split('\n')
        formatted_text += "\n### 조리법:\n"
        for i, step in enumerate(instructions, 1):
            formatted_text += f"{i}. {step.strip()}\n"

    return formatted_text

def app():
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
        </style>
        """,
        unsafe_allow_html=True
    )

    # Google AI API 키 설정
    GOOGLE_API_KEY = "AIzaSyBvmKfof-audrEt56gzpXbJsoiyT9OE38c"
    genai.configure(api_key=GOOGLE_API_KEY)

    # 번역기 초기화
    translator = Translator()

    # Streamlit 애플리케이션 시작
    if 'page' not in st.session_state:
        st.session_state['page'] = 'input_name'

    if st.session_state['page'] == 'input_name':
        image_url = "https://i.imgur.com/7cBH3fu.png"
        st.image(image_url)
        st.markdown('<div class="title-container"><h1>냉장고를 부탁해~ 셰프봇! 🧑‍🍳</h1></div>', unsafe_allow_html=True)
        st.session_state['user_name'] = st.text_input("이름을 입력하세요", key='name_input')
        st.session_state['gender'] = st.radio("성별을 선택하세요", ('남자', '여자'))

        if st.button("이름 전송", key='submit_name'):
            if st.session_state['user_name']:
                st.session_state['page'] = 'input_ingredients'
                st.experimental_rerun()

    elif st.session_state['page'] == 'input_ingredients':
        userName = st.session_state['user_name']
        st.markdown(f"### {userName}님의 냉장고를 부탁해~ 셰프봇! 🧑‍🍳")

        # 사용자 입력 받기
        user_input = st.text_input(f"{userName}님의 냉장고 속 재료를 적어주세요. 15분동안 맛있는 요리를 같이 만들어볼까요?", key='ingredients_input')

        if st.button("메시지 전송", key='send_message'):
            if user_input:
                try:
                    # 입력 텍스트를 영어로 번역
                    user_input_en = translator.translate(user_input, src='ko', dest='en').text

                    # 모델에 사용자 입력 전달하여 응답 생성
                    response = genai.generate_text(prompt=user_input_en, model="models/text-bison-001")
                    #st.write("API 응답: ", response)  # 응답 내용 출력

                    response_text_en = response.candidates[0]['output'] if response.candidates else "응답을 생성할 수 없습니다."

                    # 응답을 한국어로 번역
                    response_text_ko = translator.translate(response_text_en, src='en', dest='ko').text

                    # 생성된 응답 출력 형식화
                    formatted_response = format_recipe(response_text_ko)
                    st.markdown(formatted_response)
                    st.write("번역된 응답: ", response_text_ko)  # 번역된 응답 출력

                    if 'recipe_generated' not in st.session_state:
                        st.session_state['recipe_generated'] = True

                except Exception as e:
                    st.write(f"오류가 발생했습니다: {e}")

        if 'recipe_generated' in st.session_state and st.session_state['recipe_generated']:
            if st.button("요리 시작", key='start_cooking'):
                st.session_state['page'] = 'timer'
                st.session_state['timer_start'] = time.time()
                st.experimental_rerun()

    elif st.session_state['page'] == 'timer':
        userName = st.session_state['user_name']
        gender = st.session_state['gender']
        emoji = "🧑‍🍳" if gender == '남자' else "👩‍🍳"
        st.markdown(f'<div class="title-container"><h1>{userName}님은 지금 맛있는 요리중 {emoji}</h1></div>', unsafe_allow_html=True)

        if 'timer_start' not in st.session_state:
            st.session_state['timer_start'] = time.time()

        timer_placeholder = st.empty()
        complete_button_placeholder = st.empty()

        while True:
            elapsed_time = int(time.time() - st.session_state['timer_start'])
            remaining_time = max(15*60 - elapsed_time, 0)
            mins, secs = divmod(remaining_time, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            timer_placeholder.markdown(f'<div class="timer">{timer}</div>', unsafe_allow_html=True)

            if complete_button_placeholder.button("요리 완성", key=f'complete_cooking_{remaining_time}'):
                st.session_state['page'] = 'celebration'
                st.experimental_rerun()
                break

            if remaining_time == 0:
                st.session_state['page'] = 'celebration'
                st.experimental_rerun()
                break

            time.sleep(1)

    elif st.session_state['page'] == 'celebration':
        st.markdown('<div class="title-container"><h1>축하합니다! 이제 행복한 식사를 즐기세요~!</h1></div>', unsafe_allow_html=True)
        st.balloons()
        st.session_state.step = 0

if __name__ == "__main__":
    app()
