import streamlit as st
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Leer el string de conexión desde secrets
cnxString = st.secrets["MONGODB-CNX"]

def app():
    st.title('Hola!')
    st.write('Soy una IA especializada en Gestión Comercial.')
    st.write('Para empezar a conversar, déjame tu nombre y email. Usaré tu email para recordar lo que conversamos y darte respuestas más precisas!')

    # Inputs de usuario
    nombre = st.text_input('Nombre')
    email = st.text_input("Email", key="email_input", on_change=lambda: st.session_state.update({"submit": True}))

    if st.button('Empezar a Conversar!') or st.session_state.get("submit", False):
        st.session_state["submit"] = False  # Resetear el estado de activación

        # Mostrar pantalla de carga
        with st.spinner('Procesando... Por favor, espera.'):
            # Conexión a la base de datos MongoDB
            client = MongoClient(cnxString, server_api=ServerApi('1'))
            db = client["gestion_comercial"]
            usuarios_clx = db["usuarios"]

            # Preparar el filtro y datos para upsert
            filtro = {"email": email}
            datos = {
                "$set": {
                    "nombre": nombre,
                    "email": email,
                }
            }

            # Actualizar o insertar el documento en la base de datos
            resultado = usuarios_clx.update_one(filtro, datos, upsert=True)

        # Mostrar resultados en la consola
        if resultado.matched_count > 0:
            print("Documento actualizado.")
        elif resultado.upserted_id is not None:
            print(f"Documento insertado con el ID: {resultado.upserted_id}")
        else:
            print("No hubo cambios en la colección.")

        # Actualizar los valores de sesión
        st.session_state['username'] = nombre
        st.session_state['useremail'] = email

        # Recargar la aplicación para reflejar los cambios
        st.rerun()
