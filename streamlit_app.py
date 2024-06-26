# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col
# from snowflake.snowpark.context import get_active_session


# Write directly to the app
st.title(":cup_with_straw: Example Streamlit App :cup_with_straw:")
smoothie_name = st.text_input('Name on the smoothie:')
st.write(
    "Choose the fruits you want in your Smoothie!"
)

# option = st.selectbox('What is your favorite fruit?', ('Banana', 'Strawberries', 'Peaches'))
# st.write('Your favorite fruit is:',option);


# session = get_active_session()

cnx=st.connection("snowflake")
session=cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

pd_df=my_dataframe.to_pandas()
# st.dataframe(data=pd_df)
# st.stop()



ingredients_list = st.multiselect('Choose up to 5 ingredients:',my_dataframe,max_selections=5);

if ingredients_list:
    st.text(ingredients_list);
    ingredients_string = ''
    for fruit in ingredients_list:
        ingredients_string += fruit + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit,' is ', search_on, '.')
        
        st.subheader(fruit + ' Nutrition information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit)
        # if fruityvice_response == 200:
        fv_df=st.dataframe(data=fruityvice_response.json(), use_container_width=True)
        #st.write("https://fruityvice.com/api/fruit/"+fruit)
    
    button_submit=st.button('Submit Order')
    if button_submit:
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """' , '""" + smoothie_name + """')"""
        st.write(my_insert_stmt)
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! ' + smoothie_name, icon="✅")

# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# st.text(fruityvice_response.json())
# fv_df=st.dataframe(data=fruityvice_response.json(), use_container_width=True)
