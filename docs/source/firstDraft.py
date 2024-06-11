def add_join_csv_file(self, target_layer: QgsVectorLayer, target_field: str = "DruhPozemkuKod", csv_name: str = "druh_pozemku.csv", csv_field: str = "KOD", csv_subset: list = ["NAZEV"]) -> QgsVectorLayer:
    """Joins a .csv (code list of land types with description) to layer 'Parcely'
    """
    path = os.path.join(os.path.dirname(__file__), "files", csv_name)
    csv_layer = QgsVectorLayer(path, "DruhPozemku", "delimitedtext")

    joinObject = QgsVectorLayerJoinInfo()
    joinObject.setJoinLayerId(csv_layer.id())
    joinObject.setJoinFieldName(csv_field)
    joinObject.setTargetFieldName(target_field)
    joinObject.setUsingMemoryCache(True)
    joinObject.setJoinLayer(csv_layer)
    joinObject.setJoinFieldNamesSubset(csv_subset)

    target_layer.addJoin(joinObject)

    return target_layer 
    # rearrange columns: https://gis.stackexchange.com/a/445885 (ALE POTREBUJI CELEJ LIST SLOUPCU ASI)
    # import csv to SQLite: https://www.geeksforgeeks.org/how-to-import-a-csv-file-into-a-sqlite-database-table-using-python/


def importCsv2Sqlite(self, data):
    import csv, sqlite3
    con = sqlite3.connect(":memory:") # QUESTION: asi bude potreba vytvorit (novou) databazi nejdriv?
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
        to_db = [(i["KOD"], i["NAZEV"], i["ZEMEDELSKA_KULTURA"], i["PLATNOST_OD"], i["PLATNOST_DO"], i["ZKRATKA"], i["TYPPPD_KOD"], i["STAVEBNI_PARCELA"], i["POVINNA_OCHRANA_POZ"], i["POVINNY_ZPUSOB_VYUZ"]) for i in reader] #QUESTION: dlouhy jaxvist, jak na vic radku?

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

def main():
    uri = "Parcely.gpkg"
    add_join_csv_file(QgsVectorLayer(uri, "Parcely2", "ogr"))

if __name__ == "__main__":
    main()       