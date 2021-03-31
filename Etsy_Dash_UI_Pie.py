
import numpy as np
import pickle
import pandas as pd
import webbrowser
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

global data
data=pd.read_csv("Etsy_Scrapped_Reviews.csv")


global pickle_model
file = open("pickle_model.pkl", 'rb') 
pickle_model = pickle.load(file)

global vocab
file = open("feature.pkl", 'rb') 
vocab = pickle.load(file)
predict=[]
reviewText=data.iloc[:, 0]
    
transformer = TfidfTransformer()
loaded_vec = CountVectorizer(decode_error="replace",vocabulary=vocab)
vectorised_review = transformer.fit_transform(loaded_vec.fit_transform(reviewText))   
pred=pickle_model.predict(vectorised_review)  
data['Positivity']  =pred
data['Sentiment']  =None


data['Sentiment']=np.where(data['Positivity']==1,'Positive','Negative')
global pie_data
pie_data=data['Sentiment']

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
#project_name = "Sentiment Analysis with Insights"

def open_browser():
    webbrowser.open_new('http://127.0.0.1:8050/')
    
def create_app_ui():
    main_layout = html.Div([
            
        dcc.Graph(id='Pie',figure=px.pie(data_frame=data,names=data['Sentiment']),style={'color':"pink"}),
        html.H1(id='name',children='Pie Chart For Etsy Reviews!!',style={"margin-left": "250px",'width':'250px','font-size': '50px','font-weight': 'bold',}),
        
     ]
        
    )
    
    return main_layout





def main():
    print("Start of your project")
    
    open_browser()
    #update_app_ui() 
    global scrappedReviews
    global app
    
    project_name = "Sentiment Analysis with Insights"
    print("My project name = ", project_name)
    #print('my scrapped data = ', scrappedReviews.sample(5)    
    app.layout = create_app_ui()
    app.run_server()
    
    
    
    print("End of my project")
    project_name = None
    scrappedReviews = None
    app = None
    
        
# Calling the main function 
if __name__ == '__main__':
    main()