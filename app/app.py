import streamlit as st
import pandas as pd
import json
import requests

def set_page_config():
    st.set_page_config(
        page_title="Kubernets Deployments",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/yemoncada/mlops_covertype',
            'Report a bug': "https://github.com/yemoncada/mlops_covertype",
            'About': "Kubernets APP Deployment"
        }
    )

def create_header():
    st.title('Despliegue Kubernets (CoverType Dataset)')
    st.subheader('by Yefry Moncada Linares ([@yemoncad](https://github.com/yemoncada?tab=repositories))')

    st.markdown(
        """
        <br><br/>
        Galaxy Zoo DECaLS includes deep learning classifications for all galaxies.
        Our model learns from volunteers and predicts posteriors for every Galaxy Zoo question.
        Explore the predictions using the filters on the left. Do you agree with the model?
        To read more about how the model works, click below.
        """
        , unsafe_allow_html=True)

    st.markdown('---')

def create_sidebar():
    st.sidebar.markdown('# Choose Your Galaxies')

    option = st.sidebar.selectbox(
        'Seleccione el proceso que desee realizar',
        ('Procesar Información', 'Entrenamiento Modelo', 'Inferencia', 'Almacenar Información'))

    return option

def procesar_informacion():

    base_url = "http://load-database:8502"

    if st.button('Cargar Base de Datos'):
        with st.spinner('Wait for it...'):
            response = requests.get(f"{base_url}/load_data")
            if response.status_code == 200:
                st.success('La base de Datos ha sido Creada y Cargada!', icon="✅")
                df = pd.read_json(response.json(), orient='records')
                st.dataframe(df.head(50))
            else:
                st.write(f"Ocurrió un error. Código de estado: {response.status_code}")

def entrenamiento_modelo():
    base_url = "http://train-model:8503"

    if st.button('Entrenar Modelo'):
        with st.spinner('Wait for it...'):
            response = requests.get(f"{base_url}/train")
            if response.status_code == 200:
                st.success('El modelo ha sido entrenado satisfactoriamente!', icon="✅")
                st.json(response.json())
            else:
                st.write(f"Ocurrió un error. Código de estado: {response.status_code}")

def inferencia():

    base_url = "http://inference:8504"

    option_inf = st.sidebar.selectbox('Opciones Modelo', ['Inferencias', 'Ver Base Inferencias', 'Limpiar Tabla Inferencias'])

    if option_inf == 'Inferencias':
        # Crear sliders para recibir datos de entrada del usuario
        Elevation = st.sidebar.slider("Elevation", 0, 5000, 2800)
        Slope = st.sidebar.slider("Slope", 0, 90, 5)
        Horizontal_Distance_To_Hydrology = st.sidebar.slider("Horizontal Distance To Hydrology", 0, 10000, 250)
        Vertical_Distance_To_Hydrology = st.sidebar.slider("Vertical Distance To Hydrology", 0, 1000, 50)
        Horizontal_Distance_To_Roadways = st.sidebar.slider("Horizontal Distance To Roadways", 0, 10000, 1000)
        Hillshade_9am = st.sidebar.slider("Hillshade 9am", 0, 255, 220)
        Hillshade_Noon = st.sidebar.slider("Hillshade Noon", 0, 255, 230)
        Horizontal_Distance_To_Fire_Points = st.sidebar.slider("Horizontal Distance To Fire Points", 0, 10000, 500)
        
        
        if st.button("Predict"):
            cover_data = {
                "Elevation": Elevation,
                "Slope": Slope,
                "Horizontal_Distance_To_Hydrology": Horizontal_Distance_To_Hydrology,
                "Vertical_Distance_To_Hydrology": Vertical_Distance_To_Hydrology,
                "Horizontal_Distance_To_Roadways": Horizontal_Distance_To_Roadways,
                "Hillshade_9am": Hillshade_9am,
                "Hillshade_Noon": Hillshade_Noon,
                "Horizontal_Distance_To_Fire_Points": Horizontal_Distance_To_Fire_Points,
            }

            payload = {**cover_data, "model": "covertype_data"}

            headers = {"Content-Type": "application/json"}

            response = requests.post(f"{base_url}/predict_model", data=json.dumps(payload), headers=headers)
            st.write(response)
            
            prediction = response.json()

            st.write(prediction)

            st.write(f"La predicción del tipo de cobertura es: {prediction['prediction']}")

    elif option_inf == 'Ver Base Inferencias':
        # Realizar una solicitud GET a la ruta "/cover_type_data"
        response = requests.get(f"{base_url}/cover_type_data")
        json_data = json.dumps(response.json()['cover_type_data'])

        if len(response.json()['cover_type_data']) != 0:
            st.success('Cargando Base de Datos de Inferencia', icon="✅")
            df = pd.read_json(json_data, orient='records')
            st.dataframe(df.head(50))
        else:
            st.warning('Base de datos vacia - No Hay Inferencias Generadas', icon="⚠️")

    elif option_inf == 'Limpiar Tabla Inferencias':
        # Realizar una solicitud GET a la ruta "/cover_type_data"

        if st.button("Limpiar Base de datos"):
            response = requests.delete(f"{base_url}/delete_data_inference/")
            st.success('Limpieza de la Base de datos satisfactoria ', icon="✅")

def almacenar_informacion():
    # Código relacionado con la opción 'Almacenar Información' aquí
    if st.button("Almacenar Información"):

        base_url = "http://logging:8505"    
        response = requests.get(f"{base_url}/save_inferences")
        json_data = json.dumps(response.json()['cover_type_data'])

        st.json(json_data, expanded=True)

        st.download_button(
            label="Download JSON",
            file_name="data.json",
            mime="application/json",
            data=json_data,
        )

def main():
    set_page_config()
    create_header()
    option = create_sidebar()

    if option == 'Procesar Información':
        procesar_informacion()
    elif option == 'Entrenamiento Modelo':
        entrenamiento_modelo()
    elif option == 'Inferencia':
        inferencia()
    elif option == 'Almacenar Información':
        almacenar_informacion()


if __name__ == "__main__":
    main()
