import requests
from sqlalchemy.orm import sessionmaker
# from get_store_data import ObjetTrouve, Meteo, engine

def get_data(gares, year_start, year_end):
    """Load data of SNCF about lost objects in Lille Europe

    Args:
        gares (_type_): _description_
        year_start (_type_): _description_
        year_end (_type_): _description_

    Returns:
        _type_: _description_
    """

    data = list()
    for date in range(year_start, year_end+1):
        for gare in gares:
            gare = "+".join(gare.split())
            # print(gare, date)
            res = requests.get(f"https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=lille&rows=10000&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.gc_obo_gare_origine_r_name={gare}&refine.date={date}").json()
            
            for row in res["records"]:
                # print(row)
                # id = row["recordid"]
                # gare_origine_id = row["fields"]["gc_obo_gare_origine_r_code_uic_c"]
                gare_origine_nom = row["fields"]["gc_obo_gare_origine_r_name"]
                type_objet = row["fields"]["gc_obo_type_c"]
                objet = row["fields"]["gc_obo_nature_c"]
                # recordtype = row["fields"]["gc_obo_nom_recordtype_sc_c"]
                date_perdu = row["fields"]["date"]

                if "gc_obo_date_heure_restitution_c" in row["fields"].keys():
                    date_rendu = row["fields"]["gc_obo_date_heure_restitution_c"]
                    new_row = {#"id":id,
                                # "gare_origine_id":gare_origine_id,
                                "gare_origine_nom":gare_origine_nom,
                                "type_objet":type_objet,
                                "objet":objet,
                                # "recordtype":recordtype,
                                "date_perdu":date_perdu,
                                "date_rendu":date_rendu}
                    data.append(new_row)
                else :
                    new_row = {#"id":id,
                                # "gare_origine_id":gare_origine_id,
                                "gare_origine_nom":gare_origine_nom,
                                "type_objet":type_objet,
                                "objet":objet,
                                # "recordtype":recordtype,
                                "date_perdu":date_perdu}
                    data.append(new_row)

    return data

def get_meteo_data(year_start, year_end):
    """Load meteo from a date to another for Lille area

    Args:
        year_start (_type_): _description_
        year_end (_type_): _description_

    Returns:
        _type_: _description_
    """
    data = list()
    for date in range(year_start, year_end+1):
        res = requests.get(f"https://public.opendatasoft.com/api/records/1.0/search/?dataset=donnees-synop-essentielles-omm&q=lille&rows=10000&facet=date&facet=nom&facet=temps_present&facet=libgeo&facet=nom_epci&facet=nom_dept&facet=nom_reg&refine.nom=LILLE-LESQUIN&refine.date={date}").json()
            
        for row in res["records"]:
            # print(row)
            id = row["recordid"]
            temperatureK = row["fields"]["t"]
            # climat = row["fields"]["temps_present"]
            humidite = row["fields"]["u"]
            # vent_mps = row["fields"]["ff"]
            # pression_station = row["fields"]["pres"]
            # pression_mer = row["fields"]["pmer"]
            zone = row["fields"]["nom"]
            coordonnees = row["fields"]["coordonnees"]
            ville_ref = row["fields"]["libgeo"]
            date = row["fields"]["date"]

            new_row = {"id":id,
                        "temperatureK":temperatureK,
                        # "climat":climat,
                        "humidite":humidite,
                        # "vent_mps":vent_mps,
                        # "pression_station":pression_station,
                        # "pression_mer":pression_mer,
                        "zone":zone,
                        "coordonnees":coordonnees,
                        "ville_ref":ville_ref,
                        "date":date}
            data.append(new_row)

    return data

# def store_data(lost_objects_data, meteo_data):

#     Session = sessionmaker(bind=engine)
#     session = Session()


#     for row in lost_objects_data:
#         session.add(ObjetTrouve(gare_origine_nom = row.get("gare_origine_nom"),
#                                 type_objet =  row.get("type_objet"),
#                                 objet =  row.get("objet"),
#                                 date_perdu =  row.get("date_perdu"),
#                                 date_rendu = row.get("date_rendu")
#                                 ))

#     for row in meteo_data:
#         session.add(Meteo(temperatureK =  row.get("temperatureK"),
#                                 humidite =  row.get("humidite"),
#                                 zone =  row.get("objet"),
#                                 # coordonnees =  row.get("coordonnees"),
#                                 ville_ref =  row.get("ville_ref"),
#                                 date = row.get("date")
#                                 ))

#     session.commit()