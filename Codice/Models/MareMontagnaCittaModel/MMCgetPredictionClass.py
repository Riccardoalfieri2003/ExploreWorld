def proportionate(num1, num2, num3):
    numSum=num1+num2+num3
    perc1=num1/numSum
    perc2=num2/numSum
    perc3=num3/numSum
    return perc1,perc2,perc3

def MareMontagnaCittaGetClassPrediction(model, img):
    predictions=model.predict(img)

    predictions[0]=proportionate( predictions[0][0], predictions[0][1], predictions[0][2] )

    predictions[0][0]*=5
    predictions[0][2]/=2

    if predictions[0][0]>0.5: predicted_sea=1
    else: predicted_sea=0

    if predictions[0][1]>0.3: predicted_mountain=1
    else: predicted_mountain=0

    if predictions[0][2]>0.2: predicted_city=1
    else: predicted_city=0


    
    #print(predictions[0])
    """print(predictions[0][0])
    print(predictions[0][1])
    print(predictions[0][2])
    """

    return predicted_sea,predicted_mountain,predicted_city