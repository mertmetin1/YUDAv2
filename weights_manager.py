class WeightsManager:
    def __init__(self, initial_weights):
        self.weights = initial_weights

    def update_weight(self, category, weight):
        self.weights[category] = weight

    def remove_weight(self, category):
        self.weights.pop(category, None)
