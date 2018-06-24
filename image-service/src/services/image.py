import numpy as np
from keras.applications import imagenet_utils
from keras.applications.resnet50 import decode_predictions
from keras.preprocessing.image import img_to_array

from services.model import get_model

ALLOWED_EXTENSIONS = {"jpg", "jpeg"}


def allowed_extension(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def prepare_image(img, target):
    """

    :param img: PIL.Image
    :param target:
    """

    # if the image mode is not RGB, convert it
    if img.mode != "RGB":
        img = img.convert("RGB")

    # resize the input image and preprocess it
    img = img.resize(target)
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = imagenet_utils.preprocess_input(img)

    # return the processed image
    return img


def analyze(img, top=3):
    """

    :param top: int
    :param img: PIL.Image
    """
    if top is None:
        top = 3
    top = int(top)

    # prepare img
    prepared_img = prepare_image(img, (224, 224))

    # predict
    # predictions = get_res_net_50().predict(prepared_img)
    model_name = 'vgg19'
    predictions = get_model(model_name).predict(prepared_img)
    decoded_predictions = decode_predictions(predictions, top=top)[0]

    # transform data
    listed_predictions = list()
    for class_name, class_description, score in decoded_predictions:
        listed_predictions.append(dict(class_name=class_name, class_description=class_description, score=str(score)))

    return {
        "used_model": model_name,
        "predictions": listed_predictions,
        "file_info": {
            "original": {
                "dimensions": img_dimensions(img)
            },
            "prepared": {
                "dimensions": dimensions(224, 224)
            }
        },
    }


def img_dimensions(img):
    width, height = img.size
    return dimensions(width, height)


def dimensions(width, height) -> dict:
    return dict(width=width, height=height)
