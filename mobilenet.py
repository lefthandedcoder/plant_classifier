import tensorflow

model = tensorflow.keras.applications.MobileNetV2(
    include_top=False,
    input_shape=(224,224,3),
    weights='imagenet')

model.summary()
model.save('mobilenet.hdf5')
