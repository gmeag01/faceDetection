from tensorflow.python.keras import layers, metrics, Model

class CNN(Model):
    def __init__(self, input):
        super(CNN, self).__init__()
        self.conv1 = layers.Conv2D(32, (7, 7), activation='relu', padding='same')
        self.pool1 = layers.MaxPooling2D((3, 3), padding='same')

        self.conv2 = layers.Conv2D(64, (5, 5), activation='relu', padding='same')
        self.pool2 = layers.MaxPooling2D((3, 3), padding='same')

        self.conv3 = layers.Conv2D(128, (3, 3), activation='relu', padding='same')
        self.pool3 = layers.MaxPooling2D((2, 2), padding='same')

        self.conv4 = layers.Conv2D(256, (3, 3), activation='relu', padding='same')
        self.pool4 = layers.MaxPooling2D((2, 2), padding='same')
        self.flatten = layers.Flatten()

        self.d1 = layers.Dense(512, activation='relu')
        self.drop1 = layers.Dropout(0.5)
        self.d2 = layers.Dense(1024, activation='relu')
        self.drop2 = layers.Dropout(0.5)
        self.d3 = layers.Dense(4)

    def call(self, x):
        x = self.conv1(x)
        x = self.pool1(x)

        x = self.conv2(x)
        x = self.pool2(x)

        x = self.conv3(x)
        x = self.pool3(x)

        x = self.conv4(x)
        x = self.pool4(x)
        x = self.flatten(x)
        
        x = self.d1(x)
        x = self.drop1(x)
        x = self.d2(x)
        x = self.drop2(x)
        x = self.d3(x)
        return x