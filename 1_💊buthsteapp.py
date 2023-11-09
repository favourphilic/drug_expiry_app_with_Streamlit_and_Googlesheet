import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_gsheets import GSheetsConnection
import pickle
from pathlib import Path
import pandas as pd  
import streamlit_authenticator as stauth  






st.set_page_config(page_title="ButhExpiry", page_icon="🧊", layout="wide")
st.title("  SoonToExpire Portal :pill: ")
#------------------------------------------
#trying to ccreate a session state
#-------------------------------------------
# 5. Add on_change callback for the option menu
def on_change(key):
    selection = st.session_state[key]
    st.write(f"Selection changed to {selection}")
#with st.sidebar:
selected = option_menu(None, ["Pharmacist", 'Doctor'], 
    icons=['bandaid', 'person-plus-fill'],
     on_change=on_change, key='menu_5', menu_icon="cast", default_index=1, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "green"},
    })
#st.markdown("***")
if selected == "Pharmacist":
    
    import yaml
    from yaml.loader import SafeLoader
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
    name, authentication_status, username = authenticator.login('Login', 'sidebar')

    if authentication_status:
        authenticator.logout('Logout', 'sidebar')
        if username == 'jonyemelukwe'or 'oladapo' or'vjokanola' or 'eoyedotun' or 'sombule' or 'majala' or'fajani':
        #     st.write(f'Hello Focal Pharmacist *{name}*')
        #     st.subheader('Your detail will go in here')
        # elif username == "jonyemelukwe":
        #     st.write(f'Hello Store Pharmacist *{name}*')
        #     st.subheader('Your detail will go in here')
        # else:
            st.write(f'Welcome  Pharm  *{name}*')
            #st.title(" :pill: SoonToExpire  Portal  ")

            #Constants

            TYPES = ["Tab", "Sups", "Inj", "Cap"]
            CLASSES= ["Antibiotics", "Analgesic", "Antifungal", "Heamatinics", "Creams","Gutt","Occ","Multivitamin", "Others"]

            #Establish a google sheet connection
            conn = st.connection("gsheets", type=GSheetsConnection)
            #fetching existing data
            existing_data = conn.read(worksheet="drug", usecols=list(range(4)), ttl=5)
            #use na to avoid displaying empty roles
            existing_data = existing_data.dropna(how='all')

            if "df" not in st.session_state:
                st.session_state['df'] = existing_data
            
            
            action = st.selectbox(
                "Click Here to Onboard,Update,Delete or View Soon to Expire Drug Items",
                [
                    "Onboard New SoonToExpireDrug",
                    "Update Existing SoonToExpireDrug",
                    "View All SoonToExpireDrug",
                    "Delete SoonToExpireDrug",
                ],
            )
            st.markdown("---")
            st.markdown("***")
            if action == "Onboard New SoonToExpireDrug":
                st.markdown(":ninja: Enter the Details of the new soon to expired drug below :ninja:")
                with st.form(key="DrugForm"):
                    Type= st.selectbox(label="Formulation", options=TYPES)
                    Item= st.text_input(label="Name Of Drug(Generic)*")
                    Class= st.selectbox(label="Drug Category", options=CLASSES)
                    Date=st.date_input(label="Expire Date")
                    #Indicate a sign for madatory fields
                    st.markdown("**required*")
                    submit_button = st.form_submit_button(label="Submit SoonToExpire Details")

                     #if the submit button is pressed

                    if submit_button:
            #st.write("You have Submit the form")
            #check that all the mandatory fields are fill out

                        if not Item:
                            st.warning("Kindly Input the name of the drug")
                            st.stop()
                        else:
                            #create a new row for the soon to be expired drug
                            # which is a list of dictionary
                            SED_data= pd.DataFrame(
                                [ 
                                    {
                                        "Type": Type,
                                        "Item":Item,
                                        "Class":Class,
                                        "Date":Date.strftime("%d-%B-%Y")

                                    }
                                ])
                            #Add the new data to existing data
                            update_df=pd.concat([existing_data, SED_data], ignore_index=True)

                            #Update the google sheet data with the new about to expire data
                            conn.update(worksheet="drug", data=update_df)

                            st.success("Your Entry Has been Successfully Submitted!")
            #--------------------------------------------------------------------------        
            #if the submit button is pressed
            elif action == "Update Existing SoonToExpireDrug":
                st.write("This space is still under construction")
            elif action ==  "View All SoonToExpireDrug":
                    st.markdown(" :memo: Soon To Expire Drug BY Months :memo:")
                    #convert the date column to datetime
                    existing_data['Date'] = pd.to_datetime(existing_data['Date'])
                    existing_data['Month'] = existing_data['Date'].dt.month
                    #st.write(existing_data)
                    st.dataframe(existing_data.sort_values(by='Month', ascending=False))
            elif action == "Delete SoonToExpireDrug":
                    drug_to_delete= st.selectbox(
                    "Select drug to Delete", options=existing_data['Item'].tolist() )

                    if st.button("Delete"):
                        existing_data.drop(
                            existing_data[existing_data['Item']== drug_to_delete].index, inplace=True )
                        conn.update(worksheet="drug", data=existing_data)
                        st.success("Drug Successfully deleted")

            

