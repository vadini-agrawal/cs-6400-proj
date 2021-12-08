# cs-6400-proj
Project code for CS 6400

## Set up steps
1. Clone repo 
2. To run locally, you will most likely need to use [conda](https://docs.conda.io/en/latest/). Install Conda.
4. The requirements.txt includes the dependencies needed for the project. A command like this should work once you are in your conda environment: "conda create --name <env> --file <this file>". Make sure you are running Python 3. 
5. Download this file: https://drive.google.com/file/d/1k2bNgPDB5nPFJfyiiPziGx848q_pJuXH/view?usp=sharing and place it under the "Downloads" directory 
6. Download this folder of images: https://drive.google.com/file/d/1QZcJmGVlF9f4h-XLWe9Gkmnmj2z1gSnk/view?usp=sharing and place the "images" folder inside this directory under the "hico_20160224_det" folder under "app/static/data". The "train2015" images are the ones used in the app. 
7. "cd app" and run python3 app.py 
8. The app should be running on "http://127.0.0.1:5000/"
9. To view db:
   1. Download https://sqlitebrowser.org/
   2. Open "db/database.db" file there 
