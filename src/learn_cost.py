import numpy as np
import sys
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from keras import optimizers, losses, metrics

file_name = sys.argv[1]
is_contain_header = True


def load_csv():
    cnt_total_line_number = 0
    _line_number = 0
    _data = np.zeros([1, 8])
    with open(file_name, 'r') as f:
        for rl in f.readlines():
            cnt_total_line_number += 1
            if is_contain_header and 0 == _line_number:
                _line_number += 1
                # skip header
                continue

            _line_number += 1
            if (_line_number - 1) % 50 == 0:
                print('Loading... %d' % (_line_number - 1))

            cols = [int(x) for x in rl.replace('\n', '').split(',')]

            # verify COST value
            if 0 == cols[0]:
                # if the COST equals ZERO, then skip current line
                continue

            cols[1] = cols[1] / cols[0]
            cols[2] = cols[2] / cols[0]
            cols[3] = cols[3] / cols[0]
            cols[4] = cols[4] / cols[0]
            cols[5] = cols[5] / cols[0]
            cols[6] = cols[6] / cols[0]
            _data = np.vstack((_data, np.array(cols)))

    # cut header
    _data = _data[1:, ]
    # fix data amount
    _line_number = _data.shape[0]
    print('Find {0} valid lines. Total {1} lines.'.format(_line_number, cnt_total_line_number))

    return _data, _line_number


all_data, cnt_line_number = load_csv()
np.random.shuffle(all_data)
x_data = all_data[:, 1:7]
y_data = all_data[:, 7]

train_size = int(cnt_line_number * 0.7)
x_train = x_data[:train_size,]
x_test = x_data[train_size:,]
y_train = y_data[:train_size,]
y_test = y_data[train_size:,]

model = Sequential()
model.add(Dense(16, activation='relu'))
model.add(Dense(1,  activation='sigmoid'))
model.compile(optimizer=optimizers.RMSprop(lr=0.002),
              loss=losses.binary_crossentropy,
              metrics=[metrics.binary_accuracy])

history = model.fit(x_train,
                    y_train,
                    epochs=15,
                    batch_size=15,
                    validation_data=(x_test, y_test))

# print(history.history.keys())

# create a report
loss = history.history['loss']
val_loss = history.history['val_loss']
acc = history.history['binary_accuracy']
val_acc = history.history['val_binary_accuracy']
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
