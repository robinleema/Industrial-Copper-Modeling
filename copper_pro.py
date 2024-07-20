
import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import sklearn
import pickle


# Streamlit Part
st.set_page_config(layout="wide")
st.title(":rainbow[**INDUSTRIAL COPPER MODELING**]")
st.write("**Industrial Copper Modeling Analysis**")

# user input:
class options:

    country_option = [25.0, 26.0, 27.0, 28.0, 30.0, 32.0, 38.0, 39.0, 40.0, 77.0, 78.0, 79.0, 80.0, 84.0, 89.0, 107.0, 113.0]
    
    status_option = ['Won', 'Draft', 'To be approved', 'Lost', 'Not lost for AM','Wonderful', 'Revised', 'Offered', 'Offerable']
    
    status_dict = {"Lost":0,"Won":1,"Draft":2,"To be approved":3,"Not lost for AM":4,"Wonderful":5,
                   "Revised":6,"Offered":7,"Offerable":8}
    
    item_type_option = ['W', 'WI', 'S', 'PL', 'IPL', 'SLAWR','Others']
    item_type_dict = {'W':5.0, 'WI':6.0, 'S':3.0, 'Others':1.0, 'PL':2.0, 'IPL':0.0, 'SLAWR':4.0}

    application_values = [2.0, 3.0, 4.0, 5.0, 10.0, 15.0, 19.0, 20.0, 22.0, 25.0, 26.0, 27.0, 28.0, 
                          29.0, 38.0, 39.0, 40.0, 41.0, 42.0, 56.0, 58.0, 59.0, 65.0, 66.0, 67.0, 68.0, 69.0, 70.0, 79.0, 99.0]
    
    product_ref_values = [611728, 611733, 611993, 628112, 628117, 628377, 640400, 640405, 640665, 164141591, 164336407, 164337175, 929423819, 
                          1282007633, 1332077137, 1665572032, 1665572374, 1665584320, 1665584642, 1665584662, 1668701376, 1668701698, 1668701718, 
                          1668701725, 1670798778, 1671863738, 1671876026, 1690738206, 1690738219, 1693867550, 1693867563, 1721130331, 172220757]


# Functions in Predict_status("Won" or "Lost")

def predict_status(country,item_type,application,width,product_ref,quantity_tons_log,customer_log,thickness_log,
                   selling_price_log,item_date_day,item_date_month,item_date_year,delivery_date_day,delivery_date_month,
                    delivery_date_year):
    
    # pickle file for Classification Model
    with open(r"C:/Users/USER/Desktop/Robin vs/guvi_projects/Classification_model.pkl", "rb") as f:
        model_class = pickle.load(f)

    user_class_data = np.array([[country,options.item_type_dict[item_type],application,width,product_ref,quantity_tons_log,customer_log,thickness_log,
                   selling_price_log,item_date_day,item_date_month,item_date_year,delivery_date_day,delivery_date_month,
                    delivery_date_year]])
    
    y_pred = model_class.predict(user_class_data)

    if y_pred == 1:
        return 1
    else:
        return 0

# Function in predict_selling_price:

def predict_selling_price(country,status,item_type,application,width,product_ref,quantity_tons_log,customer_log,thickness_log,
                   item_date_day,item_date_month,item_date_year,delivery_date_day,delivery_date_month,
                    delivery_date_year):
    
    # pickle file for Regression Model
    with open (r"C:/Users/USER/Desktop/Robin vs/guvi_projects/Regression_Model.pkl","rb") as f:
        model_regression = pickle.load(f)

        user_regression_data = np.array([[country,options.status_dict[status],options.item_type_dict[item_type],application,width,product_ref,quantity_tons_log,customer_log,thickness_log,
                   item_date_day,item_date_month,item_date_year,delivery_date_day,delivery_date_month,
                    delivery_date_year]])
        
        y_pred = model_regression.predict(user_regression_data)

        exponential_y_pred = np.exp(y_pred[0])

        return exponential_y_pred



with st.sidebar:
    option = option_menu("DATA EXPLORATION", options=["PREDICT SELLING PRICE", "PREDICT STATUS"])

