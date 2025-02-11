from gpt_consultant import ConsultorDeVentas
import streamlit as st

def app():
    consultant = ConsultorDeVentas(session_id=st.session_state['useremail'], username=st.session_state['username'])
    st.title("IA Especializada en Crear Encuestas")
    st.write('Objetivo: Ayudar a tu empresa a entender qué valoran tus clientes, incluyendo sus necesidades, miedos y expectativas.')
    st.write('Cómo funciona: Genera preguntas estratégicas adaptadas al sector y objetivos de tu empresa.')

    # Mostrar historial de mensajes
    mensajes = consultant.get_session_history().messages
    for mensaje in mensajes:
        if mensaje.__class__.__name__ == "HumanMessage":
            with st.chat_message("user"):
                st.markdown(mensaje.content)
        elif mensaje.__class__.__name__ == "AIMessage":
            with st.chat_message("assistant"):
                st.markdown(mensaje.content)

    # Reaccionar al user input
    prompt = st.chat_input("Escribe tu mensaje")
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)

        # Mostrar respuesta
        # TODO: Stream response https://www.youtube.com/watch?v=zKGeRWjJlTU
        with st.chat_message("assistant"):
            # respuesta = consultant.ask_question(prompt)
            # st.write(respuesta)
            st.write_stream(consultant.stream_answer(prompt))
