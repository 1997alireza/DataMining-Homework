import numpy as np
from active_function import *


class DrinksNN:
    # using 2 hidden layers:
        #  input layer: 13 neurons
        #  1st hidden layer: 8 neurons
        #  2nd hidden layer: 5 neurons
        #  output layer: 3 neurons

    def __init__(self, layer_dim=None, h_active_function=tanh, o_active_function=softmax):
        """

        :param h_active_function: hidden layers active function, get input as a number
        :param o_active_function: output layer active function, get input as a numpy array
        """
        if layer_dim is None:
            layer_dim = [13, 8, 5, 3]
        self.layer_dim = layer_dim
        self.h_active_function = h_active_function
        self.o_active_function = o_active_function
        self.w = []
        for i in range(len(self.layer_dim)-1):
            self.w.append(np.random.rand(layer_dim[i], layer_dim[i+1]))
        # self.w1 = np.random.rand(13, 8)
        # self.w2 = np.random.rand(8, 5)
        # self.w3 = np.random.rand(5, 3)

    def train(self, x_batch, y_batch, learning_rate=.7, epoch_num=10000):
        assert type(x_batch) == type(y_batch) == list and len(x_batch) == len(y_batch) > 0 \
               and len(x_batch[0]) == self.layer_dim[0] and len(y_batch[0]) == self.layer_dim[-1], 'invalid input'

        for epoch in range(epoch_num):
            error_sum = 0
            for batch_num in range(len(x_batch)):
                x = x_batch[batch_num]
                y = y_batch[batch_num]

                a, z = self._forward_propagation(x)
                predicted_y = z[-1]
                expected_y = np.array(y)

                delta, error = self._back_propagation(predicted_y, expected_y, a)
                error_sum += error

                # update weights
                for i in range(len(self.layer_dim)-1):
                    for j in range(self.layer_dim[i]):
                        for k in range(self.layer_dim[i+1]):
                            dEdW = z[i][j] * delta[i+1][k]
                            self.w[i][j, k] -= learning_rate * dEdW

            epoch_error = error_sum / len(x_batch[0])
            print('Error on epoch {}: {}'.format(epoch, epoch_error))

    def test(self, x):
        _, z = self._forward_propagation(x)
        return list(z[-1])

    def _forward_propagation(self, x):
        assert type(x) == list and len(x) == self.layer_dim[0], 'invalid input'
        a = [np.array(x)]
        z = [np.array(a[0])]  # input layer has not active function
        for i in range(1, len(self.layer_dim)):
            a.append(np.zeros(self.layer_dim[i]))
            z.append(np.zeros(self.layer_dim[i]))

        for layer_id in range(1, len(self.layer_dim) - 1):  # hidden layers
            for i in range(self.layer_dim[layer_id]):  # iteration on current layer
                for j in range(self.layer_dim[layer_id - 1]):  # iteration on previous layer
                    a[layer_id][i] += z[layer_id - 1][j] * self.w[layer_id - 1][j, i]
                z[layer_id][i] = self.h_active_function(a[layer_id][i])

        # output layer
        for i in range(self.layer_dim[-1]):
            for j in range(self.layer_dim[-2]):
                a[-1][i] += z[-2][j] * self.w[-1][j, i]
            z[-1] = self.o_active_function(a[-1])

        return a, z

    def _back_propagation(self, predicted_y, expected_y, a):
        difference = predicted_y - expected_y
        error = .5 * np.sum(difference * difference)
        delta = []  # delta[i][k] = d Error / d a[i][k]
        for i in range(0, len(self.layer_dim) - 1):
            delta.append(np.zeros(self.layer_dim[i]))

        # Error = .5 * (predicted_y - expected_y)^2
        delta.append((predicted_y - expected_y) * self.o_active_function(a[-1], derived=True))

        for i in range(len(self.layer_dim) - 2, 0, -1):  # no need to calculate delta on input layer (delta[0])
            for j in range(self.layer_dim[i]):
                sig = 0
                for k in range(self.layer_dim[i + 1]):
                    sig += delta[i + 1][k] * self.w[i][j, k]
                delta[i][j] = self.h_active_function(a[i][j]) * sig

        return delta, error


if __name__ == '__main__':
    model = DrinksNN()
    model.train([[1,2,3,4,5,6,7,8,9,10,11,12,13]], [[1,0,0]])
    print(model.test([1,2,3,4,5,6,7,8,9,10,11,12,13]))


