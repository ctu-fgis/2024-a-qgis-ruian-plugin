from qgis.core import QgsProject

csv = QgsProject.instance().mapLayersByName('SC_D_POZEMKU')[0]
csvField = 'KOD'
layer = QgsProject.instance().mapLayersByName('Parcely')[0]
layerField = 'DruhPozemkuKod'

joinObject = QgsVectorLayerJoinInfo()
joinObject.setJoinLayerId(csv.id())
joinObject.setJoinFieldName(csvField)
joinObject.setTargetFieldName(layerField)
joinObject.setPrefix('g')
joinObject.setUsingMemoryCache(True)
joinObject.setJoinLayer(csv)

layer.addJoin(joinObject)
QgsProject.instance().addMapLayer(layer)