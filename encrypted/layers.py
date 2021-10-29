import numpy as np

from array_utils import encrypt_array, relinearize_array, refresh_array

BUDGET = 300


class Layer:
    def __init__(self):
        self.input = None
        self.output = None

    def feed_forward(self, x, HE):
        raise NotImplementedError

    def propagate_backward(self, error, lr, HE):
        raise NotImplementedError


class Dense(Layer):
    def __init__(self, input_size, output_size, HE, weights=None, bias=None):
        super().__init__()
        if weights is not None and bias is not None:
            self.weights = encrypt_array(np.load(weights), HE)
            self.bias = encrypt_array(np.load(bias), HE)
        else:
            random_weights = np.random.rand(input_size, output_size) - 0.5
            random_bias = np.random.rand(1, output_size) - 0.5
            self.weights = encrypt_array(random_weights, HE)
            self.bias = encrypt_array(random_bias, HE)

    def feed_forward(self, x, HE):
        self.input = x
        output = np.dot(self.input, self.weights)
        relinearize_array(output, HE)
        output += self.bias

        if output[0, 0].noiseBudget < BUDGET:
            output = refresh_array(output, HE)
        return output

    def propagate_backward(self, output_err, lr, HE):
        input_err = np.dot(output_err, self.weights.T)
        relinearize_array(input_err, HE)
        weights_err = np.dot(self.input.T, output_err)
        relinearize_array(weights_err, HE)
        self.weights -= weights_err * lr
        self.bias -= output_err * lr

        if self.weights[0, 0].noiseBudget < BUDGET:
            self.weights = refresh_array(self.weights, HE)
        if self.bias[0, 0].noiseBudget < BUDGET:
            self.bias = refresh_array(self.bias, HE)
        if input_err[0, 0].noiseBudget < BUDGET:
            input_err = refresh_array(input_err, HE)

        return input_err


class Activation(Layer):
    def __init__(self, activation, activation_deriv):
        super().__init__()
        self.activation = activation
        self.activation_deriv = activation_deriv

    def feed_forward(self, x, HE):
        self.input = x
        output = self.activation(self.input, HE)
        if output[0, 0].noiseBudget < BUDGET:
            output = refresh_array(output, HE)
        return output

    def propagate_backward(self, output_err, lr, HE):
        input_err = self.activation_deriv(self.input, HE) * output_err
        relinearize_array(input_err, HE)
        if input_err[0, 0].noiseBudget < BUDGET:
            input_err = refresh_array(input_err, HE)
        return input_err