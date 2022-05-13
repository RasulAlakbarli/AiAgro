from email.mime import multipart
from email.policy import default
import numpy as np 
import pickle


class Modifiable_NN(object):
    #initializer 
    def __init__(self,sizes, activations = None , cost_function = 'binary_cross_entropy' ,param_init_type = None):
        self.sizes = sizes
        self.num_layers = len(sizes)
        self.caches = dict() 
        self.cost_function = cost_function
        
        if activations == None:         self.layer_activations = self.default_layer_activations_init(sizes)
        else:                           self.layer_activations = activations
        

        if param_init_type == None:     self.param_init_type = 'default' 
        else:                           self.param_init_type = param_init_type
        self.parameters_initializer()
        
    
    #This function initalize parameter with needed matrix shapes
    #* it refers to multiple_method function which is give us opportunity to initialize parameters with different methods
    def parameters_initializer(self):
        parameters = dict()
        for l in range(1,self.num_layers):
            parameters['W'+str(l)] = np.random.randn(self.sizes[l],self.sizes[l-1])* self.multiple_method(l)
            parameters['b'+str(l)] = np.zeros((self.sizes[l],1))

        self.parameters = parameters
    
    #weight initializer methods
    def multiple_method(self,l):
        if   self.param_init_type == 'default' :   return 10000
        elif self.param_init_type == 'xavier'  :   return np.sqrt(1/self.sizes[l-1])
        elif self.param_init_type == 'he'      :   return np.sqrt(2/self.sizes[l-1])            

    #this function return the dictionary that contain number of layer and activation function for this layer
    def default_layer_activations_init(self,size):
        return {  num_layer:"relu"  if (num_layer < self.num_layers - 1) else 'sigmoid' for num_layer in range(1,self.num_layers) }
    
    #Basically give us the output from network if param A is input
    def feed_forward(self,A):
        for layer_num in range(1,self.num_layers):
            Z = np.dot(self.parameters['W'+str(layer_num)],A) 
            Z = Z + self.parameters['b'+str(layer_num)]
            A = self.activation(Z,self.layer_activations[layer_num])
            ## Add to cache
            self.caches['Z'+str(layer_num)] = Z ; self.caches['A'+str(layer_num)] = A
        return A #output of network | Y_hat
    
    #These are activation functions for NN
    def activation(self,Z,activation):
        if activation == 'relu':
            return np.maximum(0,Z)
        elif activation == 'sigmoid':
            return 1/(1+np.exp(-Z))

    #usable cost functions
    def cost(self,X,Y):
        """param X : Input that will be given to network , Function itself does forward propagation steps and compute cost
           param Y : Wanted output corresponds to given input data. Cost will be computed by This Y and Y_hat which is output of NN for X input"""
        Y_hat = self.feed_forward(X)
        m = Y.shape[1]
        
        if self.cost_function == 'binary_cross_entropy':
            cost = (-1/m)*np.sum( np.multiply(Y,np.log(Y_hat)) + np.multiply( (1-Y) , np.log(1-Y_hat) )) ; cost = np.squeeze(cost)
            return cost
        elif self.cost_function == 'mse':
            cost = (1/m)*np.sum(np.square(Y-Y_hat)) ; cost = np.squeeze(cost) 
            return cost
        else:
            raise Exception('No such cost function yet')
        
    # function basically return Partial derivative of Cost with respect to last activation
    def cost_derivative(self,last_A,Y):
        """Param last_A : Activation of last layer
           Param Y      : Output"""
        if self.cost_function =='binary_cross_entropy':
            return - (np.divide(Y, last_A) - np.divide(1 - Y, 1 - last_A))
        elif self.cost_function == 'mse':
            return ( last_A - Y )

    # This function propagates NN Backward in order to compute derivatives with chain rule for each parameter 
    def backward_prop(self, dA_l, layer_num):
        """param  dA_l : activation derivative of given layer
           param layer_num : layer number """
        dZ = dA_l* self.activation_derivative(self.caches['Z'+str(layer_num)],self.layer_activations[layer_num])
        m = dA_l.shape[1]
        grad_w_l =(1/m)*np.dot(dZ , self.caches['A'+str(layer_num - 1)].T)
        grad_b_l = (1/m)*np.sum(dZ,axis=1, keepdims=True)
        dA_l_prev =  np.dot(self.parameters['W'+str(layer_num)].T,dZ)

        return grad_w_l,grad_b_l,dA_l_prev


    #Derivative of activation function respect to its input Z
    def activation_derivative(self,Z,activation_function):
        if activation_function == 'relu':
            Z[Z<0] = 0; Z[Z>0] = 1 
            return Z
        elif activation_function == 'sigmoid':
            return self.activation(Z,'sigmoid')*(1-self.activation(Z,'sigmoid'))
            #computationally simplified version


    #update the parameters with computed gradients 
    def update_param(self,grad_w,grad_b,layer_num,lr):
        """param  grad_w , grad_b : gradients of parameters
           param layer_num        : layer number 
           param lr               : learning rate """


        # TODO Idea: Make backprop algo reversible so with calculated prev activation derivative make backprop algo goes back,forward and back again 
        layer_num = str(layer_num) # we need string type of layer number so as to concatnate string for calling key of parameters dictionary 
        self.parameters['W'+layer_num] = self.parameters['W'+layer_num] - lr*grad_w
        self.parameters['b'+layer_num] = self.parameters['b'+layer_num] - lr*grad_b
        
    def train(self,X,Y,lr = 0.0001,epoch=1000 , X_test = None , Y_test = None , regularization  = None , dropout = False):
        assert (X.shape[1] == Y.shape[1]) , "Unmatched In out batch size"
        self.caches['A0'] = X
        for iter in range(epoch):
            A_l = self.feed_forward(X)
            dA_l = self.cost_derivative(A_l,Y)
            for layer_num in reversed(range(1,self.num_layers)):
                grad_w,grad_b,dA_l = self.backward_prop(dA_l,layer_num)
                self.update_param(grad_w,grad_b,layer_num, lr = lr)
            if iter% (epoch/10) ==0:
                print('\n COST:::',self.cost(X,Y),end=' ')    
                self.score(X,Y)
                                                                                                                                               
        if X_test is not None:
            self.score(X_test,Y_test)

        #Saving parameters dictionary to file 
        a_file = open("parameters.pkl", "wb")
        pickle.dump(self.parameters, a_file)
        a_file.close()

    
    def decide(self, A_last):
        """This function will decide final prediction based on output and last activation function"""
        last_l_num = list(self.layer_activations)[-1]#layer number of last layer

        if self.layer_activations[last_l_num] == 'sigmoid':
            A_last[A_last<=0.5] = 0 ; A_last[A_last>0.5] = 1
        elif self.layer_activations[last_l_num]  == 'relu':
            pass
        return A_last

    #If test datasets are given, during training we will score NN on train set and once training is completed 
    #It measures score of NN on test set and gives final accuracy
    def score(self,X,Y):
        Y_hat = self.feed_forward(X)
        #just for Relu function
        count =  0
        for i in range(Y.shape[1]):
            if Y[0][i]*0.9<  Y_hat[0][i]  < Y[0][i]*1.1  :
                count+=1
            #so with 10 cm difference predicted data is acceptable
        print( '\n  {} / {} Accuracy : {}% '.format(count,Y.shape[1],count/Y.shape[1]*100))

    def predict(self,X):
        #Reading parameters from file to file 
        param_file = open("parameters.pkl", "rb")
        self.parameters= pickle.load(param_file)
        #computing output
        output = self.feed_forward(X)
        return output

        
        

            



        




    


            






    