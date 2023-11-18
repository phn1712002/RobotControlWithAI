import os, threading
import netron
import keyboard
import keras_core as keras
import tensorflow as tf

# Control robot and convolutional neural network
class RLCRACNN(keras.Model):
    def __init__(self, 
                 shape_image:tuple=(224, 224, 3), 
                 shape_parameters:tuple=(7,), 
                 number_action:int=361,
                 *args, **kwargs):
            """
            Initialize the Model class.

            Args:
                shape_image (tuple): The dimensions of the input image. Default is (224, 224, 3) - Represents the size of the image.
                shape_parameters (tuple): The dimensions of the input parameters. Default is (7,) - Consists of three angle values for all robot links and four points defining a rectangle.
                number_action (int): The total number of possible actions. Default is 361 - Each link can control the direction angle within the range [-180, 180].
                args: Variable-length argument list.
                kwargs: Arbitrary keyword arguments.

            """
            super().__init__(*args, **kwargs)
            
            # ! Input
            self.input_image = keras.layers.Input(shape=shape_image, name='image')
            self.input_parameter = keras.Input(shape=shape_parameters, name='parameter')
            
            # ! Branch parameter
            self.fc_1 = keras.layers.Dense(units=16 ,activation='relu')
            self.fc_2 = keras.layers.Dense(units=32, activation='relu')

        
            # ! Branch image
            self.cnn_1 = keras.layers.Conv2D(filters=16, kernel_size=(3,3), padding='same', activation='relu')
            self.cnn_2_1 = keras.layers.Conv2D(filters=16, kernel_size=(3,3), padding='same', activation='relu')
            self.max_pool_1 = keras.layers.MaxPool2D(pool_size=(2,2), strides=(2,2))
            
            
            self.cnn_2 = keras.layers.Conv2D(filters=32, kernel_size=(3,3), padding='same', activation='relu')
            self.cnn_2_2 = keras.layers.Conv2D(filters=32, kernel_size=(3,3), padding='same', activation='relu')
            self.max_pool_2 = keras.layers.MaxPool2D(pool_size=(2,2), strides=(2,2))
            
            self.cnn_3 = keras.layers.Conv2D(filters=64, kernel_size=(3,3), padding='same', activation='relu')
            self.cnn_2_3 = keras.layers.Conv2D(filters=64, kernel_size=(3,3), padding='same', activation='relu')
            self.max_pool_3 = keras.layers.MaxPool2D(pool_size=(2,2), strides=(2,2))
            
            self.flatten = keras.layers.Flatten()
            
            # ! Branch general
            self.concat = keras.layers.Concatenate(axis=1)
            self.fc_general_1 = keras.layers.Dense(units=4096, activation='relu')
            self.fc_general_2 = keras.layers.Dense(units=4096, activation='relu')
            self.q_output = keras.layers.Dense(units=number_action)
            
            
            # ! Build model
            self.__build()
            
            # ! Var view model
            self.PATH_NAME_VIEW_MODEL = self.name + '_view_model.keras'
        
    def __build(self):
        x = self.input_parameter, self.input_image
        self.model = keras.Model(inputs=x, outputs=self.call(x))
        
    def call(self, inputs, training=False):
         
        # ! Input
        input_parameters, input_image = inputs

        # ! Branch parameter 
        x1 = self.fc_1(input_parameters)
        x1 = self.fc_2(x1)
        
        # ! Branch image
        x2 = self.cnn_1(input_image)
        x2 = self.cnn_2_1(x2)
        x2 = self.max_pool_1(x2)
        
        x2 = self.cnn_2(x2)
        x2 = self.cnn_2_2(x2)
        x2 = self.max_pool_2(x2)
        
        x2 = self.cnn_3(x2)
        x2 = self.cnn_2_3(x2)
        x2 = self.max_pool_3(x2)
        
        x2 = self.flatten(x2)
        
        # ! Branch general
        x = self.concat([x1, x2])
        x = self.fc_general_1(x)
        x = self.fc_general_2(x)

        # ! Output softmax 
        y = self.q_output(x)
        
        return y

    def view_model(self, port=1712):
        """View the model architecture using Netron.

        Args:
            port (int, optional): The port number to run Netron on. Defaults to 1712.
        """
        # ! Save model
        self.model.save(self.PATH_NAME_VIEW_MODEL)
        
        # ! Start netron
        netron_thread = threading.Thread(target=netron.start, args=(self.PATH_NAME_VIEW_MODEL, port))
        netron_thread.start()
        
        # ! Wait for esc key press
        print("Press the 'ESC' key to stop NETRON.")
        keyboard.wait('esc')

        # ! Stop netron
        os.remove(self.PATH_NAME_VIEW_MODEL)
        netron.stop(port)
        
    def plot_model(self, *args, **kwargs):
        """Converts a Keras model to dot format and save to a file.
        Args:
            to_file: File name of the plot image.
            show_shapes: whether to display shape information.
            show_dtype: whether to display layer dtypes.
            show_layer_names: whether to display layer names.
            rankdir: `rankdir` argument passed to PyDot,
                a string specifying the format of the plot: `"TB"`
                creates a vertical plot; `"LR"` creates a horizontal plot.
            expand_nested: whether to expand nested Functional models
                into clusters.
            dpi: Image resolution in dots per inch.
            show_layer_activations: Display layer activations (only for layers that
                have an `activation` property).
            show_trainable: whether to display if a layer is trainable.

        Returns:
            A Jupyter notebook Image object if Jupyter is installed.
            This enables in-line display of the model plots in notebooks.
        """
        keras.utils.plot_model(self.model, *args, **kwargs)