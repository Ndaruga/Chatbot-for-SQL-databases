import vanna as vn
import streamlit as st
import time
from streamlit_option_menu import option_menu


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



vn.set_api_key(st.secrets["vanna_api_key"])
vn.set_model('chinook')

st.title("Welcome to your :blue[SQL Chatbot]")

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


if selected == "SQL Server":
    st.subheader('SQL Server database')
    Db_Host, DBpassword, DBuser, Db_name = conn_params()
    # Add a button to connect to the database
    connect = st.button("Connect", key="connect")

    # Display a message when the button is clicked
    if connect:
        st.write(f"Connecting to {Db_Host} as {DBuser}...")
        vn.connect_to_postgres(host=Db_Host, dbname=Db_name, password=DBpassword, user=DBuser)
        # Check the connection status
        query_database()


if selected == "PostgreSQL":
    st.subheader('PostgerSQL database')
    Db_Host, DBpassword, DBuser, Db_name = conn_params()
    # Add a button to connect to the database
    connect = st.button("Connect", key="connect")

    # Display a message when the button is clicked
    if connect:
        st.write(f"Connecting to {Db_Host} as {DBuser}...")
        vn.connect_to_postgres(host=Db_Host, dbname=Db_name, password=DBpassword, user=DBuser)
        # Check the connection status
        query_database()


# Hostname: hh-pgsql-public.ebi.ac.uk
# Port: 5432
# Database: pfmegrnargs
# User: reader
# Password: NWDMCE5xdipIjRrp



