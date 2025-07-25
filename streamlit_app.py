# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Fresh Up with a Healthy Smoothie :cup_with_straw: {st.__version__}")
st.write(
  """Choose the Fruits of your choice for your Smoothie
  """
)
name_on_order = st.text_input("Enter your name on your Smoothie")
st.write("The name on your smoothie will be:",name_on_order)
final_msg = (f":cup_with_straw: Your smoothie is ordered!"+' '+name_on_order)

session = get_active_session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose upto 5 ingredients'
    ,my_dataframe
    ,max_selections=5
    )
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen+' '
    #st.write(ingredients_string)

    my_insert_stmt = """
                    insert into smoothies.public.orders(ingredients,name_on_order) values('"""+ingredients_string+"""','"""+ name_on_order +"""');
                 """
    time_to_insert = st.button("Submit Order")
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(final_msg)
      
    st.stop()
    
