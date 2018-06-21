from keras.applications import ResNet50

res_net_50 = None


def get_res_net_50() -> ResNet50:
    global res_net_50
    if res_net_50 is not None:
        return res_net_50
    print("Please wait. Initializing ResNet50 model..")
    res_net_50 = ResNet50(weights="imagenet")
    return res_net_50
