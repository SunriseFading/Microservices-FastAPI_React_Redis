from main import redis, Product
import time

key = 'order_completed'
group = 'products-group'

try:
    redis.xgroup_create(key, group)
except Exception:
    print('Group already exists!')

while True:
    try:
        results = redis.xreadgroup(group, key, {key: '>'}, None)

        if results != []:
            for result in results:
                obj = result[1][0][1]
                try:
                    product = Product.get(obj['product_pk'])
                    product.quantity = product.quantity - int(obj['quantity'])
                    product.save()
                except Exception:
                    redis.xadd('refund_order', obj, '*')

    except Exception as e:
        print(e)
    time.sleep(1)
