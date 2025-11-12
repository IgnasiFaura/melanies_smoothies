# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """)

import streamlit as st

title = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be:", title)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
    )  
name_on_order_list = 'Ignasi'

if ingredients_list:
    ingredients_string=''
#    if name_on_order_list:
 #       name_on_order_string=''
    
    for fruit_chosen in ingredients_list:
  #      for name_chosen in name_on_order_list:
                ingredients_string += fruit_chosen + ' '
   #             name_on_order_string += name_chosen + ' '

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+ 'Ignasi' +"""')"""

 #   st.write(my_insert_stmt)
  #  st.stop()
    time_to_insert = st.button('Submit Oder')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, Ignasi!', icon="✅")
