#!/usr/bin/env python3

from main import app as application, configuration
from models import get_model

if __name__ == "__main__":
    # Load Keras model to memory
    get_model(configuration.app_model)

    application.run()
