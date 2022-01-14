# ParkWhere

ParkWhere is a web application that helps me predict parking availability at my apartment block. 

![image](https://github.com/zeyalt/ParkWhere/blob/master/parkwhere_demo_gif.gif "GIF image")

Check out ParkWhere at this [link](https://share.streamlit.io/zeyalt/parkwhere/app.py)!

## The motivation behind ParkWhere

Parking spaces are always limited at the apartment block where I live. Very often, I return home at night, only to end up parking a few hundred metres away. 
    
It's especially frustrating when there are things to carry from the car and an active toddler to manage!
    
One day, an idea popped into my head! Why not collect some data myself, and put data science into action? 

## How does it work?

I divided available parking spaces at my apartment block into four zones, 'Zone 1' being the nearest. For eight months, I recorded the dates, times and zones at which I found a parking lot upon returning home.
    
Using the collected data, I trained a binary classification model using Logistic Regression that predicts, given a specific time I return home, how likely I will find a parking lot nearest to my block.

If you're interested in more details of how I developed ParkWhere, check out [this Medium article](https://towardsdatascience.com/how-i-built-my-own-real-time-parking-availability-predictive-model-31332e1b7747?source=friends_link&sk=f46426c23c938ed05f996925c4b225a0)!