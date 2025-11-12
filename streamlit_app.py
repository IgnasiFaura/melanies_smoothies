# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
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
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

#Convert the snowpark dataframe to a pandas dataframe so we can use the LOC function
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

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
      
                search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
                st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
      
                st.subheader(fruit_chosen + ' Nutrition Information')
                smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
                sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
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
