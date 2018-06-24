from keras.applications import ResNet50, VGG19, InceptionV3, Xception

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


incept_v3 = None


def get_incept_v3() -> InceptionV3:
    global incept_v3
    if incept_v3 is not None:
        return incept_v3
    print("Please wait. Initializing InceptionV3 model..")
    incept_v3 = InceptionV3(weights="imagenet")
    return incept_v3


xcept_v1 = None


def get_xcept_v1() -> InceptionV3:
    global xcept_v1
    if xcept_v1 is not None:
        return xcept_v1
    print("Please wait. Initializing Xception model..")
    xcept_v1 = Xception(weights="imagenet")
    return xcept_v1


def get_model(name: str):
    name = name.lower()
    if name == 'resnet50':
        return get_res_net_50()
    elif name == 'vgg19':
        return get_vgg_19()
    elif name == 'inceptv3':
        return get_incept_v3()
    elif name == 'xceptv1':
        return get_xcept_v1()

    raise ValueError('Model %s not exists. Available: %s' % (name, ', '.join(['resnet50', 'vgg19', 'inceptv3', 'xceptpv1'])))
