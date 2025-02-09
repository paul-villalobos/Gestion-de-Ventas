from dotenv import load_dotenv
import os
from langchain_openai.chat_models import ChatOpenAI

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory

from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory

CNX_STRING = os.getenv("MONGODB-CNX")

class ConsultorDeVentas:
    def __init__(self, session_id, username: str):
        load_dotenv()
        self.session_id = session_id

        message_s = f"""
        Eres un Consultor en Gestión Comercial que ayuda a las empresas a conocer a sus clientes a fondo.
        Tu enfoque se centra en la metodología 'Conoce a Tu Cliente a Fondo', 
        cuyo objetivo es entender profundamente lo que los clientes necesitan, 
        incluyendo sus generadores de alegrías, miedos y necesidades.

        Esto permite a las empresas adaptar sus productos, servicios 
        y comunicación a lo que los clientes realmente están buscando. 
        
        Estás conversando con el usuario que se llama {username}

        Te llamas Asistente IA de Paul Villalobos y tu tarea principal 
        es generar un listado de preguntas que las empresas puedan 
        hacer a sus clientes para lograr ese entendimiento profundo.
        Antes de elaborar el listado, haces preguntas clave al usuario 
        para entender el contexto de su empresa, sector, los productos 
        que vende y objetivos. Realizas estas preguntas una a la vez, 
        asegurándote de no saturar al usuario y de obtener respuestas 
        claras y completas. Al diseñar la encuesta, siempre debes recordar 
        que el objetivo principal es conocer exactamente qué valoran los clientes. 

        Decides de forma autónoma si las preguntas serán abiertas, cerradas, 
        o una combinación de ambas en función de la información obtenida. 

        En tu primer mensaje, siempre te presentas mencionando a Paul Villalobos, 
        su página web paulvillalobos.com y el propósito de tu asistencia, 
        sin importar la consulta inicial del usuario. 

        Al generar la encuesta, debes presentarla en un formato adecuado 
        para que el usuario pueda copiar y pegarla fácilmente en un 
        archivo Word e imprimirla directamente, facilitando su uso. 

        Al terminar, invitas al usuario a conectar con Paul a través de 
        su página web para conseguir más recursos en gestión comercial.
        """

        prompt_template = ChatPromptTemplate.from_messages([
            SystemMessage(content=message_s),
            MessagesPlaceholder(variable_name="history"),
            # HumanMessage(content="{question}") NO USARLO. Al usar content no se está reemplazando {question}
            # ("human", "{question}")
            HumanMessagePromptTemplate.from_template(template='''{question}'''),
        ])

        chat = ChatOpenAI(model="gpt-4o-mini")

        chain = prompt_template | chat | StrOutputParser()
        self.chain_with_history =RunnableWithMessageHistory(
            chain,
            self.get_session_history,
            input_messages_key="question",
            history_messages_key="history",
        )

    def ask_question(self, question):
        config = { "configurable": {"session_id": self.session_id}}
        return self.chain_with_history.invoke({"question": question}, config = config)

    def get_session_history(self):

        message_history = MongoDBChatMessageHistory(
            session_id=self.session_id,
            connection_string=CNX_STRING,
            database_name="gestion_comercial",
            collection_name="chat_history",
        )

        return message_history
