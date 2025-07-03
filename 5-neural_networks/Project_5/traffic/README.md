Initial experiment (get_model_1)
- 2 units of {conv, maxpool}
- 3 fc layers 128 -> 100 -> 43
test accuracy: 0.9094

experiment 2 (get_model_2):
Changes: 
- larger model, more conv layers, more channels
- 3 units of {conv, batchnormalization, maxpooling2d, and dropout}
- more neurons in fc layers (256 -> 128 -> 43)
- 50% dropout after every fc layer
test accuracy = 0.9900

experiment 3 (get_model_2):
Changes
- same architecture as before but w/ more epochs (15 instead of 10)
test accuracy: 0.9916

experiment 4 (get_model_3):
- same architecture as model2 but removed dropout and batch normalization. 15 epochs
test accuracy: 0.9860

experiment 5 (get_model_2):
Changes
- back to model2 w/ regularization techniques
- same architecture as get_model_2 as before but w/ more epochs (30 instead of 15)
test accuracy: accuracy: 0.9938


General Takeways:

Model complexity and regularization techniques were the biggest factors in improving performance. 
- Simple models w/o enough convolutional layers/capacity didn't perform as well => increasing the depth and number of filters, channels, and neurons allowed the network to learn more abstract features and perform better
- Batch normalization and dropout helped to prevent overfitting as the model grew larger and trained longer. Without batch norm or dropout the model overfitted (experiment 4). With batch norm + dropout, the model could train for much longer and still not overfit
- Longer training times consistently improved accuracy, especially when combined with these regularization methods. Diminishin returns => small improvements in accuracy for large time/processing power spent (e.g. training for twice as long and only get 0.002 improvement in accuracy)