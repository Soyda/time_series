from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Float, String, Boolean, SmallInteger, CheckConstraint
from sqlalchemy.orm import sessionmaker

from utils import get_data, get_meteo_data#, store_data

engine = create_engine('sqlite:///db_sncf.sqlite')
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


class ObjetTrouve(Base):
    __tablename__ = "ObjetTrouve"

    id = Column(Integer, primary_key=True)
    gare_origine_nom = Column(String)
    type_objet = Column(String)
    objet = Column(String)
    date_perdu = Column(String)
    date_rendu = Column(String)

class Meteo(Base):
    __tablename__ = "Meteo"

    id = Column(Integer, primary_key=True)
    temperatureK = Column(Float)
    humidite = Column(Float)
    zone = Column(String)
    # coordonnees = Column(String)
    ville_ref = Column(String)
    date = Column(String)

Base.metadata.create_all(engine)

# vide les tables

Session = sessionmaker(bind=engine)
session = Session()
session.query(ObjetTrouve).delete()
session.query(Meteo).delete()

session.commit()

#remplit les tables
gares = ["Lille Flandres", "Lille Europe"]
year_start = 2016
year_end = 2023

lost_objects_data = get_data(gares=gares,year_start=year_start, year_end=year_end)
meteo_data = get_meteo_data(year_start=year_start, year_end=year_end)

# store_data(lost_objects_data=lost_objects_data,
#            meteo_data=meteo_data)

for row in lost_objects_data:
    session.add(ObjetTrouve(gare_origine_nom = row.get("gare_origine_nom"),
                            type_objet =  row.get("type_objet"),
                            objet =  row.get("objet"),
                            date_perdu =  row.get("date_perdu"),
                            date_rendu = row.get("date_rendu")
                            ))

for row in meteo_data:
    session.add(Meteo(temperatureK =  row.get("temperatureK"),
                            humidite =  row.get("humidite"),
                            zone =  row.get("zone"),
                            # coordonnees =  row.get("coordonnees"),
                            ville_ref =  row.get("ville_ref"),
                            date = row.get("date")
                            ))

session.commit()