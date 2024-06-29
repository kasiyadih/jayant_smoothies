# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
# Write directly to the app
st.title("Customize your smoothie")
st.write(
    """Replace this example with your own code!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)


#option =  st.selectbox('What is your favourite food',('Banana','Strawberries','Peaches'))
#st.write('your Favourite food is',option)
cnx = st.connection("snowflake")
session = cnx.session()


name_on_order = st.text_input('Name on smootie')
st.write('Your name in smoothie :',name_on_order)
my_dataframe = session.table('SMOOTHIES.PUBLIC.FRUIT_OPTIONS').select(col('FRUIT_NAME'))
#st.dataframe(data = my_dataframe, use_container_width=True)

ingrefients_list = st.multiselect('Choose up to five ingredients',my_dataframe,max_selections =5)
if ingrefients_list:    
    #st.write(ingrefients_list)
    #st.text(ingrefients_list)
    ingredients_string  = ''
    for fruits_choosen in ingrefients_list:
        ingredients_string += fruits_choosen+' '
    #st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!'+name_on_order,icon="✅")
