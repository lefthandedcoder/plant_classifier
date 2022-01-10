import os
from PIL import Image, ImageFile
import io
from io import BytesIO
from tensorflow.keras.models import load_model
import base64
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.backend import expand_dims

ALLOWED_EXT = set(['jpg', 'jpeg'])
IMAGE_HEIGHT = 224
IMAGE_WIDTH = 224
IMAGE_CHANNELS = 3


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXT


classes = ['alfalfa',
           'allium',
           'borage',
           'burdock',
           'calendula',
           'cattail',
           'chickweed',
           'chicory',
           'chive_blossom',
           'coltsfoot',
           'common_mallow',
           'common_milkweed',
           'common_vetch',
           'common_yarrow',
           'coneflower',
           'cow_parsley',
           'cowslip',
           'crimson_clover',
           'crithmum_maritimum',
           'daisy',
           'dandelion',
           'fennel',
           'fireweed',
           'gardenia',
           'garlic_mustard',
           'geranium',
           'ground_ivy',
           'harebell',
           'henbit',
           'knapweed',
           'meadowsweet',
           'mullein',
           'pickerelweed',
           'ramsons',
           'red_clover']
app = Flask(__name__)
model = load_model('model.hdf5', compile=True)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return render_template('index.html', prediction="Please upload an image.")
    file = request.files['image']

    if file.filename == '':
        return render_template('index.html', prediction='Please select an image.')

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print("***" + filename)
        ImageFile.LOAD_TRUNCATED_IMAGES = False
        img = Image.open(BytesIO(file.read()))
        data = io.BytesIO()
        img.save(data, "JPEG")
        encoded_img_data = base64.b64encode(data.getvalue())
        img.load()
        img = img.resize((IMAGE_WIDTH, IMAGE_HEIGHT))
        img = img_to_array(img)/255.
        img = expand_dims(img, axis=0)
        result = model.predict(img)
        dict_result = {}
        for i in range(35):
            dict_result[result[0][i]] = classes[i]

        res = result[0]
        res.sort()
        res = res[::-1]
        prob = res[:3]

        prob_result = []
        class_result = []
        prob_result.append((prob[0] * 100).round(2))
        class_result.append(dict_result[prob[0]])
        return render_template('index.html', img_data=encoded_img_data.decode('utf-8'),
                               prediction='This is most likely an image of the wild edible plant '
                                          + str(class_result[0]) + ' with a confidence of ' + str(prob_result[0]) + '%')
    else:
        return render_template(prediction='Invalid file extension.')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
