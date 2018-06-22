from keras.applications import ResNet50, VGG19

res_net_50 = None


def get_res_net_50() -> ResNet50:
    global res_net_50
    if res_net_50 is not None:
        return res_net_50
    print("Please wait. Initializing ResNet50 model..")
    res_net_50 = ResNet50(weights="imagenet")
    return res_net_50


vgg_19 = None


def get_vgg_19() -> VGG19:
    global vgg_19
    if vgg_19 is not None:
        return vgg_19
    print("Please wait. Initializing VGG19 model..")
    vgg_19 = VGG19(weights="imagenet")
    return vgg_19


def get_model(name: str):
    name = name.lower()
    if name == 'resnet50':
        return get_res_net_50()
    elif name == 'vgg19':
        return get_vgg_19()
    else:
        raise ValueError('Model %s not exists. Available: %s' % (name, ', '.join(['resnet50', 'vgg19'])))
