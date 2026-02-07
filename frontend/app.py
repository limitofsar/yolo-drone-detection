import streamlit as st
import requests
import time

BACKEND_URL = "http://127.0.0.1:8000"

# Получение моделей
@st.cache_data
def fetch_models():
    r = requests.get(f"{BACKEND_URL}/models")
    r.raise_for_status()
    return r.json()["models"]

st.set_page_config(page_title="YOLO Video Detection", layout="centered")
st.title("YOLO Video Detection")

models = fetch_models()
model_choice = st.selectbox("Модель", models, key="model_choice")

with st.expander("⚙️ Настройки детекции", expanded=False):
    line_width = st.number_input(
        "Толщина линий (line_width)",
        min_value=1,
        max_value=20,
        value=2,
        step=1,
        key="line_width_input"
    )

# session_state
if "video_bytes" not in st.session_state:
    st.session_state.video_bytes = None
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
if "task_id" not in st.session_state:
    st.session_state.task_id = None

# File uploader
uploaded = st.file_uploader(
    "Загрузите видео",
    type=["mp4", "avi", "mov"],
    key="uploaded_video"
)

# Если загружен новый файл, обновляем session_state
if uploaded is not None:
    if st.session_state.uploaded_file != uploaded:
        st.session_state.uploaded_file = uploaded
        st.session_state.video_bytes = None
        st.session_state.task_id = None
    st.video(uploaded)
else:
    # Если пользователь реально удалил файл, сброс результата
    if st.session_state.uploaded_file is not None:
        st.session_state.video_bytes = None
        st.session_state.task_id = None
        st.session_state.uploaded_file = None

# Кнопка Detect
if uploaded and st.button("Detect", key="detect_button"):
    files = {"file": uploaded.getvalue()}
    data = {"model_name": model_choice, "line_width": int(line_width)}

    r = requests.post(f"{BACKEND_URL}/upload", files={"file": uploaded}, data=data)
    st.session_state.task_id = r.json()["task_id"]

    progress_bar = st.progress(0)
    progress_text = st.empty()

    while True:
        status = requests.get(f"{BACKEND_URL}/status/{st.session_state.task_id}").json()
        percent = int(status.get("progress", 0))
        state = status.get("status")

        progress_bar.progress(percent)
        progress_text.markdown(f"**Progress:** {percent}%")

        if state == "done":
            progress_text.markdown("✅ **Ready: 100%**")
            break
        if state == "error":
            progress_text.markdown("❌ **Ошибка обработки**")
            break
        time.sleep(1)

    # Сохраняем результат независимо от uploaded
    res = requests.get(f"{BACKEND_URL}/result/{st.session_state.task_id}")
    st.session_state.video_bytes = res.content

# Отображение результата
if st.session_state.video_bytes:
    st.video(st.session_state.video_bytes)
    st.download_button(
        label="💾 Download",
        data=st.session_state.video_bytes,
        file_name="processed_video.mp4",
        mime="video/mp4",
        key="download_button"
    )
