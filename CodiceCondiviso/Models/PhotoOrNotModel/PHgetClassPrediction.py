import numpy as np

def proportionate(num1, num2, num3, num4):
    numSum=num1+num2+num3
    perc1=num1/numSum
    perc2=num2/numSum
    perc3=num3/numSum
    perc4=num4/numSum
    return perc1,perc2,perc3,perc4

def PhotoGetClassPrediction(model,img):
    predictions=model.predict(img)

    """
    predictions[0]=proportionate( predictions[0][0], predictions[0][1], predictions[0][2], predictions[0][3] )


    predicted_class = np.argmax(predictions[0])

    #print(predictions)

    #SOLO SE è PER FOTO VERE
    if predicted_class==1 and predictions[0][0]*5>=predictions[0][1]: predicted_class=0
    else: predicted_class = np.argmax(predictions[0])
    """
    if predictions[0]> 0.6: predicted_class=1
    else: predicted_class=0

    return predicted_class