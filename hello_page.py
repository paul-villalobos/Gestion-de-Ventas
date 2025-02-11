import streamlit as st
from pymongo import MongoClient
from pymongo.server_api import ServerApi


def conectar_bd():
    """Establece la conexión con MongoDB usando la cadena de conexión de Streamlit secrets."""
    cnx_string = st.secrets["MONGODB-CNX"]
    return MongoClient(cnx_string, server_api=ServerApi('1'))


def guardar_usuario(nombre: str, email: str, website: str):
    """Guarda o actualiza la información del usuario en la base de datos."""
    client = conectar_bd()
    db = client["gestion_comercial"]
    usuarios_clx = db["usuarios"]

    filtro = {"email": email}
    datos = {"$set": {"nombre": nombre, "email": email, "website": website}}

    usuarios_clx.update_one(filtro, datos, upsert=True)


def app():
    """Interfaz de bienvenida para los usuarios."""
    st.title('¡Hola!')
    st.write('Soy Paul Villalobos')
    st.write(
        'Ayudo a empresas a potenciar sus Estrategias Comerciales a través de tecnología, datos y procesos eficientes.')
    st.write(
        'Pongo a tu disposición algunas herramientas de IA Generativa especializada en Ventas. ¡Ingresa tus datos para comenzar!')

    # Inputs de usuario
    nombre = st.text_input('Nombre')
    email = st.text_input("Email", key="email_input")
    website = st.text_input("Opcional: Página Web")

    if st.button('Empezar a Conversar!'):
        with st.spinner('Procesando... Por favor, espera.'):
            guardar_usuario(nombre, email, website)

        # Actualizar valores de sesión
        st.session_state.update({
            'username': nombre,
            'useremail': email,
            'website': website
        })

        # Recargar la aplicación para reflejar los cambios
        st.rerun()
