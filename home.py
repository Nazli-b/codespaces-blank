import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Données Statistiques",
    page_icon="📈",
    layout = wide
)

from constantes import SEXE, MOIS, CATEGORIES_VEHICULES_GROUPE, TRAJET, GRAVITE, ATM, OBSM

dataUsagers = pd.read_csv("datas/usagers.csv", sep=";")
dataVehicules = pd.read_csv("datas/vehicules.csv", sep=";")
dataLieux = pd.read_csv("datas/lieux.csv", sep=";")
dataCaracteristiques = pd.read_csv("datas/carcteristiques.csv", sep=";", decimal=',')

def get_day_of_week(date):
    days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    return days[date.weekday()]

def add_all_option(options):
    options = ["Tous"] + options
    return options

st.header("Statistiques sur les accidents corporels de la circulation routière")
col1, col2= st.columns(2)

#Le nombre d'accidents.
nombreaccidentvehicule= dataVehicules['Num_Acc'].nunique()
 
#Le nombre de véhicules impliqués.
nombrevehiculeimplique= dataVehicules['id_vehicule'].nunique()
 
#Le nombre d'usagers impliqués.
nombreusagerimplique=dataUsagers['id_usager'].nunique()
 
#Le nombre de décès.
nombredeces=len(dataUsagers[dataUsagers['grav'] == 2])
 
#Le taux de létalité.
letalite = (nombredeces/nombreaccidentvehicule)*100
letalite_formate = f"{letalite:.2f}%"
 
col1, col2, col3, col4, col5= st.columns([2,3,3,2,3])
col1.metric(label="🚧Nombre accident", value= nombreaccidentvehicule)
col2.metric(label="🚗Nombre de vehicule implique", value= nombrevehiculeimplique)
col3.metric(label="🧍Nombre d'usager impliqué", value= nombreusagerimplique)
col4.metric(label="💀Nombre de décès", value= nombredeces)
col5.metric(label="⚰️Taux de létalité", value= letalite_formate)


col1, col2= st.columns([3,3])

#Graphique Courbe du nombre d'accident par mois 
monthAccident = dataCaracteristiques[['Accident_Id', 'mois']]
nbAccidentByMonth = monthAccident.groupby(by='mois').count().reset_index()
nbAccidentByMonth['mois'] = nbAccidentByMonth['mois'].map(MOIS)

fig = px.line(nbAccidentByMonth, x='mois', y='Accident_Id', 
            labels={'mois': "mois", 'Accident_Id': "Nombre d'accidents"},
            title="Nombre d'accidents par mois")
col1.plotly_chart(fig, use_container_width=True)

#Graphique Courbe du nombre d'accident par jour de semaine 
dataCaracteristiques['date'] = pd.to_datetime(dataCaracteristiques['an'].astype(str) + '-' + dataCaracteristiques['mois'].astype(str) + '-' + dataCaracteristiques['jour'].astype(str), format='%Y-%m-%d')
dataCaracteristiques['jour_semaine'] = dataCaracteristiques['date'].apply(get_day_of_week)

dayAccident = dataCaracteristiques[['Accident_Id', 'jour_semaine']]
nbAccidentByDay = dataCaracteristiques.groupby('jour_semaine').count().reset_index()

jours_semaine_ordre = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
nbAccidentByWeekday = nbAccidentByDay.set_index('jour_semaine').reindex(jours_semaine_ordre).reset_index()

fig = px.line(nbAccidentByWeekday, x='jour_semaine', y='Accident_Id', 
            labels={'jour_semaine': "Jour de semaine", 'Accident_Id': "Nombre d'accidents"},
            title="Nombre d'accidents par jour de semaine")
col2.plotly_chart(fig, use_container_width=True)


##Nombre d'usager par gravité d'accident
gravite=dataUsagers[['id_usager', 'grav']]
gravite = gravite[gravite['grav'] > -1]
nbrusager=gravite.groupby(by='grav').count().reset_index()
 
nbrusager['grav'] = nbrusager['grav'].map(GRAVITE)
 
fignbrusager = px.bar(nbrusager, x='grav', y='id_usager',
                      labels={'grav': "Gravité", 'id_usager': "Nombre d'usager"},
                      title="Nombre d'usager par gravité d'accident")
   
st.plotly_chart(fignbrusager)

#Graphique Courbe du nombre d'accident par catégorie de véhicule 
categorie=dataVehicules[['Num_Acc', 'catv']]
categorie = categorie[categorie['catv'] > -1]
categorieimplique=categorie.groupby(by='catv').count().reset_index()
categorieimplique['catv'] = categorieimplique['catv'].map(CATEGORIES_VEHICULES_GROUPE)
fig = px.pie(categorieimplique, values='Num_Acc', names='catv', title="Répartition du nombre d'accidents par type de véhicule")
st.plotly_chart(fig)

#Graphique histogramme du nombre d'accident par type de trajet 
trajetAccident = dataUsagers[['Num_Acc', 'trajet']]
nbAccidentByTrajet = trajetAccident.groupby(by='trajet').count().reset_index()
nbAccidentByTrajet['trajet'] = nbAccidentByTrajet['trajet'].map(TRAJET)

fig = px.bar(nbAccidentByTrajet, x='trajet', y='Num_Acc', 
            labels={'trajet': "Type de trajet", 'Num_Acc': "Nombre d'accidents"},
            title="Répartition des accidents par type de trajet")
st.plotly_chart(fig, use_container_width=True)

#Graphique circulaire du nombre d'accident par sexe
sexeAccident = dataUsagers[['Num_Acc', 'sexe']]
sexeAccidentCleaned = sexeAccident[sexeAccident['sexe'] > -1]
nbAccidentBySexe = sexeAccidentCleaned.groupby(by='sexe').count().reset_index()

nbAccidentBySexe['sexe'] = nbAccidentBySexe['sexe'].map(SEXE)

fig = px.pie(nbAccidentBySexe, values='Num_Acc', names='sexe', title='Répartition des usagers par sexe')
st.plotly_chart(fig)

## Nombre d'accident par condition atmospherique

conditionat=dataCaracteristiques[['Accident_Id', 'atm']]
conditionat=conditionat[conditionat['atm'] > -1]
resconditionatmosph=conditionat.groupby(by='atm').count().reset_index()
 
resconditionatmosph['atm']= resconditionatmosph['atm'].map(ATM)
 
figconditionatmo = px.bar(resconditionatmosph, x='Accident_Id', y='atm',
                              labels={'Accident_Id': "Nombre d'accident", 'atm': "Condition atmosphérique"},
                              title="Nombre d'accident par condition atmospherique")
 
st.plotly_chart(figconditionatmo)

#La répartition des obstacles mobiles heurtés
obstaclemob = dataVehicules[['Num_Acc', 'obsm']]
obstaclemob = obstaclemob[obstaclemob['obsm'] > -1]
resobstaclemob=obstaclemob.groupby(by='obsm').count().reset_index()
 
resobstaclemob['obsm']= resobstaclemob['obsm'].map(OBSM)
 
figobstaclemob = px.pie(resobstaclemob , values='Num_Acc', names='obsm',
                         title="La répartition des obstacles mobiles heurtés")
 
st.plotly_chart(figobstaclemob)