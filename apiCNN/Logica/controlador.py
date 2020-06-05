from io import BytesIO
from six.moves import urllib
from keras.preprocessing import image
from tensorflow.keras.models import model_from_json
from keras.preprocessing.image import load_img
from keras import backend as k
import numpy as np

def predecirImg(url_imagen):
    TAM_IMG = (150, 150)

    url_modelo = r'apiCNN/Logica/architectura_optimizada.json'
    url_pesos = r'apiCNN/Logica/pesos_optimizados.h5'

    modelo = cargar_modelo(url_modelo, url_pesos)

    img = load_img(url_imagen, target_size=TAM_IMG)
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img /= 255
    print(img)
    resultado = modelo.predict(img)
    rst = None
    for i in resultado:
        rst = i
    rst*=100

    prd = max(rst)
    inx, = np.where(np.isclose(rst, prd))

    if int(inx[0]) == 0:
        return 'La imagen es: buildings', prd
    elif int(inx[0] == 1):
        return 'La imagen es: forest', prd
    elif int(inx[0] == 2):
        return ' La imagen es: glacier', prd
    elif int(inx[0] == 3):
        return 'La imagen es: mountain', prd # <-- CUIDADO
    elif int(inx[0] == 4):
        return 'La image es: sea', prd
    elif int(inx[0] == 5):
        return 'La image es: street', prd


def cargar_modelo(url_modelo, url_pesos):
    k.reset_uids()
    with open(url_modelo, 'r') as f:
        print('INTENTA LEER <<___ ' * 5)
        model = model_from_json(f.read())
        print('FINALIZA EL LEER <----' * 10)
    # Cargar Pesos (weights) en el nuevo modelo.json
    model.load_weights(url_pesos)
    print("Red Neuronal Cargada desde Archivo")
    return model