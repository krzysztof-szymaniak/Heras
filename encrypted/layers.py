"""
Kod prezentuje implementacje warstw gęstej, aktywacyjnej oraz aktywacyjnej o rozszerzonej dziedzinie.
Implementuje szczegóły algorytmu wstecznej propagacji błędu.
"""

import numpy as np

from encrypted.array_utils import encrypt_array, relinearize_array, refresh_array


class Layer:
    def __init__(self):
        self.input = None

    def feed_forward(self, x, HE):
        pass

    def propagate_backward(self, error, lr, HE):
        pass


class Dense(Layer):
    def __repr__(self):
        return f"Dense({self.input_size}, {self.output_size})"

    def __init__(self, input_size, output_size, HE, weights=None, bias=None):
        super().__init__()
        self.input_size = input_size
        self.output_size = output_size
        if weights is not None and bias is not None:
            self.weights = encrypt_array(np.load(weights, allow_pickle=True), HE)
            self.bias = encrypt_array(np.load(bias, allow_pickle=True), HE)
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
        return output

    def propagate_backward(self, output_err, lr, HE):
        print("Updating weights in layer ", self)
        input_err = np.dot(output_err, self.weights.T)
        relinearize_array(input_err, HE)
        weights_err = np.dot(self.input.T, output_err)
        relinearize_array(weights_err, HE)
        self.weights -= weights_err * lr
        self.bias -= output_err * lr
        return input_err


class Activation(Layer):
    def __repr__(self):
        return f"Activation({self.activation.__name__}, {self.activation_deriv.__name__})"

    def __init__(self, activation, activation_deriv):
        super().__init__()
        self.activation = activation
        self.activation_deriv = activation_deriv

    def feed_forward(self, x, HE):
        self.input = refresh_array(x, HE)
        output = self.activation(self.input, HE)
        return output

    def propagate_backward(self, output_err, lr, HE):
        deriv = self.activation_deriv(self.input, HE)
        input_err = deriv * output_err
        input_err = refresh_array(input_err, HE)
        return input_err


class ExtendedActivation(Layer):
    def __init__(self, activation, activation_deriv, coeffs_map, coeffs_map_deriv):
        super().__init__()
        self.coeffs_map = coeffs_map
        self.coeffs_map_deriv = coeffs_map_deriv
        self.activation = activation
        self.activation_deriv = activation_deriv

    def feed_forward(self, x, HE):
        self.input = refresh_array(x, HE)
        output = self.activation(self.input, HE, coeffs_map=self.coeffs_map)
        return output

    def propagate_backward(self, output_err, lr, HE):
        deriv = self.activation_deriv(self.input, HE, coeffs_map=self.coeffs_map_deriv)
        input_err = deriv * output_err
        input_err = refresh_array(input_err, HE)
        return input_err
