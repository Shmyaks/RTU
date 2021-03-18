"Дерево сервисов"

# Технологии
* Sqlalchemy
* Restfull api!
* Nginx

Сделанно 3 сервиса
1) Purchase serivce
2) Shop service
3) Factory service.

Каждый сервис имеет свой отдельный сервер. 
Работу с информацией, как я писал выше, помогает FLASK SQLALCHEMY.

В качестве базы данных выбрана postgresql. У каждого сервиса своя база данных.

Архитектура:

![Purple and Orange Shapes Electronics Facebook Feed Ad](https://user-images.githubusercontent.com/72697029/111568989-ddcc1500-87b2-11eb-8e92-c7b2c8a6e604.png)

Архитектура выглядит, как "Дерево" соответсвенно такое название.

# Routes

*   Purchses: (port 5000)

    * /api/purchase 
        * post - params[shop_id: int, products: list[dict], payment: choice['Cash', 'card'], purchase_name: string, user_id: int, check_id_shop: int, full_price: int, category_id_shop: int, category_shop: string]
            * Description: create purchase by shop
        * get - params[user_id: int]
            * Description: Get purhcases by user_id
        * delete - params[pruchase_id: int, user_id: ibt]
            * Description: Delete purchases on user
        * put - params[user_category_shop: int, payment: choice['cash', ''card'], user_id: int, purchase_id: int]

    * /api/user/<int:user_id>
        * get - params[user_id: int]
            * Decirption: get user by user_id
        * put - params[first_name: string, second_name: string]
            * Description: Change first_name or second_name'
            
    * /api/user/own_categories
        * get - params[user_id: int]
            * Description: Get user category bu user_id
        * post - params[user_id: int, user_category_name: string]
            * Description: Create user category for user
        * put - params[user_category_name: string, user_category_id: int, user_idL int]
            * Description: Change user_category. 

    * /api/user/register
        * post - params[first_name: string, second_name: string, password: string, login: string]
            * Description: Create user

    * /api/purchases
        * get - params[purchases_id: list[integer]]
            * Description: get purchases by purchases id.

*   Shop (port: 5001)

    * /api/shop/create_shop')
        * post - params[shop_name: string, shop_address: string, shop_phone: string]
            * Description: Create shop
            
    * /api/shop/<int:shop_id>')
        * get - params[shop_id: int]
            * Description: Get info by shop_id

    * /api/shop/categories')
        * get - params[shop_id]
            * Description: Get category by shop_id
        * post - params[category_name: string, shop_id: int]
            * Description: Create category in shop

    * /api/shop/products')
        * post - params[product_name: stirng, product_price: integer, product_description: string, category_id: integer, shop_id: integer]
            * Description: Add product to shop
        * get - params[shop_id: integer, products_id: list[integer]]
            * Description: Get products. You can get all products or by filter
        * put - params[product_name: string, product_price: integer, product_description: string, category_id integer, product_id: integer, shop_id: integer]
            * Description: Change info by product

    * /api/shop/buy')
        * post - params[payment: choice['Cash', 'Card'], products: list[dict], purchase_name: string, user_id: integer, shop_id: integer]
            * Description: Buy in shop.

    * /api/shop/checks')
        * get - params[shop_id: integer]
            * Description: Get checks by shop_id

    * /api/shop/checks/products')
        * post - params[checks_id: list[integer], shop_id: integer]
            * Description: Get products by checks. Work if purchase service is on
            
    * /api/shop/product/search')
        * get - params[shop_id: list[integer], category_idL list[integer], product_name: string]
            * Description: Serach in shops and caregories by product_name

    * /api/shop/delivery')
        * post - params[count: integer, shop_id: integer, product_id: integer]
            * Description: Delivery to shop. For Factory service

*   Factory (port: 5002)

    *  /api/factory
        *   post - params[factory_name: string]
            * Description: create factory
        *   get - params [factory_id: int]
            * Description: Get factories
        *   put - params [factory_id: int, factory_name: string]
            * Description: Change Factory
        *   delete - params [factory_id: int]
            * Description: delete factory

    *  /api/factory/craft
        *   post - params[factpry_id: int, product_id: int, shop_id: int, craft_count: int, interval_count: int]
            * Description: create craft for factory
        *   get - params[factory_id: int]
            * Desceiption: Get crafts factory
        *   put - params[factory_id: int, craft_id: int, product_id :int, shop_id : int, interval_delivary: int]
            * Description: Put craft by factory
# Tests

* purchase swagger: /api/purchase/doc
* shop swagger: /api/shop/doc
* factory swagger: /api/factory/doc

# Имеется Migration
* Она нужна для удобства в расширении базы данных.




