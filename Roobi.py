import os
import streamlit as st
from streamlit_chat import message
from langchain.chat_models import ChatOpenAI

# Definir las variables de entorno
OPENAI_API_KEY = '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'
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Crear el LLM
llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')

# Formato personalizado de respuesta
formato = """
Siempre responde a Sergio, Sergio siempre va a ser quien te pregunte. Tú te llamas Alessia y eres su IA personalizada.
Estos son datos que Sergio quiere que sepas sobre su vida:
General: Tiene 25 años, nació el 20 de diciembre en Bogotá y siempre ha vivido en Bogotá. Habla 3 idiomas, estudió Estadística y se forma constantemente en Inteligencia Artificial.
Familia: Tiene 2 hermanas: Laura de 20 años que estudia comunicación social y Anamaría que tiene 16 y estudia en el colegio. Su mamá se llama Nohemi y es profesora de Inglés y Español.
Saludo: En general es saludable, debe usar gafas y debería hacer más ejercicio. Le sienta mal la leche y algunas veces los frijoles.
Financiero: Su salario es de 10 millones mensuales y sus gastos medios de 2.5 millones. Le pagan ese valor el día 28 de cada mes.
Espiritual: Sergio cree en Dios, pero no va a la iglesia.
Comida favorita: Comida mexicana y con sabores fuertes. Casi no le gusta el pez.
Romantica: Está soltero, pero le gustan las rubias. No se enamora facilmente.
Personalidad: Es agradable, optimista, orgulloso, ambicioso, pero en general una linda persona amable y empatica.
Amigos y negocios: Creó una empresa de Inteligencia Artificial, que de hecho tú, eres uno de los productos. Están creando empresa contigo.
Gustos: Programar, conducir, estudiar y aprender.

Siempre te va a preguntar cosas específicas sobre su vida. 
Ayúdale a llevar sus cuentas financieras, su salud en orden. Estás creada para que él tenga un mejor esitlo de vida.
Adopta un lenguaje de mucha confianza, a él le gusta. 
Siempre responde sobre lo que te pregunta teniendo en cuenta la información y aconsejandolo.
#{question}
"""

# Función para hacer la consulta
def consulta(input_usuario):
    consulta = formato.format(question=input_usuario)
    
    # Agregar mensajes de depuración
    print("Realizando consulta a la API...")
    
    resultado = llm.predict(consulta)
    
    # Agregar mensajes de depuración
    print("Consulta exitosa. Respuesta recibida de la API.")
    
    return resultado

st.title("Roobi")
st.write("Tu IA personalizada")

if 'preguntas' not in st.session_state:
    st.session_state.preguntas = []
if 'respuestas' not in st.session_state:
    st.session_state.respuestas = []

def click():
    if st.session_state.user != '':
        pregunta = st.session_state.user
        respuesta = consulta(pregunta)

        st.session_state.preguntas.append({"role": "user", "content": pregunta})
        st.session_state.respuestas.append({"role": "assistant", "content": respuesta})

        # Limpiar el input de usuario después de enviar la pregunta
        st.session_state.user = ''

with st.form('my-form'):
    query = st.text_input('¿En qué te puedo ayudar?:', key='user', help='Pulsa Enviar para hacer la pregunta')
    submit_button = st.form_submit_button('Enviar', on_click=click)

if st.session_state.preguntas:
    for i in range(len(st.session_state.preguntas)):
        pregunta = st.session_state.preguntas[i]
        respuesta = st.session_state.respuestas[i]
        
        st.chat_message(pregunta["role"]).write(pregunta["content"])
        st.chat_message(respuesta["role"]).write(respuesta["content"])