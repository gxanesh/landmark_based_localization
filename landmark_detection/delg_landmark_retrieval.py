import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub  # for model
import numpy as np

import warnings as warn
warn.filterwarnings("ignore")
# ref for app: https://www.kaggle.com/code/ayodejiyekeen/african-landmarks-classification-app
# Define prediction Function
def retrieve_landmark(image, TF_MODEL_URL, LABEL_MAP_URL):
    """
        :param:
        :image: input image of shape 321*321*3
        :TF_MODEL_URL: Deep local and global feature based Model URL
        :LABEL_MAP_URL: label map containing 96... labels
    """

    IMAGE_SHAPE = (321, 321)
    img = np.array(image) / 255.0
    img = img[np.newaxis, ...]
    classifier = tf.keras.Sequential([hub.KerasLayer(TF_MODEL_URL,
                                                     input_shape=IMAGE_SHAPE + (3,),
                                                     output_key="predictions:logits")])
    # set verbose=0 to remove the time progress bar
    prediction = classifier.predict(img, verbose=0)
    df = pd.read_csv(LABEL_MAP_URL)
    label_map = dict(zip(df.id, df.name))
    return label_map[np.argmax(prediction)]
