
from network import Network
from layers import Dense, Activation
from activations import *
from losses import *
from plain.datasets import get_mnist_data


x_train, y_train, x_test, y_test, input_size, test_values = get_mnist_data(seed=9876)
network = Network(seed=5678)

network.add(Dense(input_size, 5))
network.add(Activation(square, square_deriv))
network.add(Dense(5, 1))
network.add(Activation(sigmoid, sigmoid_deriv))

network.set_loss(binary_crossentropy, binary_crossentropy_deriv)

for j in range(1000):
    for i in range(13):
        print("Batch ", i)
        start = i*10
        end = 10*(i+1)
        x_enc = x_train[start:end]
        y_enc = y_train[start:end]
        network.fit(x_enc, y_enc, epochs=1, lr=0.1)

correct_preds = 0
preds = 0
for i in range(4):
    print("Test Batch ", i)
    start = i*10
    end = 10*(i+1)
    y = y_test[start:end]
    val = test_values[start:end]
    x_enc = x_test[start:end]
    pred = network.predict(x_test)

    for e in zip(pred.flatten(), y.flatten(), val.flatten()):
        p = np.round(e[0])
        correct = p == e[1]
        if correct:
            correct_preds += 1
        preds += 1
        print(f"{e[2]} is {'even' if p == 0 else 'odd'} ({'GOOD' if correct else 'BAD'}) ({np.round(e[0], 4)})")

print("Correct predictions: {}/{} ({:.2f}%)".format(correct_preds, preds, 100 * correct_preds / preds))
