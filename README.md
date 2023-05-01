# Annaotation File
Welcome to this project. this projects allow to annotate csv file, it take in entry a csv file and it product at the output 3 csv file: cea.csv, cta.csv, cpa.csv after done search in wikidata

## Dependencies
this projects is build with python languange, thus rassure that you have python version>=3.8 in you computer, then install all dependencies in requirements.txt with this command:

```
pip install -r requirements.tx
```
rassure that you virtual environnement activate in your projects else following these instructions in terminal:
- linux os
   ```
   python -m venv myenv
   ```

   ```
      source myenv/bin/activate
   ```

- windows os (in using git bash as terminal)
   ```
   python -m venv myenv
   ```

   ```
   source myenv/Scripts/activate
   ```


## Stack
navigate inside folder [helpers](./helpers/) at inside we have a dataset folder and to main files called wikidata.py and foodon.py.<br>
navigate inside [dataset folder](./helpers/dataset/) ans copy-paste your cleaned csv file inside

### wikidata

Follow these instructions:
1. in main.py file we have 03 main function known as openFilecsvCea(), openFilecsvCta() and openFilecsvCpa(). at the end of script you can uncomment the call of these functions. Note that each function is independant.

2. to execute the program for annotate wikidata files run this command in terminal
   ```
      python wikidata.py
   ```
3. at the end of this execution you can see result of annotation, navigate inside [wikidata folder](./wikidata/). you will see three file cea.csv cta.csv and cpa.csv

### foodon
Follow these instructions:
1. in main.py file we have 03 main function known as openFilecsvCea(), openFilecsvCta() and openFilecsvCpa(). at the end of script you can uncomment the call of these functions. Note that each function is independant.

2. to execute the program for annotate wikidata files run this command in terminal
   ```
      python foodon.py
   ```
3. at the end of this execution you can see result of annotation, navigate inside [foodon folder](./wikidata/). you will see three file cea.csv cta.csv and cpa.csv


## deployment 

## Author
@jeanpetit

