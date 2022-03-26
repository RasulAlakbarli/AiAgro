import numpy  as np
import pandas as pd 


#Read the data
input_d = pd.read_csv(r"C:\Users\Ilkin\Desktop\Hacktahon\_prepared_input.csv",header=None)
output_d = pd.read_csv(r"C:\Users\Ilkin\Desktop\Hacktahon\_prepared_output.csv",header = None)

input_d = np.array(input_d)
output_d = np.array(output_d)

#Note: Our input to the NN is vectorized form and it trains for entire batch in once for each iter
input_d = input_d.T
output_d = output_d.T

#usages of sklearn lib for data splitting
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(input_d, output_d,test_size=0.05)
#Take back to the acceptable shape
x_train = x_train.T ; x_test = x_test.T ; y_train = y_train.T ; y_test = y_test.T

#Import Neural Network
import NeuralNetwork
#initialization
network = NeuralNetwork.Modifiable_NN([x_train.shape[0],20,20,1],activations={1:'relu',2:'relu',3:'relu',4:'relu'},cost_function='mse',param_init_type='xavier')

#Train the data
network.train(x_train , y_train ,X_test = x_test , Y_test = y_test, lr = 0.0015 , epoch=10000)

# Note that!  : PARAMETERS of NN was SAVED

#Save the x_test for using in predict program such that it'll help us to show the basic working priciple of App
np.savetxt('x_test.csv',x_test,delimiter=',')


