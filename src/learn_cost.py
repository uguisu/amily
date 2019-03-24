import numpy as np
import sys
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras import optimizers, losses, metrics

file_name = sys.argv[1]
is_contain_header = True
learn_rate = 0.00039
dr_rate_1 = 0.15
dr_rate_2 = 0.1
train_test_rate = 0.7
epoch = 150
batch_size = 15


def clean_data(cols):
    cols[1] = cols[1] / cols[0]
    cols[2] = (cols[2] + cols[1]) / cols[0]
    cols[3] = (cols[3] + cols[2] + cols[1]) / cols[0]
    cols[4] = (cols[4] + cols[3] + cols[2] + cols[1]) / cols[0]
    cols[5] = (cols[5] + cols[4] + cols[3] + cols[2] + cols[1]) / cols[0]
    cols[6] = (cols[6] + cols[5] + cols[4] + cols[3] + cols[2] + cols[1]) / cols[0]
    cols[7] = (cols[7] + cols[6] + cols[5] + cols[4] + cols[3] + cols[2] + cols[1]) / cols[0]

    cols[9] = cols[9] / cols[8]
    cols[10] = cols[10] / cols[8]
    cols[11] = cols[11] / cols[8]
    cols[12] = cols[12] / cols[8]
    cols[13] = cols[13] / cols[8]
    cols[14] = cols[14] / cols[8]
    cols[15] = cols[15] / cols[8]

    return np.array([cols])


def load_csv():
    cnt_total_line_number = 0
    _line_number = 0
    _data = np.zeros([1, 17])
    with open(file_name, 'r') as f:

        for rl in f.readlines():
            # init
            cnt_total_line_number += 1
            is_skip_current_line = False

            if is_contain_header and 0 == _line_number:
                _line_number += 1
                # skip header
                continue

            _line_number += 1
            if (_line_number - 1) % 50 == 0:
                print('Loading... %d' % (_line_number - 1))

            # cover all string value to integer, if the input value is null, cover it to ZERO
            cols = [int('0' if '' == x else x) for x in rl.replace('\n', '').split(',')]

            # verify invalid value
            for i in range(15):
                if 0 == cols[i]:
                    # if the COST equals ZERO, then skip current line
                    is_skip_current_line = True
                    break
            if is_skip_current_line:
                continue

            _data = np.vstack((_data, clean_data(cols)))

    # cut header
    _data = _data[1:, ]
    # fix data amount
    _line_number = _data.shape[0]
    print('Find {0} valid lines. Total {1} lines.'.format(_line_number, cnt_total_line_number))

    return _data, _line_number


def make_network(lr):
    tmp_model = Sequential()
    tmp_model.add(Dense(128, activation='relu'))
    tmp_model.add(Dropout(rate=dr_rate_1))
    tmp_model.add(Dense(64, activation='relu'))
    tmp_model.add(Dropout(rate=dr_rate_2))
    tmp_model.add(Dense(1, activation='sigmoid'))
    # target Mean_squared_error
    tmp_model.compile(optimizer=optimizers.RMSprop(lr=lr),
                      loss=losses.mean_squared_error,
                      metrics=[metrics.binary_accuracy])
    return tmp_model


def show_result(in_history):

    # print(in_history.history.keys())

    loss = in_history.history['loss']
    val_loss = in_history.history['val_loss']
    acc = in_history.history['binary_accuracy']
    val_acc = in_history.history['val_binary_accuracy']
    epochs = range(1, len(loss) + 1)

    plt.figure(num='Game data logistic', figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.plot(epochs, loss, 'bo', label='Training loss')
    plt.plot(epochs, val_loss, 'b', label='Validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.title('Loss')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(epochs, acc, 'bo', label='Training accuracy')
    plt.plot(epochs, val_acc, 'b', label='Validation accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.title('Accuracy')
    plt.legend()

    plt.show()


def get_business_data():
    t1 = clean_data([898,71,39,30,31,21,27,32,10659,6525,5085,4345,3852,3546,3339,3145])
    t1 = np.vstack((t1, clean_data([4134,615,501,496,412,347,306,244,35186,26296,22687,19841,17626,16192,15037,14002])))
    return t1


all_data, cnt_line_number = load_csv()
np.random.shuffle(all_data)
x_data = np.hstack((all_data[:, 1:8], all_data[:, 9:16]))
y_data = all_data[:, 16]

train_size = int(cnt_line_number * train_test_rate)
x_train = x_data[:train_size,]
x_test = x_data[train_size:,]
y_train = y_data[:train_size,]
y_test = y_data[train_size:,]

model = make_network(lr=learn_rate)
history = model.fit(x_train,
                    y_train,
                    epochs=epoch,
                    batch_size=batch_size,
                    validation_data=(x_test, y_test))

show_result(in_history=history)

pre_data = get_business_data()
pre_data = np.hstack((pre_data[:, 1:8], pre_data[:, 9:16]))
pre = model.predict_classes(pre_data)
print(pre[:,0])
