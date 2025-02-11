import streamlit as st
from streamlit_option_menu import option_menu

import hello_page, generar_encuesta_page

st.set_page_config(
    page_title="IA de Paul"
)

# Inicializar el estado de sesión para el usuario si no existe
st.session_state.setdefault('useremail', None)
is_logged_in = bool(st.session_state['useremail'])
# print("Is Logged In:", is_logged_in)

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })

    def run(self):

        with st.sidebar:
            if is_logged_in:
                app = option_menu(
                menu_title="Asistente IA",
                options=["Generar Encuesta"],
                icons=["check2-square"],
                default_index=0,
            )
            else:
                app = option_menu(
                menu_title="Asistente IA",
                options=["Hola"],
                icons=["house-fill"],
                default_index=0,
            )

        if app == "Hola":
            hello_page.app()
        if app == "Generar Encuesta":
            generar_encuesta_page.app()

if __name__ == "__main__":
    app = MultiApp()
    app.run()