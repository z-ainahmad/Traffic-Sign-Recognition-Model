import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 1
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """

    images = []
    labels = []

    #Gets directory of images
    data_dir = os.getcwd() + os.sep + data_dir

    #Iterates through the categories
    for x in range(0, NUM_CATEGORIES):
        #Gets the path of directory for each category
        image_dir = data_dir + os.sep + str(x)

        #Gets list of files in directory
        files = os.listdir(image_dir)

        #Iterates through each image file
        for file in files:
            #Gets path for each image, reads it and resizes it
            file = image_dir + os.sep + file                
            image = cv2.imread(file)
            image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))

            #Image added to list
            images.append(image)
            #Label added to list
            labels.append(x)
        
    return (images, labels)


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """

    #Creates a convolutional neural network
    model = tf.keras.models.Sequential([

        #Convolutional layer
        tf.keras.layers.Conv2D(
            32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
        ),

        #Convolutional layer
        tf.keras.layers.Conv2D(
            32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
        ),

        #Max-pooling layer
        tf.keras.layers.MaxPooling2D(pool_size=(3,3)),

        #Flatten units
        tf.keras.layers.Flatten(),

        #Hidden layer
        tf.keras.layers.Dense(NUM_CATEGORIES * 32, activation="relu"),

        #Hidden layer with dropout
        tf.keras.layers.Dense(NUM_CATEGORIES * 16, activation="relu"),
        tf.keras.layers.Dropout(0.2),

        #Hidden layer
        tf.keras.layers.Dense(NUM_CATEGORIES * 4, activation="relu"),

        #Output layer with output units for all categories
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

    #Model is compiled
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
    
    return model

if __name__ == "__main__":
    main()
