import streamlit as st
from streamlit_folium import folium_static
import geemap.eefolium as geemap
import ee
from datetime import datetime

#os.environ["EARTHENGINE_TOKEN"] == st.secrets["EARTHENGINE_TOKEN"]

with st.echo():
    import streamlit as st
    from streamlit_folium import folium_static
    import geemap.eefolium as geemap
    import ee
    from datetime import datetime
    def maskL8clouds(image):
      cloudBitMask = ee.Number(2).pow(3).int()
      qa = image.select('QA_PIXEL')
      mask = qa.bitwiseAnd(cloudBitMask).eq(0)
      return image.updateMask(mask)

    def dates(image):
      date = image.date().format("YYYY-MM-dd")
      return date
    
    current_date = datetime.today().strftime('%Y-%m-%d')
    start = ee.Date('2018-01-01')
    end = ee.Date(current_date)
    
    landsat = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")     .filterDate(start, end).filter(ee.Filter.Or(
        ee.Filter.And(ee.Filter.eq('WRS_PATH', 39),
                      ee.Filter.eq('WRS_ROW', 32)),
        ee.Filter.And(ee.Filter.eq('WRS_PATH', 39),
                      ee.Filter.eq('WRS_ROW', 31)))).map(maskL8clouds)
    
    selector = -1 
    offset = 0 
    landsat_S = landsat.filter(ee.Filter.Or(
        ee.Filter.And(ee.Filter.eq('WRS_PATH', 39),
                      ee.Filter.eq('WRS_ROW', 32))))

    landsat_S_list = landsat_S.toList(landsat_S.size())
    S_img = ee.Image(landsat_S_list.get(selector))
    S_img_date = S_img.get('DATE_ACQUIRED')

    landsat_N = landsat.filter(ee.Filter.Or(
        ee.Filter.And(ee.Filter.eq('WRS_PATH', 39),
                      ee.Filter.eq('WRS_ROW', 31))))
    landsat_N_list = landsat_N.toList(landsat_N.size())
    N_img = ee.Image(landsat_N_list.get(selector+offset))
    N_img_date = N_img.get('DATE_ACQUIRED')
    vis_params = {'bands': ['SR_B4', 'SR_B3', 'SR_B2'], 'min': 0, 'max': 29000, 'gamma': [0.6, 0.6, 0.6]}
    Map = geemap.Map(center=(40.8410, -113.4853), zoom=10)
    Map.addLayer(N_img, vis_params, 'N image', True, 1)
    Map.addLayer(S_img, vis_params, 'S image', True, 1)
    Map.addLayerControl()
    folium_static(Map)

