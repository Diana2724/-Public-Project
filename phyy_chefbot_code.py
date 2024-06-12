import streamlit as st
import google.generativeai as genai

# gData 모듈 대신 이름을 하드코딩
user_name = "사용자"

def check_google_generativeai():
    try:
        import google.generativeai as genai
        return True
    except ImportError:
        return False

def app():
    if not check_google_generativeai():
        st.write("google-generativeai 패키지가 설치되지 않았습니다. 'pip install google-generativeai' 명령어를 사용하여 설치하세요.")
        return

    # Google AI API 키 설정
    GOOGLE_API_KEY = "AIzaSyBvmKfof-audrEt56gzpXbJsoiyT9OE38c"
    genai.configure(api_key=GOOGLE_API_KEY)

    # 이미지 URL에서 직접 로드
    image_url = "https://i.imgur.com/7cBH3fu.png"

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

    # 로고 이미지 표시
    st.image(image_url, use_column_width=True)

    # Streamlit 애플리케이션 시작
    st.markdown('<div class="title-container"><h1>냉장고를 부탁해~ 셰프봇! 🧑‍🍳</h1></div>', unsafe_allow_html=True)

    # 사용자 입력 받기
    user_input = st.text_input(f"{user_name}님의 냉장고에 있는 재료를 적어주세요 15분만에 맛있는 요리를 같이 만들어볼까요?")
    user_input = "\"" + user_input + "\"" + " 따옴표 안에 음식재료가 있다면 재료로 15분 내로 만들 수 있는 레시피와 요리이름을 알려줘 하지만 음식으로 사용할 수 없는 재료라면 \"잘못된 재료입니다\"라고만 응답해"

    # '전송' 버튼 클릭 시 동작
    if st.button("메시지 전송"):
        try:
            # 모델에 사용자 입력 전달하여 응답 생성
            response = genai.generate_text(prompt=user_input, model="models/text-bison-001")
            # 생성된 응답 출력
            response_text = response.candidates[0]['text']
            st.write(response_text)
        except Exception as e:
            st.write(f"오류가 발생했습니다: {e}")

if __name__ == "__main__":
    app()
