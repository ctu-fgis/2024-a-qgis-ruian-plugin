import os
from qgis.core import QgsProject, QgsVectorLayer, QgsVectorLayerJoinInfo

def add_join(target_layer: QgsVectorLayer, 
             csv_layer: QgsVectorLayer, 
             target_field: str = "DruhPozemkuKod", 
             csv_field: str = "KOD", 
             csv_subset: list = ["NAZEV"]) -> QgsVectorLayer:
    """Performs left outer join from 'target_layer' to 'csv_layer'. Initially used to perform a join from 'Parcely' to code list of land types.
    
    @type target_layer: QgsVectorLayer
    @param target_layer: A layer on which the join will be performed
    @type csv_layer: QgsVectorLayer
    @param csv_layer: A layer which will be joined to the 'target_layer'
    @type target_field: str
    @param target_field: Name of the field of the 'target_layer' that will be used for join
    @type csv_field: str
    @param csv_field: Name of the field of the 'csv_layer' that will be used for join
    @type csv_subset: list
    @param csv_subset: Subset of fields to be used from joined layer
    
    @rtype: QgsVectorLayer
    @returns: A vector layer ('target_layer') with left outer join to other vector layer ('csv_layer') 
    """
    joinObject = QgsVectorLayerJoinInfo()
    joinObject.setJoinLayerId(csv_layer.id())
    joinObject.setJoinFieldName(csv_field)
    joinObject.setTargetFieldName(target_field)
    joinObject.setUsingMemoryCache(True)
    joinObject.setPrefix("")
    joinObject.setJoinLayer(csv_layer)
    joinObject.setJoinFieldNamesSubset(csv_subset)

    target_layer.addJoin(joinObject)

    return target_layer 
    

def rearrange_columns(layer: QgsVectorLayer, new_order: list) -> None:
    """
    Changes order of all columns in the layer
    
    :param layer: layer whose collumns are to be rearranged
    :param new_order: a list with a new order of columns
    """
    layer_attr_table_config = layer.attributeTableConfig()
    columns_config = layer_attr_table_config.columns()

    columns_new_order_dict = {column : new_order.index(column.name) for column in columns_config if
                              column.type == 0 and column.name in new_order}
    columns_new_order_list = sorted(columns_new_order_dict, key=columns_new_order_dict.get, reverse=False)

    layer_attr_table_config.setColumns(columns_new_order_list)
    layer.setAttributeTableConfig(layer_attr_table_config)

    return
    # rearrange columns: https://gis.stackexchange.com/a/445885 (ALE POTREBUJI CELEJ LIST SLOUPCU ASI)

def main():
    parcely_uri = os.path.join(os.path.dirname('__file__'), "test", "sample_data", "testData.gpkg") + "|layername=parcely"
    parcely_layer = QgsVectorLayer(parcely_uri, "parcely", "ogr")
    parcely_field = "DruhPozemkuKod"

    # headTail = os.path.split(os.path.dirname(__file__)) # TODO: po zarazeni do MainApp upravit cestu
    csv_path = os.path.join(os.path.dirname('__file__'), "files", "druh_pozemku.csv")
    csv_layer = QgsVectorLayer(f"file:///{csv_path}?delimiter=;", "DruhPozemku", "delimitedtext")
    csv_field = "KOD"

    add_join(parcely_layer, csv_layer, parcely_field, csv_field)
    QgsProject.instance().addMapLayer(parcely_layer)
    QgsProject.instance().addMapLayer(csv_layer, addToLegend=False)
    
    new_order = ['fid', 'gml_id', 'Id', 'Nespravny', 'KmenoveCislo', 'PododdeleniCisla',
                 'VymeraParcely', 'ZpusobyVyuzitiPozemku', 'DruhCislovaniKod', 
                 'DruhPozemkuKod', 'NAZEV'
                 'KatastralniUzemiKod', 'PlatiOd', 'PlatiDo', 'IdTransakce', 'RizeniId',
                 'BonitovanyDilVymera', 'BonitovanyDilBonitovanaJednotkaKod', 'BonitovanyDilIdTranskace',
                 'BonitovanyDilRizeniId', 'ZpusobOchranyKod', 'ZpusobOchranyTypOchranyKod',
                 'ZpusobOchranyIdTransakce', 'ZpusobOchranyRizeniId']
    rearrange_columns(parcely_layer, new_order)

if __name__ in ('__main__', '__script__', '__console__'):
    main()
