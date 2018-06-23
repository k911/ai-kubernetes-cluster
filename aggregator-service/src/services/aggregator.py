import io

from requests_futures.sessions import FuturesSession

from main.configuration import services_urls

USED_SERVICES = ["resnet50", "vgg19", "xceptv1", "inceptv3"]


def generate_service_url(service, path: str) -> str:
    return "%s/%s" % (services_urls[service], path.lstrip('/'))


def resp_callback(session, response):
    response.original_url = response.history[0].url if response.history else response.url
    try:
        data = response.json()
    except ValueError:
        data = None
        print("Not valid JSON in received response to request: %s" % response.original_url)
    response.data = data


def ask_for_predictions(session, img, service, top):
    if top < 5:
        top = 5

    files = {"image": img}
    resp = session.post(generate_service_url(service, "/image/analyze"), params=dict(top=top), files=files,
                        background_callback=resp_callback)
    return resp


def make_score(model, score):
    return dict(model=model, score=score)


def parse_responses(responses: list) -> list:
    results = []
    for response in responses:
        response = response.result()
        original_url = response.history[0].url if response.history else response.url
        if response.status_code != 200:
            print("An error occurred requesting: %s" % original_url)
            continue

        if response.data is not None:
            results.append(response.data)

    return results


def map_predictions(results: list) -> dict:
    predictions = dict()
    for result in results:
        for prediction in result["predictions"]:
            pred_class = prediction["class_description"]
            score = make_score(result["used_model"], prediction["score"])

            if pred_class in predictions:
                predictions[pred_class].append(score)
            else:
                predictions[pred_class] = [score]

    return predictions


def make_result(label, score, scores) -> dict:
    return dict(label=label, score=score, scores=scores)


def parse_predictions(predictions: list, top: int) -> list:
    return [make_result(prediction["label"], str(prediction["score"]), prediction["scores"]) for prediction in
            predictions][:top]


def count_scores(predictions: iter) -> list:
    results = []
    for label, scores in predictions:
        score = 0.
        for partial in scores:
            score = score + float(partial["score"])
            results.append(make_result(label, score, scores))
    return results


def make_file(data, img):
    return img.filename, io.BytesIO(data), img.mimetype


def aggregate(img, top=None, models=USED_SERVICES):
    top = int(top or 5)
    img_data = img.read()
    img.close()

    max_workers = len(models)
    if max_workers > 10:
        max_workers = 10

    session = FuturesSession(max_workers=max_workers)
    responses = [ask_for_predictions(session, make_file(img_data, img), service, top) for service in models]
    results = parse_responses(responses)
    mapped_predictions = map_predictions(results)
    predictions = count_scores(mapped_predictions.items())
    predictions = sorted(predictions, key=lambda k: k['score'], reverse=True)

    return {
        "predictions": parse_predictions(predictions, top),
        "file_info": {
            "name": img.filename
        }
    }
