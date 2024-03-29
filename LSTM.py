from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.layers import Embedding
from keras.layers import LSTM
from keras.layers import Conv1D, MaxPooling1D
from keras.datasets import imdb

import numpy
import tensorflow as tf
import matplotlib.pyplot as plt

#seed 값 설정
seed = 0
numpy.random.seed(seed)
tf.set_random_seed(seed)

#학습셋과 테스트셋 지정하기
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=5000)

#데이터 전처리
x_train = sequence.pad_sequences(x_train, maxlen = 100)
x_test = sequence.pad_sequences(x_test, maxlen=100)

#모델의 설정

model = Sequential()

model.add(Embedding(5000,100)) #단어를 의미론적 기하공간에 매핑할 수 있도록 벡터화 시킨다.
model.add(Dropout(0.5))
model.add(Conv1D(64, 5, padding='valid', activation='relu', strides=1)) #필터를 이용하여 지역적인 특징을 추출한다.
model.add(MaxPooling1D(pool_size=4)) #입력벡터에서 특정 구간마다 값을 골라 벡터를 구성한 후 반환한다.
model.add(LSTM(55)) #LSTM을 적용
model.add(Dense(1))
model.add(Activation('sigmoid'))
model.summary()

#모델의 컴파일
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

#모델의 실행
history = model.fit(x_train, y_train, batch_size=100, epochs=5, validation_data=(x_test,y_test))

#테스트 정확도 출력
print("\n Test Accuracy: %.4f" % (model.evaluate(x_test, y_test) [1]))


#테스트셋의 오차
y_vloss= history.history['val_loss']

#학습셋의 오차
y_loss = history.history['loss']

#그래프로 표현
x_len=numpy.arange(len(y_loss))
plt.plot(x_len, y_vloss, marker='.', c='red', label='Testset_loss')

plt.plot(x_len, y_loss, marker='.', c='blue', label='Trainset_loss')

#그래프에 그리드를 주고 레이블을 표시
plt.legend(loc='upper right')
plt.grid()
plt.xlabel('epoch')
plt.ylabel('loss')
plt.show()

