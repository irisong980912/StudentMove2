# Instructions to run 

1. Navigate to project folder
2. Run `pip3 install -r "requirements.txt"`
3. Run `python3 app.py`
4. Navigate to localhost on browser 

# Notes for deployment to heroku

Procfile and Requirements.txt are already created.
Use the `git push heroku -f` command to deploy to remote

If push to heroku is not successful, it is because that the version specificed in `Requirements.txt` is outdated. please do the following:
1. `brew install gdal --HEAD` This will help install all the dependencies required by gdal.
2. use `pip3 list` to check the versions of the packages installed.
3. copy and paste the installed version numbers into `Requirements.txt` accordingly. 
