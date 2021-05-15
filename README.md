# Beeldverwerking: Detectie van verkeersborden met de Hough-transformatie
Dit is een project van Beeldverwerking waarbij verkeersborden kunnen gedetecteerd worden met behulp van de cirkel Hough-transformatie.


Universiteit Gent \
Faculteit Ingenieurswetenschappen en architectuur \
Opleiding Industriële Wetenschappen Elektronica-ICT \
Academiejaar 2019-2020

Auteurs: Maxime Carella, Felix De Muelenaere, Stephanie Maes, Laurens Van Goethem \
Project onder begeleiding van: dr. Ir. Jan Aelterman

## Inhoud

- **images**: map met datasets van dag, nacht, original (initiele afbeeldingen), road (internet afbeeldingen), schemering
- **Video**: map met videobeelden van dag, nacht, schemering, veelsigns.mp4 (combinatie van enkele video's)
- **main.py**: hoofdbestand om de methoden te tonen met de testbench
- **DEMO.py**: Demo bestand, toont mengeling van video's
- **testbench.py**: Bestand dat video's of afbeeldingen binnenneemt en er processietechnieken op toepast 
- **hough.py**: Bestand dat de Houdh-transformatie behandelt en de bekomen cirkels manipuleert
- **segmentation.py**: Bestand dat de segmentatie van het beeld behandelt
- **Kalman.py**: Bestand dat gebruikt wordt bij de kalman filter implementatie

## Gebruik

Het project gebruikt python 3.7 \
De packages (zie versie controle) kunnen geïnstalleerd worden met pip:

    pip install -r requirements.txt
    
**Main.py**

Hoofdbestand om de methoden te evalueren op de datasets

argumenten:
- method: naam van de methode
    - videos
    - images
- dataset: naam van de dataset in de mappen
    - videos:
        - dag
        - nacht
        - schemering
    - images:
        - dag
        - nacht
        - Original
        - Road
        - schemering

gebruik:

    python main.py --method videos --dataset dag
    
**DEMO.py**

Speelt enkele voorbeeldfilmen af.

gebruik:

    python DEMO.py
    
## Versie controle

OS: Windows 10

IDE: JetBrains Pycharm 2019.2.2 (Professional Edition)

Python 3.7.1

Packages
- numpy 1.17.4
- matplotlib 3.1.1
- opencv-python 4.1.2.30
- scikit-video 1.1.11
- numba 0.46.0
- pillow 6.2.1
- imutils 0.5.3
- argparse 1.4.0
