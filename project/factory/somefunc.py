import requests
from database import Factory

def check_storage(factory_id, product_id):
    factory = Factory.query.filter_by(factory_id = factory_id).first()
    storage = factory.crafting_items.filter_by(product_id = product_id).first()
    print(storage)
    send_count = storage.craft_count + storage.product_storage#If items is storage add to delivary

    body = {}
    body['product_id'] = product_id
    body['count'] = send_count
    body['shop_id'] = storage.shop_id

    try:
        result = requests.post('http://127.0.0.1:80/api/shop/delivery', json = body)
    except requests.exceptions.ConnectionError:
        storage.product_storage += storage.craft_count #if connect error add to storage

    print('Success delivary {} factory {} to shop {}'.format(product_id, factory_id, body['shop_id']))     

def to_dict(database_object, SHEMA, many = False): #Convert Object to SHEMA in Python dict. If need handle list -> use many = True, but !!USE!! the list schema
    def convert_to_dict(database_object, SHEMA):
        dictionary = {}
        for params in SHEMA.properties:#Compare by database columns
            list_volume = [x.name for x in database_object.__table__.columns]
            if SHEMA.properties[params].get('type') == 'array':
                dictionary[params] = to_dict(getattr(database_object, params).all(), SHEMA.properties[params].get('items'), many = True)
            elif params in list_volume:
                dictionary[params] = getattr(database_object, params)#Adding without order
            else:
                dictionary[params] = None

            
        dictionary = {**SHEMA.properties, **dictionary}#Compare and arrange them in the right order

        return dictionary

    if many:
        list_dictionary_converted = []
        name_list = None# First element dict SHEMA (if use many)
        for param in SHEMA.properties:
            name_list = param
        if SHEMA.properties[name_list].get('type') == 'array':#check configuration models .array
            shema = SHEMA.properties[name_list].get('items')
        elif len(SHEMA.properties) == 1:#Check count properties
            shema = SHEMA.properties[name_list]
        else:
            shema = SHEMA
        for i in range(0, len(database_object)):#Handle list
            list_dictionary_converted.append(convert_to_dict(database_object[i], shema))
        if len(SHEMA.properties) != 1:
            return list_dictionary_converted
        
        dictionary = {}
        dictionary[name_list] = list_dictionary_converted
        return dictionary

    return convert_to_dict(database_object, SHEMA)

def tuple_to_dict(tuple_object, SHEMA, many = False):#many = True if need handle list, but !!USE!! the list schema

    #Convert tuple to dict. 
    #We arrange them according to the principle of 1 in the tuple, 1 in the SHEMA.properties. 2 in tuple, 2 in SHEMA.properties and etc.
    def convert_to_dict(tuple_object, SHEMA):
        dictionary = dict(zip(SHEMA.properties, tuple_object))
        
        return dictionary
    
    if many:
        list_dictionary_converted = []
        name_list = None# First element dict SHEMA (if use many)
        for param in SHEMA.properties:
            name_list = param

        if SHEMA.properties[name_list]['type']:#check configuration models .array
            shema = SHEMA.properties[name_list].get('items')
        elif SHEMA.properties[name_list]:
            shema = SHEMA.properties[name_list]
        print(shema)
        for i in range(0, len(tuple_object)):#Handle list
            list_dictionary_converted.append(convert_to_dict(tuple_object[i], shema))
        dictionary = {}
        dictionary[name_list] = list_dictionary_converted
        
        return dictionary
    
    return convert_to_dict(tuple_object, SHEMA)