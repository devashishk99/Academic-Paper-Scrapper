# Academic-Paper-Scrapper

In this project, I have created a web scrapper which extracts data about Academic Research Papers related to AI from https://paperswithcode.com/ and toots them on Mastodon.

## Initial Setup:

Clone repo and create a virtual environment
```
$ git clone https://github.com/devashishk99/Academic-Paper-Scrapper.git
$ cd Academic-Paper-Scrapper
$ python3 -m venv venv
```
### Activate virtual environment
Mac / Linux:
```
. venv/bin/activate
```
Windows:
```
venv\Scripts\activate
```
Install dependencies
```
$ pip install -r requirement.txt 
```
Install xml library (For Macs)
```
$ STATIC_DEPS=true pip install lxml
```

Install nltk package
```
$ (venv) python
>>> import nltk
>>> nltk.download('punkt')
```

Run
```
$ (venv) streamlit run main.py
```

This is will redirect to the localhost in the browser, where you can start interacting with the app by clicking on the type of research paper (Trending/Latest) you want to view and toot.

![Alt Text](https://github.com/devashishk99/Academic-Paper-Scrapper/blob/main/image.png)

