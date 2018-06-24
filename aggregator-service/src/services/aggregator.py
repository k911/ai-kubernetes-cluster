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


def make_score(model, score, weight):
    return dict(model=model, score=score, weight=weight)


def map_predictions(results: list, weights: dict) -> dict:
    predictions = dict()
    for result in results:
        for prediction in result["predictions"]:
            label = prediction["class_description"]
            model = result["used_model"]
            score = make_score(model, float(prediction["score"]), weights[model])

            if label in predictions:
                predictions[label].append(score)
            else:
                predictions[label] = [score]

    return predictions


def make_result(label, score, scores) -> dict:
    return dict(label=label, score=score, scores=scores)


def parse_float(f: float) -> str:
    return "%.3f" % f


def parse_scores(scores: list) -> list:
    return [make_score(score["model"], parse_float(score["score"]), parse_float(score["weight"])) for score in
            scores]


def parse_predictions(predictions: list, top: int) -> list:
    return [make_result(prediction["label"], parse_float(prediction["score"]), parse_scores(prediction["scores"]))
            for prediction in predictions][:top]


def count_scores(predictions: iter) -> list:
    results = []
    for label, scores in predictions:
        score = 0.
        for partial in scores:
            score = score + partial["score"] * partial["weight"]

        results.append(make_result(label, score, scores))
    return results


def make_file(data, img):
    return img.filename, io.BytesIO(data), img.mimetype


def aggregate(img, top: int, weights: dict):
    top = int(top or 5)
    img_data = img.read()
    img.close()

    models = weights.keys()
    max_workers = len(models)
    if max_workers > 10:
        max_workers = 10

    session = FuturesSession(max_workers=max_workers)
    responses = [ask_for_predictions(session, make_file(img_data, img), service, top) for service in models]
    results = parse_responses(responses)
    mapped_predictions = map_predictions(results, weights)
    predictions = count_scores(mapped_predictions.items())
    predictions = sorted(predictions, key=lambda k: k['score'], reverse=True)

    return {
        "predictions": parse_predictions(predictions, top),
        "file_info": {
            "name": img.filename
        }
    }