if option == "PREDICT SELLING PRICE":
    st.header(":Red[PREDICT SELLING PRICE]")
    st.write("")

    col1,col2 = st.columns(2)
    with col1:
        country = st.selectbox(label='Country', options=options.country_option)

        status = st.selectbox(label='Status', options=options.status_option)

        item_type = st.selectbox(label='Item Type', options=options.item_type_option)

        application = st.selectbox(label='Application', options=options.application_values)

        product_ref = st.selectbox(label='Product Ref', options=options.product_ref_values)

        quantity_tons_log = st.number_input(label='Quantity Tons Log Value [Min:-11.51 & Max:20.72]', format= "%0.2f")

        customer_log = st.number_input(label='Customer Log Value [Min:9.43 & Max:21.48]', format="%0.2f")

        thickness_log = st.number_input(label="Thickness Log Value [Min:-1.71 & Max:7.82]", format="%0.2f")
       
        
    with col2:

        width = st.number_input(label='Width [Min:1.0 & Max:2990.0]')

        item_date_day = st.number_input(label='Item Date Day [Min:1 & Max:31]')

        item_date_month = st.number_input(label='Item Date Month [Min:1 & Max:12]')

        item_date_year = st.number_input(label='Item Date Year [Min:2020 & Max:2021]')

        delivery_date_day = st.number_input(label='Delivery Date Day [Min:1 & Max:31]')

        delivery_date_month = st.number_input(label='Delivery Date Month [Min:1 & Max:12]')

        delivery_date_year = st.number_input(label='Delivery Date Year [Min:2020 & Max:2022]')


    button = st.button(":blue[PREDICT THE SELLING PRICE]", use_container_width=True)

    if button:
        price = predict_selling_price(country,status,item_type,application,product_ref,quantity_tons_log,customer_log,thickness_log,
                                      width,item_date_day,item_date_month,item_date_year,delivery_date_day,delivery_date_month,delivery_date_year)
        
        st.write(":green[THE SELLING PRICE IS : ]",price)


if option == "PREDICT STATUS":

    st.header(":Red[Predict The Status (Won / Lost)]")
    st.write(" ")
    
    col1,col2 = st.columns(2)
    with col1:
       
        country = st.selectbox(label='Country', options=options.country_option)

        item_type = st.selectbox(label='Item Type', options=options.item_type_option)

        application = st.selectbox(label='Application', options=options.application_values)

        product_ref = st.selectbox(label='Product Ref', options=options.product_ref_values)

        quantity_tons_log = st.number_input(label='Quantity Tons Log Value [Min:-11.51 & Max:20.72]', format= "%0.2f")

        customer_log = st.number_input(label='Customer Log Value [Min:9.43 & Max:21.48]', format="%0.2f")

        thickness_log = st.number_input(label='Thickness Log Value [Min:-1.71 & Max:7.82]', format="%0.2f")

        selling_price_log = st.number_input(label= 'Selling Price Log Value [Min:-2.30 & Max:18.42]',format="%0.2f")

    with col2:

        width = st.number_input(label='Width [Min:1.0 & Max:2990.0]')

        item_date_day = st.number_input(label='Item Date Day [Min:1 & Max:31]')

        item_date_month = st.number_input(label='Item Date Month [Min:1 & Max:12]')

        item_date_year = st.number_input(label='Item Date Year [Min:2020 & Max:2021]')

        delivery_date_day = st.number_input(label='Delivery Date Day [Min:1 & Max:31]')

        delivery_date_month = st.number_input(label='Delivery Date Month [Min:1 & Max:12]')

        delivery_date_year = st.number_input(label='Delivery Date Year [Min:2020 & Max:2022]')
     
  
    
    button = st.button(":violet[PREDICT THE STATUS]" ,use_container_width=True)
    st.header(":Rainbow[The Status (Won / Lost)]")
    if button:
        status = predict_status(country,item_type,application,product_ref,quantity_tons_log,customer_log,thickness_log,selling_price_log,
                                width,item_date_day,item_date_month,item_date_year,delivery_date_day,delivery_date_month,delivery_date_year)
        
       
        if status == 1:
            st.write(":green[THE STATUS IS WON]")
        else:
            st.write(":red[THE STATUS IS LOST]")        



