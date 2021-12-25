# Import modules
from parkwhere import extract_all_features
import streamlit as st
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import plotly.graph_objects as go

def main():

    # Main interface
    st.title("ParkWhere")
    st.write("Check out the side bar to find out more about ParkWhere!")

    # Sidebar interface
    st.sidebar.header("What is ParkWhere?")
    st.sidebar.info("ParkWhere is a web application that helps me predict parking availability at my apartment block.")

    st.sidebar.header("How did this begin?")
    how_it_began = """
    Parking spaces are always limited at the apartment block where I live. Very often, I return home at night, only to end up parking a few hundred metres away. 
    
    It's especially frustrating when there are things to carry from the car and an active toddler to manage!
    
    One day, an idea popped into my head \U0001F4A1! Why not collect some data myself, and put data science into action? 
    """
    st.sidebar.info(how_it_began)

    st.sidebar.header("How does it work?")
    how_it_works = """
    I divided available parking spaces at my apartment block into four zones, 'Zone 1' being the nearest. For eight months, I recorded the dates, times and zones at which I found a parking lot upon returning home.
    
    Using the collected data, I trained a binary classification model using Logistic Regression that predicts, given a specific time I return home, how likely I will find a parking lot nearest to my block.

    Check out this [GitHub repo](https://github.com/zeyalt/ParkWhere) to find the source codes and dataset for this project.
    """
    st.sidebar.info(how_it_works)

    st.sidebar.header("Who am I?")
    about_me = """
    Hi! My name is Zeya. This is a project that I've been working on during my free time. 
    
    My main motivation was to develop a simple machine learning application that helps me in my everyday life. 
    
    Feel free to connect with me via 👇:
    """
    connect_with_me = """
    [![image](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/zeyalt/) 
    
    [![image](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/zeyalt_) 
    
    [![image](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white)](https://zeyalt.medium.com/)
    """
    st.sidebar.info(about_me + connect_with_me)

    p1, p2 = st.columns([1, 1])

    # Get date and time inputs (defaults to current date and time)
    date_predict = p1.date_input('Enter date...', dt.date.today(), key='1') 
    time_now_predict = dt.datetime.now() + dt.timedelta(hours=8) # Based on server time
    # time_now_predict = dt.datetime.now() # Based on local machine time
    time_now_predict = time_now_predict.strftime("%H:%M")
    time_now_predict = p2.text_input("... and time", value=time_now_predict, key='1') 

    # Load trained model
    model = pickle.load(open('model/model.sav', 'rb'))

    # Arrange date and time inputs as a DataFrame and extract features
    predict_df = pd.DataFrame({'date_time': str(date_predict) + ' ' + time_now_predict}, index=[0])
    predict_df['date_time'] = pd.to_datetime(predict_df['date_time'])
    predict_df = extract_all_features(predict_df)
    predict_df = predict_df[['hour_min', 'day_of_week', 'ph_eve']]

    # Generate prediction and predicted probabilities
    pred = model.predict(predict_df)[0]
    pred_proba = model.predict_proba(predict_df)[0]
    
    # Create a static donut chart 
    labels = [i+"\n"+str(round(j,3)) for i, j in zip(model.classes_, pred_proba)]
    plt.figure(figsize=(6,6))
    fig = plt.pie(pred_proba, labels=labels, colors=['green', 'red'])
    my_circle = plt.Circle((0,0), 0.7, color='white')
    fig = plt.gcf()
    fig.gca().add_artist(my_circle)
    
    # Result message
    if pred == 'Zone 1':
        result_string = "Good news \U0001F973\U0001F973\U0001F973! You are likely to park at a lot near to your apartment block!"
        proba = round(pred_proba[1], 3)
    else:
        result_string = '\U0001F974\U0001F974\U0001F974 Oops. Looks like all nearest parking lots might have been taken up. Come home earlier next time!'
        proba = round(pred_proba[0], 3)
    st.markdown(result_string)

    # Expander to view prediction results
    with st.expander('View prediction results'):
        s1, s2 = st.columns([1, 3])
        s1.markdown(f"<h3 style='text-align: center; color: black;'>{pred} (with {proba} probability)</h1>", unsafe_allow_html=True)
        s2.pyplot(fig)

if __name__ == "__main__":
    main()