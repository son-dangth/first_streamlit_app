import streamlit as st
import snowflake.connector
import pandas as pd
import requests
from urllib.error import URLError


st.header("Breakfast Favourites")
st.text(" 🥣 Omega 3 & Blueberry Oatmeal")
st.text(" 🥗 Kale, Spinach & Rocket Smoothie")
st.text(" 🐔 Hard-Boiled Free-Range Egg")
st.text("🥑🍞 Avocado Toast")

st.header("🍌🥭 Build Your Own Fruit Smoothie 🥝🍇")
my_fruit_list = pd.read_csv(
    "https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt"
)
my_fruit_list = my_fruit_list.set_index("Fruit")

# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = st.multiselect(
    "Pick some fruits:", list(my_fruit_list.index), ["Avocado", "Strawberries"]
)
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
st.dataframe(fruits_to_show)

# New section to display Fruivice API Response
st.header("Fruityvice Fruit Advice!")


def get_fruitvice_data(fruit_choice):
    fruityvice_response = requests.get(
        "https://fruityvice.com/api/fruit/" + fruit_choice
    )
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized


try:
    fruit_choice = st.text_input("What fruit would you like information about?")
    if not fruit_choice:
        st.error("Please select a fruit to get information about.")
    else:
        back_from_function = get_fruitvice_data(fruit_choice)
        st.dataframe(back_from_function)
except URLError as e:
    st.error()


def get_fruit_load_list(cnx):
    with cnx.cursor() as my_cur:
        my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
        return my_cur.fetchall()


st.header("The fruit load list contains:")
# Connecting to Snowflake
if st.button("Get Fruit Load List"):
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    my_data_rows = get_fruit_load_list(my_cnx)
    my_cnx.close()
    st.dataframe(my_data_rows)


def insert_row_snowflake(newfruit, cnx):
    with cnx.cursor() as my_cur:
        my_cur.execute(
            "insert into pc_rivery_db.public.fruit_load_list (fruit_name) values ('"
            + newfruit
            + "')",
        )
        return f"Thanks for adding {newfruit}!"


add_my_fruit = st.text_input("What fruit would you like to add?", "jackfruit")
if st.button("Add Fruit"):
    with snowflake.connector.connect(**st.secrets["snowflake"]) as my_cnx:
        response = insert_row_snowflake(add_my_fruit, my_cnx)
    st.success(response)
