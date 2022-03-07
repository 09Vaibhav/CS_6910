# CS_6910
solution 1: copy_of_assignment_1_1 contains the code that will give the sample image for each class as given in the question 1 . For getting the mnist dataset , we use the command "from keras.datasets import fashion_mnist".

solution 2: First, a class named neural network is created having parameters train_X, train_Y,inp_dim,size_of_hidden_layer,hidden_layers,output_dim,batch_size,epochs,activation_func,learning_rate, decay_rate,beta,beta1,beta2,optimizer,weigh_init. secondly, an object is created for the above class where we passed the training datas (train_X, train_Y,inp_dim,size_of_hidden_layer,hidden_layers,output_dim,batch_size,epochs,activation_func,learning_rate, decay_rate,beta,beta1,beta2,optimizer,weigh_init) here in activation_func , we choose which activation function , we want to pass and in optimizer , we select the optimizer function . also the weight initializer is selected by us . As per the need, we use gradient descent as our optimizer function and sigmoid , tanh, ReLU as our activation function . the parameters like batch size , learning rate, epochs can be choosen any value while creating the object of the above class.

solution 3: AS per the question , we implement different optimiser function and use appropriate abbreviations for them in our python code.

solution 4: in this , we use sweep function to plot different parameter in wandb . however, we divided the datas into training datas and cross validation datas . abd hence after implementing the sweep function , the plot we can see in wandb panel.

solution 7: A confusion matrix problem is there , we first use the test data to plot the matrix . The model having highest validation accuracy is used for plotting confusion matrix . The model is as follows: optimizer : nadam activation : tanh batch size : 64 hidden layers : 2 learning rate : 0.002 weight decay : 0.1

solution 8: As per the question , here we compared square loss and cross entropy loss by running 4 configurations .

solution 10: we load the  mnist images from keras data set and run those to get the test accuracy.
