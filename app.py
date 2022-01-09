import os
from tensorflow.keras.models import load_model
from flask import Flask, render_template, request
from tensorflow.keras.preprocessing.image import load_img , img_to_array
from tensorflow.keras.backend import expand_dims

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = load_model(os.path.join(BASE_DIR, 'model.hdf5'))
ALLOWED_EXT = set(['jpg', 'jpeg', 'png'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXT


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


def predict(filename, model):
    img = load_img(filename, target_size = (224, 224))
    img = img_to_array(img)/255.
    img = expand_dims(img, axis = 0)
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
    prob_result.append((prob[0]*100).round(2))
    class_result.append(dict_result[prob[0]])

    return class_result, prob_result


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/results', methods=['GET', 'POST'])
def success():
    error = ''
    target_img = os.path.join(os.getcwd(), 'static/images')
    if request.method == 'POST':
        if (request.files):
            file = request.files['file']
            if file and allowed_file(file.filename):
                file.save(os.path.join(target_img, file.filename))
                img_path = os.path.join(target_img, file.filename)
                img = file.filename
                class_result, prob_result = predict(img_path, model)
                predictions = {
                    "class1": class_result[0],
                    "prob1": prob_result[0]
                }
            else:
                error = "Please upload an image file"
            if len(error) == 0:
                return render_template('results.html', img=img, predictions=predictions)
            else:
                return render_template('index.html', error=error)
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)

#testing