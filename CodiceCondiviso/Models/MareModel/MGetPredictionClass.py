def MareGetClassPrediction(model, img):
    predictions=model.predict(img)

    #print(predictions)

    #if predictions[0]> 0.15: predicted_class=1
    if predictions[0]> 0.5: predicted_class=1
    else: predicted_class=0

    return predicted_class