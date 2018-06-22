import requests

from main.configuration import services_urls


def generate_service_url(service, path: str) -> str:
    return "%s/%s" % (services_urls[service], path.lstrip('/'))


def ask_for_predictions(img, service, top) -> dict:
    if top < 5:
        top = 5
    img.seek(0)
    files = {"image": (img.filename, img.stream, img.mimetype)}
    resp = requests.post(generate_service_url(service, "/image/analyze"), params=dict(top=top), files=files)
    return resp.json()


def make_score(model, score):
    return dict(model=model, score=score)


def map_predictions(responses) -> dict:
    predictions = dict()
    for response in responses:
        for prediction in response["predictions"]:
            pred_class = prediction["class_description"]
            score = make_score(response["used_model"], prediction["score"])

            if pred_class in predictions:
                predictions[pred_class].append(score)
            else:
                predictions[pred_class] = [score]

    return predictions


def aggregate(img, top=None):
    if top is None:
        top = 5
    top = int(top)

    responses = [ask_for_predictions(img, service, top) for service in ["resnet50", "vgg19"]]

    mapped_predictions = map_predictions(responses)
    predictions = []
    for label, scores in mapped_predictions.items():
        score = 0.
        for partial in scores:
            score = score + float(partial["score"])
        predictions.append(dict(label=label, score=str(score), scores=scores))

    predictions = sorted(predictions, key=lambda k: k['score'], reverse=True)

    return {
        "predictions": predictions[:top],
        "file_info": {
            "name": img.filename
        }
    }
