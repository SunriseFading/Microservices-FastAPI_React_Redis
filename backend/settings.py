import environs

env = environs.Env()
env.read_env('.env')

HOST = env('HOST')
PORT =  env.int('PORT')
PASSWORD = env('PASSWORD')
FRONTEND_URL = env('FRONTEND_URL')
BACKEND_URL = env('PRODUCTS_URL')
