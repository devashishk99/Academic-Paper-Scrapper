import streamlit as st #open-source framework to build quick webapps
import pandas as pd # data analysis and manipulation library
from scrapper import Scraper # the scrapper class used to scrap the webpage
from mastodonBot import MastodonBot # the mastodon class used to toot a status
from tfIdf import get_keywords # importing the function that extracts document keywords
import time

scrappy = Scraper()  # instantiating the scrapper object
mBot = MastodonBot() # instantiating the mastodon object

botFlag = False

def tootPapers(papers):
    star_emoji            = u'\U00002B50'
    paper_emojj           = u'\U0001F4C4'
    upward_trend_emoji    = u'\U0001F4C8'
    link_emoji            = u'\U0001F517'
    source_emoji          = u'\U0001F4AB'
    exclaim_emoji         = u'\U00002757'

    toots = [] # list to store all toots
    title = exclaim_emoji*3 + ' Trending Top 10 AI Papers ' + exclaim_emoji*3 + '\n'
    credits = 'Source & Credits - https://paperswithcode.com/ ' + source_emoji
    tooty = ''
    for (i, paper) in enumerate(papers): # iterating through all papers
        tooty = ''
        if i == 0: # check if first toot
            tooty += title # add title to first toot
        #formatting for the toots
        tooty += '[' + str(i+1) + '/' + str(len(papers)) + '] '  + upward_trend_emoji  + ' '  + paper['title'] + ' \n Rating - ' + paper['nb_stars'] + ' ' + star_emoji + ' \n Paper ' + paper_emojj + ' - ' + paper['pdf'] + ' \n Github ' + link_emoji + ' - ' + paper['github'] 
        if i == 9: # check if last toot
            tooty += '\n ' + credits # add credits to last toot
        print(tooty)
        toots.append(tooty) # add all toots to a list

    for (i, tooty) in enumerate(toots): # iterating through list of toots
        print('Toot' + str(i))
        mBot.toot(tooty) # toot as main status
        time.sleep(5) # sleep for 5ms
    print('Finished tooting!')
    st.balloons()
    
st.title('Academic Paper Scrapper') 
st.info("Displays the top 10 AI research papers and toots them on Mastodon.")

option = st.selectbox(
    'Do you want to post the results on your Mastodon app? Click No for view-only mode',
    ('No', 'Yes'))

if option == 'No': # if No then the flag to post on Mastodon is disabled
    postFlag = False
elif option == 'Yes':  #if Yes then the flag to post on Mastodon is enabled
    postFlag = True
    if not mBot.connect_to_mastodon_OAuth(): # since post flag is enabled check if ACCESS TOKEN exists 
        botFlag = True
        st.error('Please register an app on Mastodon and add ACCESS TOKEN!', icon='🚨')

st.caption('Click one of the following to get corresponding results:')

# splitting screen into 2 columns
col1, col2 = st.columns([1,1])
with col1:
    trending = st.button("Trending", disabled=botFlag) # trending papers button
with col2:
    latest = st.button("Latest", disabled=botFlag) # latest papers button


with st.spinner("Please wait.."): # gives user feedback as data is scrapped
    papers = [] # list to hold the papers data
    if trending:
        st.session_state["trending"] = True
        print('Trending papers...')
        papers = scrappy.scrapTrending() # gets the trending papers
    elif latest:
        st.session_state["latest"] = True
        print('Latest papers..')
        papers = scrappy.scrapLatest()  # gets the latest papers    

    abstracts = [d['abstract'] for d in papers] # stores the abstract of the papers
    abstract_keywords = get_keywords(abstracts) # calls the function to extract the keywords from the abstract
    del_key_list = ['image', 'hourly_stars'] # deleting the unwanted keys from dictionary
    for del_key in del_key_list:
        papersUpd = list(filter(lambda x: x.pop(del_key, None) or True, papers))
    papers_df = pd.DataFrame.from_dict(papersUpd) # converting dictionary to pandas DataFrame
    papers_df['keywords'] = abstract_keywords # adding the keywords as a new column to DataFrame
    if not papers_df.empty:
        st.table(papers_df) # displays the final paper data
        if postFlag:
            print('Im in')
            tootPapers(papersUpd) # toots papers 
       