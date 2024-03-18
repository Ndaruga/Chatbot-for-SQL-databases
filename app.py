import vanna as vn
import streamlit as st
import time
import pandas as pd
import pyodbc
import psycopg2
from streamlit_option_menu import option_menu
from vanna.remote import VannaDefault



# Vanna AI 
vanna_api_key = st.secrets["vanna_api_key"]
vanna_model_name='chinook'
vn = VannaDefault(model=vanna_model_name, api_key=vanna_api_key)

st.title("Welcome to your :blue[SQL Chatbot]")

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True


def conn_params():
    Db_Host = st.text_input("Hostname", placeholder="localhost")
    Db_name = st.text_input("Enter Database Name", placeholder= "DataBase name")
    DBuser = st.text_input("Enter username", placeholder= "Username")
    DBpassword = st.text_input("Enter Password", placeholder= "Password")

    return Db_Host, DBpassword, DBuser, Db_name


def query_database():
    query = st.session_state.get("query", default=None)
    if query is None:
        query = st.text_input("What would you like to know from the database?", key="query")
    else:
        st.subheader(query)
        sql = vn.generate_sql(query)
        st.code(sql, language='sql')
        df = vn.run_sql(sql)
        st.dataframe(df, use_container_width=True)
        fig = vn.get_plotly_figure(plotly_code=vn.generate_plotly_code(question=query, sql=sql, df=df), df=df)
        st.plotly_chart(fig, use_container_width=True)

        st.button("Ask another question", on_click=lambda:st.session_state.clear())

with st.sidebar:
    selected = option_menu(
            menu_title = "Connect to Database",
            options = ["Demo Database","MySQL","SQL Server","PostgreSQL"]
        )
       

if selected == "Demo Database":
    st.subheader('SQLite database')
    vn.connect_to_sqlite('https://vanna.ai/Chinook.sqlite')
    query_database()

        
if selected == "MySQL":
    st.subheader('MySQL database')
    Db_Host, DBpassword, DBuser, Db_name = conn_params()
    # Add a button to connect to the database
    connect = st.button("Connect", key="connect")

    # Display a message when the button is clicked
    if connect:
        st.write(f"Connecting to {Db_Host} as {DBuser}...")
        vn.connect_to_postgres(host=Db_Host, dbname=Db_name, password=DBpassword, user=DBuser)
        # Check the connection status
        query_database()

def run_sql_for_DB(sql: str) -> pd.DataFrame:
    df = pd.read_sql(sql, con_database)
    return df

if selected == "SQL Server":
    st.subheader('SQL Server database')

    Db_Host, DBpassword, DBuser, Db_name = conn_params()

    connect = st.button("Connect", key="connect")

    # Display a message when the button is clicked
    if connect:
        st.write(f"Connecting to {Db_Host} as {DBuser}...")
        con_database = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server}; SERVER={Db_Host}; DATABASE={Db_name};USER={DBuser};PASSWORD={DBpassword}")
        vn.run_sql = run_sql_for_DB
        # Check the connection status
        query_database()


if selected == "PostgreSQL":
    st.subheader('PostgreSQL database')
    Db_Host, DBpassword, DBuser, Db_name = conn_params()

    # Add a button to connect to the database
    st.button("Connect", on_click=click_button)

    if st.session_state.clicked:
        st.write(f"Connecting to {Db_Host} as {DBuser}...")

        # if True:    # Check the connection status
        vn.connect_to_postgres(host=Db_Host, dbname=Db_name, password=DBpassword, user=DBuser, port=5432)
        st.success("Connection is successful!")
        
        query_database()
    else:
        st.error(f"Connection to {Db_name} failed!!")



