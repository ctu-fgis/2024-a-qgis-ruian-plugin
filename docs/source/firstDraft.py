def add_join_DruhPozemku(self, parcely_layer):
    """Joins a .csv (code list of land types with description) to layer 'Parcely'
    """
    path = os.path.join(os.path.dirname(__file__), 'files','druh_pozemku.csv')
    csv_layer = QgsVectorLayer(path, 'druh_pozemku', 'delimitedtext')
    csvField = 'KOD'
    layerField = 'DruhPozemkuKod'

    joinObject = QgsVectorLayerJoinInfo()
    joinObject.setJoinLayerId(csv_layer.id())
    joinObject.setJoinFieldName(csvField)
    joinObject.setTargetFieldName(layerField)
    joinObject.setUsingMemoryCache(True)
    joinObject.setJoinLayer(csv_layer)
    joinObject.setJoinFieldNamesSubset("NAZEV")

    parcely_layer.addJoin(joinObject)
    QgsProject.instance().addMapLayer(parcely_layer)