import numpy as np 
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam



train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1./255)

training_set = train_datagen.flow_from_directory(
    'model\\Train_Set_Folder',
    target_size=(48, 48),
    batch_size=64,
    class_mode='categorical')

test_set = test_datagen.flow_from_directory(
    'model\\Test_Set_Folder',
    target_size=(48, 48),
    batch_size=64,
   
    class_mode='categorical')

model = Sequential()

# Update input_shape to (48, 48, 3) to match the RGB images
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48, 48, 3)))
model.add(Conv2D(48, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(30, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer=Adam(learning_rate=0.0001), metrics=['accuracy'])




model.fit(
        x=training_set,
        steps_per_epoch=19638 // 64,
        epochs=15,
        validation_data=test_set,
        validation_steps=7879 // 64)

# save model structure in jason file
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)

# save trained model weight in .h5 file
model.save('model.h5')
