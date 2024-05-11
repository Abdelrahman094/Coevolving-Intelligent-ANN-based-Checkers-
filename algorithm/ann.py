import numpy as np

class Activation:
    Sigmoid = 0
    Relu = 1

class Layer:
    def __init__(self, input_count, output_count, activation=Activation.Relu):
        self.input_count = input_count
        self.output_count = output_count
        self.weights = np.random.rand(input_count * output_count) * 2 - 1
        self.biases = np.random.rand(output_count) * 2 - 1
        self.activation = activation
        self.size = input_count * output_count + output_count

        if activation == Activation.Sigmoid:
            self.activate = self._activate_sigmoid
        elif activation == Activation.Relu:
            self.activate = self._activate_relu

    def _activate(self, val):
        return val

    def _activate_sigmoid(self, val):
        return 1 / (1 + np.exp(-val))

    def _activate_relu(self, val):
        return np.maximum(0, val)

    def predict(self, inputs):
        result = np.zeros(self.output_count)
        for i in range(self.output_count):
            for j in range(self.input_count):
                result[i] += inputs[j] * self.weights[i * self.input_count + j]
            result[i] += self.biases[i]
        return self.activate(result)

    def get_weights(self):
        return np.concatenate([self.weights, self.biases])

    def get_topology(self):
        return np.array([self.input_count, self.activation, self.output_count])

    def set_weights(self, weights):
        self.weights = weights[:self.weights.size]
        self.biases = weights[self.weights.size:]

class Network:
    def __init__(self, inputs, outputs, layers):
        self.inputs = inputs
        self.outputs = outputs
        self.network = []
        for layer_size in layers:
            if isinstance(layer_size, Layer):
                layer = layer_size
            else:
                layer = Layer(layer_size[0], layer_size[2], layer_size[1])
            self.network.append(layer)

    def predict(self, input):
        return reduce(lambda acc, layer: layer.predict(acc), self.network, input)

    def get_topology(self):
        return np.concatenate([[self.inputs, self.outputs, len(self.network)], *[layer.get_topology() for layer in self.network]])

    def get_weights(self):
        return np.concatenate([layer.get_weights() for layer in self.network])

    def set_weights(self, weights):
        offset = 0
        for layer in self.network:
            layer.set_weights(weights[offset:offset + layer.size])
            offset += layer.size

    def size(self):
        return sum(layer.size for layer in self.network)

    def to_binary(self):
        topology = self.get_topology()
        weights = np.concatenate([topology, self.get_weights()])
        return weights.tobytes()

    @staticmethod
    def from_binary(buffer):
        inputs, outputs, length = buffer[:3]
        layers = [Layer(*buffer[3 + i * 3:6 + i * 3], buffer[3 + i * 3 + 2]) for i in range(length)]
        network = Network(inputs, outputs, layers)
        network.set_weights(buffer[3 + length * 3:])
        return network

# Define reduce function for Network class
def reduce(func, iterable, initializer=None):
    it = iter(iterable)
    if initializer is None:
        value = next(it)
    else:
        value = initializer
    for element in it:
        value = func(value, element)
    return value
Network.reduce = reduce