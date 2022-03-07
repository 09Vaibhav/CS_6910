# -*- coding: utf-8 -*-
"""Copy of assignment_1_2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1h3SbCLQCIDnDoig6LV9R-zr4Nf0Qe1gZ
"""

from keras.datasets import fashion_mnist
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

(train_X,train_Y),(x_test,y_test)=fashion_mnist.load_data()
train_X = train_X/255
x_test = x_test/255




class neural_network:
    np.random.seed(10)
    def __init__(self,train_X,train_Y,inp_dim,size_of_hidden_layer,hidden_layers,output_dim,batch_size=30,epochs=10,activation_func="relu"
           ,learning_rate=6e-3 ,decay_rate=0.9,beta=0.9,beta1=0.9,beta2=0.99,optimizer="grad_desc",weight_init="xavier"):

        train_X,self.x_cv,train_Y,self.y_cv = train_test_split(train_X, train_Y, test_size=0.10, random_state=100,stratify=train_Y)

        np.random.seed(10)
        self.inp_dim = inp_dim
        self.hidden_layers = hidden_layers
        self.size_of_hidden_layer = size_of_hidden_layer
        self.output_dim = output_dim

        self.batch = batch_size
        self.epochs = epochs
        self.activation_func = activation_func
        self.learning_rate = learning_rate
        self.decay_rate = decay_rate
        self.optimizer = optimizer
        self.weight_init = weight_init
        self.beta = beta
        self.beta1 = beta1
        self.beta2 = beta2


        self.layers = [self.inp_dim] + self.hidden_layers*[self.size_of_hidden_layer] + [self.output_dim]

        layers = self.layers.copy()
        self.weighs = []
        self.biases = []
        self.activations = []
        self.activation_grads = []
        self.weighs_grads = []
        self.biases_grads = []

        for i in range(len(layers)-1):
            if self.weight_init == 'xavier':
                std = np.sqrt(2/(layers[i]*layers[i+1]))
                self.weighs.append(np.random.normal(0,std,(layers[i],layers[i+1])))
                self.biases.append(np.random.normal(0,std,(layers[i+1])))
            else:
                self.weighs.append(np.random.normal(0,0.5,(layers[i],layers[i+1])))
                self.biases.append(np.random.normal(0,0.5,(layers[i+1])))
            self.activations.append(np.zeros(layers[i]))
            self.activation_grads.append(np.zeros(layers[i+1]))
            self.weighs_grads.append(np.zeros((layers[i],layers[i+1])))
            self.biases_grads.append(np.zeros(layers[i+1]))

        self.activations.append(np.zeros(layers[-1]))
        
        self.grad_desc(train_X,train_Y)


    def sigmoid(self,activations):
        res = []
        for z in activations:
            if z>40:
                res.append(1.0)
            elif z<-40:
                res.append(0.0)
            else:
                res.append(1/(1+np.exp(-z)))
        return np.asarray(res)

    def tanh(self,activations):
        res = []
        for z in activations:
            if z>20:
                res.append(1.0)
            elif z<-20:
                res.append(-1.0)
            else:
                res.append((np.exp(z) - np.exp(-z))/(np.exp(z) + np.exp(-z)))
        return np.asarray(res)

    def relu(self,activations):
        res = []
        for i in activations:
            if i<= 0:
                res.append(0)
            else:
                res.append(i)
        return np.asarray(res)

    def softmax(self,activations):
        tot = 0
        for z in activations:
            tot += np.exp(z)
        return np.asarray([np.exp(z)/tot for z in activations])

    def fwd_propagation(self,x,y,weighs,biases):
        self.activations[0] = x
        n = len(self.layers)
        for i in range(n-2):
            if self.activation_func == "sigmoid":
                self.activations[i+1] = self.sigmoid(np.matmul(weighs[i].T,self.activations[i])+biases[i])
            elif self.activation_func == "tanh":
                self.activations[i+1] = self.tanh(np.matmul(weighs[i].T,self.activations[i])+biases[i])
            elif self.activation_func == "relu":
                self.activations[i+1] = self.relu(np.matmul(weighs[i].T,self.activations[i])+biases[i])

        self.activations[n-1] = self.softmax(np.matmul(weighs[n-2].T,self.activations[n-2])+biases[n-2])        
        return -(np.log2(self.activations[-1][y])) #Return cross entropy loss for single data point.


    def grad_w(self,i):
        return np.matmul(self.activations[i].reshape((-1,1)),self.activation_grads[i].reshape((1,-1)))


    def grad_b(self,i):
        return self.activation_grads[i]


    def bwd_propagation(self,x,y,weighs,biases):
        y_onehot = np.zeros(self.output_dim)
        y_onehot[y] = 1
        n = len(self.layers)

        self.activation_grads[-1] =  -1*(y_onehot - self.activations[-1])
        for i in range(n-2,-1,-1):
            self.weighs_grads[i] += self.grad_w(i)
            self.biases_grads[i] += self.grad_b(i)
            if i!=0:
                value = np.matmul(weighs[i],self.activation_grads[i])
                if self.activation_func == "sigmoid":
                    self.activation_grads[i-1] = value * self.activations[i] * (1-self.activations[i])
                elif self.activation_func == "tanh":
                    self.activation_grads[i-1] = value * (1-np.square(self.activations[i]))
                elif self.activation_func == "relu":
                    res = []
                    for k in self.activations[i]:
                        if k>0: res.append(1.0)
                        else: res.append(0.0)
                    res = np.asarray(res)
                    self.activation_grads[i-1] = value * res

    def grad_desc(self,train_X,train_Y):
        for i in range(self.epochs):
            print('Epoch---',i+1,end=" ")
            loss = 0
            val_loss = 0

            self.weighs_grads = [0*i for i in (self.weighs_grads)]
            self.biases_grads = [0*i for i in (self.biases_grads)]
            
            index = 1
            for x,y in zip(train_X,train_Y):
                x = x.ravel()
                loss += self.fwd_propagation(x,y,self.weighs,self.biases)
                self.bwd_propagation(x,y,self.weighs,self.biases)

                if index % self.batch == 0 or index == train_X.shape[0]:
                    for j in range(len(self.weighs)):
                        self.weighs[j] -= self.learning_rate * self.weighs_grads[j]
                        self.biases[j] -= self.learning_rate * self.biases_grads[j]
                    self.weighs_grads = [0*i for i in (self.weighs_grads)]
                    self.biases_grads = [0*i for i in (self.biases_grads)]
                index += 1 
              
            for x,y in zip(self.x_cv,self.y_cv):
               x=x.ravel()
               val_loss+=self.fwd_propagation(x,y,self.weighs,self.biases)

            acc=round(self.calculate_accuracy(train_X,train_Y),3)
            val_acc=round(self.calculate_accuracy(self.x_cv,self.y_cv),3)
            print('  loss = ',loss/train_X.shape[0],'  accuracy = ',acc,'   validation loss= ',val_loss/self.x_cv.shape[0],'  validation accuaracy= ',val_acc)

    def calculate_accuracy(self,X,Y):
        count = 0
        for i in range(len(X)):
            if self.predict(X[i]) == Y[i]:
                count+=1
        return count/len(X)


    def predict(self,x):
        x = x.ravel()
        self.activations[0] = x
        n = len(self.layers)
        for i in range(n-2):
            if self.activation_func == "sigmoid":
                self.activations[i+1] = self.sigmoid(np.matmul(self.weighs[i].T,self.activations[i])+self.biases[i])
            elif self.activation_func == "tanh":
                self.activations[i+1] = self.tanh(np.matmul(self.weighs[i].T,self.activations[i])+self.biases[i])
            elif self.activation_func == "relu":
                self.activations[i+1] = self.relu(np.matmul(self.weighs[i].T,self.activations[i])+self.biases[i])

        self.activations[n-1] = self.softmax(np.matmul(self.weighs[n-2].T,self.activations[n-2])+self.biases[n-2])

        return np.argmax(self.activations[-1])