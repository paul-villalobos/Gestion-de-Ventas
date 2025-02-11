import streamlit as st
from gpt_consultant import ConsultorDeVentas


def mostrar_historial(consultant):
    """Muestra el historial de mensajes en el chat."""
    mensajes = consultant.get_session_history().messages
    for mensaje in mensajes:
        with st.chat_message("user" if mensaje.__class__.__name__ == "HumanMessage" else "assistant"):
            st.markdown(mensaje.content)


def procesar_interaccion(consultant):
    """Maneja la interacción con el usuario y la IA."""
    prompt = st.chat_input("Escribe tu mensaje")
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            st.write_stream(consultant.stream_answer(prompt))


def app():
    """Página de generación de encuestas."""
    st.title("IA Especializada en Crear Encuestas")
    st.write(
        'Objetivo: Ayudar a tu empresa a entender qué valoran tus clientes, incluyendo sus necesidades, miedos y expectativas.')
    st.write('Cómo funciona: Genera preguntas estratégicas adaptadas al sector y objetivos de tu empresa.')

    consultant = ConsultorDeVentas(session_id=st.session_state.get('useremail', 'default_session'),
                                   username=st.session_state.get('username', 'Usuario Anónimo'))

    mostrar_historial(consultant)
    procesar_interaccion(consultant)
