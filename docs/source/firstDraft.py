def add_join_DruhPozemku(self, parcely_layer: QgsVectorLayer, csv_name: str = "druh_pozemku.csv") -> QgsVectorLayer:
    """Joins a .csv (code list of land types with description) to layer 'Parcely'
    """
    path = os.path.join(os.path.dirname(__file__), "files", csv_name)
    csv_layer = QgsVectorLayer(path, "DruhPozemku", "delimitedtext")
    targetFieldName = "DruhPozemkuKod"
    joinFieldNamesSubset = ["NAZEV"]
    joinFieldName = "KOD"


    joinObject = QgsVectorLayerJoinInfo()
    joinObject.setJoinLayerId(csv_layer.id())
    joinObject.setJoinFieldName(joinFieldName)
    joinObject.setTargetFieldName(targetFieldName)
    joinObject.setUsingMemoryCache(True)
    joinObject.setJoinLayer(csv_layer)
    joinObject.setJoinFieldNamesSubset(joinFieldNamesSubset)

    parcely_layer.addJoin(joinObject)

    return parcely_layer # vracet tu vrstvu mne prijde rozumnejsi/lepsi koncept nez to rovnou zapisovat do instance
    # QgsProject.instance().addMapLayer(parcely_layer)
    # rearrange columns: https://gis.stackexchange.com/a/445885 (ALE POTREBUJI CELEJ LIST SLOUPCU ASI)
    # import csv to SQLite: https://www.geeksforgeeks.org/how-to-import-a-csv-file-into-a-sqlite-database-table-using-python/


def importCsv2Sqlite(self, data):
    import csv, sqlite3
    con = sqlite3.connect(":memory:") # QUEST: asi bude potreba vytvorit (novou) databazi nejdriv?
    cur = con.cursor()
    cur.execute("""CREATE TABLE druh_pozemku (
                    KOD int primary key,
                    NAZEV text, 
                    ZEMEDELSKA_KULTURA varchar(1), 
                    PLATNOST_OD text, 
                    PLATNOST_DO text, 
                    ZKRATKA text, 
                    TYPPPD_KOD int, 
                    STAVEBNI_PARCELA varchar(1), 
                    POVINNA_OCHRANA_POZ int, 
                    POVINNY_ZPUSOB_VYUZ varchar(1));""")
    with open(data, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';') #comma is default delimiter
        to_db = [(i["KOD"], i["NAZEV"], i["ZEMEDELSKA_KULTURA"], i["PLATNOST_OD"], i["PLATNOST_DO"], i["ZKRATKA"], i["TYPPPD_KOD"], i["STAVEBNI_PARCELA"], i["POVINNA_OCHRANA_POZ"], i["POVINNY_ZPUSOB_VYUZ"]) for i in reader] #QUEST: dlouhy jaxvist, jak na vic radku?

    cur.executemany("""INSERT INTO druh_pozemku (
                        KOD, 
                        NAZEV, 
                        ZEMEDELSKA_KULTURA, 
                        PLATNOST_OD, 
                        PLATNOST_DO, 
                        ZKRATKA, 
                        TYPPPD_KOD, 
                        STAVEBNI_PARCELA, 
                        POVINNA_OCHRANA_POZ, 
                        POVINNY_ZPUSOB_VYUZ) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""", to_db)
    con.commit()
    con.close()