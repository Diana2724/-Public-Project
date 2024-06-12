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
  
