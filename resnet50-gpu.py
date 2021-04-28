import os
import sys
import tensorflow as tf
import pandas as pd

num = 7

# ref https://github.com/tensorflow/tensorflow/issues/6698
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  try:
    # Currently, memory growth needs to be the same across GPUs
    for gpu in gpus:
      tf.config.experimental.set_memory_growth(gpu, True)
    logical_gpus = tf.config.experimental.list_logical_devices('GPU')
    print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
  except RuntimeError as e:
    # Memory growth must be set before GPUs have been initialized
    print(e)

from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, GlobalAveragePooling2D, BatchNormalization
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing.image import load_img, img_to_array

data_generator = ImageDataGenerator(horizontal_flip=True,
                                   width_shift_range = 0.4,
                                   height_shift_range = 0.4,
                                   zoom_range=0.3,
                                   rotation_range=20,
                                   )

image_size = 224
batch_size = 8
train_generator = data_generator.flow_from_directory(
        'pikuto_data',
        target_size=(image_size, image_size),
        batch_size=batch_size,
        class_mode='categorical')

num_classes = len(train_generator.class_indices)


if not sys.argv[1] == '-d':
        model = tf.keras.models.load_model(sys.argv[1])
        print(f'start tarining with {sys.argv[1]}')
else:
        model = Sequential()

        model.add(ResNet50(include_top=False, pooling='avg', weights="imagenet"))
        model.add(Flatten())
        model.add(BatchNormalization())
        model.add(Dense(2048, activation='relu'))
        model.add(BatchNormalization())
        model.add(Dense(1024, activation='relu'))
        model.add(BatchNormalization())
        model.add(Dense(num_classes, activation='softmax'))

        model.layers[0].trainable = False

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        print('start training default')


count = sum([len(files) for r, d, files in os.walk("pikuto_data")])

history = model.fit_generator(
        train_generator,
        epochs=5)


model.save(f'weights/pikuto_task_v{num}.h5')

# ref https://cocoinit23.com/keras-model-fit-history-pandas-plot/
hist_df = pd.DataFrame(history.history)
hist_df.to_csv(f'history/history_v{num}.csv')

# -d -> without tarined model
# -path -> with trained model
# num = detect model version