#-------------------------------------------------------------------------------------------
    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')
#------------------------------------------------------------------------------------------------------


else:
    # Using Session State------------------------------------------
    # st.subheader(":health_worker: Welcome!!! ")
    # st.title(" :pill: SoonToExpire Portal :pill: ")
    # st.session_state.df['Date'] = pd.to_datetime(st.session_state.df['Date'], format='%d-%B-%Y')
    # # st.session_state.ed['Date'] = pd.to_datetime(st.session_state.ed['Date'], format='%d-%B-%Y.%f')
    # st.session_state.df['Month']= st.session_state.df['Date'].dt.month
    # st.session_state.df['Year']= st.session_state.df['Date'].dt.year
    # #st.write(st.session_state.df)
    

    # st.sidebar.header("Please Filter The Table Here")
    # types = st.sidebar.multiselect("By Type", options= st.session_state['df'].Type.unique(), default=st.session_state['df'].Type.unique() )
    # category = st.sidebar.multiselect("By Drug class", options= st.session_state['df'].Class.unique(), default=st.session_state['df'].Class.unique())
    # year = st.sidebar.multiselect("By Year", options= st.session_state['df'].Year.unique(),default =st.session_state['df'].Year.unique())
    # months = st.sidebar.multiselect("By Multiple Months", options= st.session_state['df'].Month.unique(),default =st.session_state['df'].Month.unique() )

    # df_selection = st.session_state['df'].query(
    # "Type == @types & Class == @category & Year == @year & Month== @months")
    # st.write(df_selection)

#---------------------------------------------------------------------
    #Establish a google sheet connection
    conn = st.connection("gsheets", type=GSheetsConnection)
    #fetching existing data
    df = conn.read(worksheet="drug", usecols=list(range(4)), ttl=5)
    #use na to avoid displaying empty roles
    df = df.dropna(how='all')
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%B-%Y')
    # st.session_state.ed['Date'] = pd.to_datetime(st.session_state.ed['Date'], format='%d-%B-%Y.%f')
    df['Month']= df['Date'].dt.month
    df['Year']= df['Date'].dt.year
    

    st.sidebar.header("Please Filter The Table Here")
    types = st.sidebar.multiselect("By Type", options= df.Type.unique(), default=df.Type.unique() )
    category = st.sidebar.multiselect("By Drug class", options= df.Class.unique(), default=df.Class.unique())
    year = st.sidebar.multiselect("By Year", options= df.Year.unique(),default =df.Year.unique())
    months = st.sidebar.multiselect("By Multiple Months", options= df.Month.unique(),default =df.Month.unique() )

    df_selection = df.query(
    "Type == @types & Class == @category & Year == @year & Month== @months")
    st.write(df_selection)


    
