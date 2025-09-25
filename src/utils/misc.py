from flask_caching import Cache
#not used anymore since using bootstrap layouts now
colors = {
        'chart_gridcolor':'#727272',
        'text': "#FFFFFF"
}

#to avoid a circulart import we define the cache here: 

#Defining a simple Cache
cache = Cache()