import vanna as vn
import streamlit as st

vn.set_api_key(st.secrets["vanna_api_key"])
vn.set_model('chinook')
vn.connect_to_sqlite('https://vanna.ai/Chinook.sqlite')

st.title("Welcome to your :blue[SQL Chatbot]")
query = st.session_state.get("query", default=None)
if query is None:
    query = st.text_input("What would you like to know from the database?", key="query")
else:
    st.header(query)
    sql = vn.generate_sql(query)
    st.code(sql, language='sql')
    df = vn.run_sql(sql)
    st.dataframe(df, use_container_width=True)
    fig = vn.get_plotly_figure(plotly_code=vn.generate_plotly_code(question=query, sql=sql, df=df), df=df)
    st.plotly_chart(fig, use_container_width=True)
    st.button("Ask another question", on_click=lambda:st.session_state.clear())
