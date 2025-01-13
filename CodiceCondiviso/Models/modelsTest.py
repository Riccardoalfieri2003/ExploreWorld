
# Aggiungi la cartella principale al sys.path
import os
import sys
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_path)

from googleScraper.google_scraping_thread import getURLs

from keras.preprocessing.image import load_img, img_to_array
from keras.models import load_model
from io import BytesIO
from PIL import Image
import numpy as np
import requests

#from MareMontagnaCittaModel.MMCgetPredictionClass import MareMontagnaCittaGetClassPrediction
from PeopleModel.PgetPredictionClass import PeopleGetClassPrediction
from TimeModel.TgetClassPrediction import TimeGetClassPrediction
from PhotoOrNotModel.PHgetClassPrediction import PhotoGetClassPrediction
from MareModel.MGetPredictionClass import MareGetClassPrediction
from MontagneModel.MountGetPredictionClass import MountainGetClassPrediction
from CittaModel.CGetPredictionClass import CittaGetClassPrediction




def imageForModel(url):
    # Fetch the image
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful

    # Load the image into Pillow
    image = Image.open(BytesIO(response.content))

    # Convert the image to BytesIO 
    image_bytes = BytesIO() 
    image.save(image_bytes, format=image.format) 
    image_bytes.seek(0) # Move the cursor to the beginning of the file

    # Load the image
    img = load_img(image_bytes, target_size=(244, 244)) # Resize to match model input size

    # Convert the image to a NumPy array
    img_array = img_to_array(img)

    # Expand dimensions to match the model's input shape (batch size, height, width, channels)
    img_array = np.expand_dims(img_array, axis=0)

    # Normalize the pixel values
    img_array = img_array / 255.0

    return img_array



# Ottieni il percorso assoluto della directory del progetto
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Percorsi assoluti per i modelli
people_model_path = os.path.join(project_path, 'Models', 'PeopleModel', 'PeopleModel_quantized.tflite')
time_model_path = os.path.join(project_path, 'Models', 'TimeModel', 'TimeModel_quantized.tflite')
photo_model_path = os.path.join(project_path, 'Models', 'PhotoOrNotModel', 'PhotoModel_quantized.tflite')
mare_model_path = os.path.join(project_path, 'Models', 'MareModel', 'MareModel_quantized.tflite')
montagna_model_path = os.path.join(project_path, 'Models', 'MontagneModel', 'MontagneModel_quantized.tflite')
citta_model_path = os.path.join(project_path, 'Models', 'CittaModel', 'CittaModel_quantized.tflite')

# Caricamento dei modelli
PeopleModel = load_model(people_model_path)
TimeModel = load_model(time_model_path)
PhotoModel = load_model(photo_model_path)
MareModel = load_model(mare_model_path)
MontagnaModel = load_model(montagna_model_path)
CittaModel = load_model(citta_model_path)



result_list, coordinate, luogo=getURLs("Okinawa","Specifico")
print(coordinate)
print(luogo)
#result_list=['https://lh5.googleusercontent.com/p/AF1QipMvf8JeWrZ32tP9cmq4YLP5HqWFILz0IhX7b55o=w2030-h1450-k-no', 'https://lh5.googleusercontent.com/p/AF1QipNIyt5lI-Pbe5--w57CgE4PkE5dhADTxDwc5d9H=w2030-h1140-k-no', 'https://lh5.googleusercontent.com/p/AF1QipOV2l0hWEaKTLyOFT0qBia1go8aXVtjTf0vdebI=w2030-h1510-k-no', 'https://lh5.googleusercontent.com/p/AF1QipN2jK6VleioAtCMoHepxcXXPqUpVWl6L0ZwZOdq=w2030-h1370-k-no', 'https://lh5.googleusercontent.com/p/AF1QipPZslM2yPP0VzeLCzozRWPryXaa5od3aJgkAP4L=w2030-h1520-k-no', 'https://lh5.googleusercontent.com/p/AF1QipOHg4z2XhJY5m-n7ybz7Gi15ztgkgyzrbZEVP6b=w2030-h1140-k-no', 'https://lh5.googleusercontent.com/p/AF1QipOrqLNWcBh4rcJ7MOd26lvHKbLa45_BtzQrQ6RN=w2030-h1140-k-no', 'https://lh5.googleusercontent.com/p/AF1QipOp48n1dwTG9D3bdfklWXGCZ16SbpVqXnTLs6xV=w2030-h1350-k-no', 'https://lh5.googleusercontent.com/p/AF1QipNiXaH7pGJ8J9bRopMAkUZzIg7GDfQ74xDyO2we=w2030-h1140-k-no', 'https://lh5.googleusercontent.com/p/AF1QipNTCpLqRJe7wb7NICEBdE6m43cROIR-M5vFmOtN=w2030-h1140-k-no', 'https://lh5.googleusercontent.com/p/AF1QipM0OBYBV4MEFGZ4g2CCwQjPoxA-WhT9i-xuMi-F=w2030-h990-k-no', 'https://lh5.googleusercontent.com/p/AF1QipP9xMO-ZQamO9enIep_1F1b6CI444AKRDaEw9sm=w2030-h1520-k-no', 'https://lh5.googleusercontent.com/p/AF1QipP1yg2tB3hJUzCWPD673pMUoCIr7xm1ODsgvo9-=w2030-h1140-k-no', 'https://www.viaggi-usa.it/wp-content/uploads/2017/05/Big-Island-Hawaii-cosa-vedere.jpg', 'https://thegetaway.mblycdn.com/uploads/tg/2022/01/GettyImages-938335974.jpg', 'https://bossfrog.com/wp-content/uploads/2017/09/Big-Island-Map.jpg', 'https://www.twowanderingsoles.com/wp-content/uploads/2023/05/IMG_2878.jpg', 'https://images.exoticestates.com/files/presets/blogimg/sitepage/pages/5e3943b3/1waterfallintoocean.jpg', 'https://afar.brightspotcdn.com/dims4/default/9c32821/2147483647/strip/true/crop/3000x1592+0+354/resize/1440x764!/quality/90/?url=https%3A%2F%2Fk3-prod-afar-media.s3.us-west-2.amazonaws.com%2Fbrightspot%2F6f%2F05%2F575035894e2f8f1330735abf9cd3%2Ftravelguides-hawaii-norbertturi-shutterstock.jpg', 'https://www.viaggi-usa.it/wp-content/uploads/2017/05/Big-Island-Hawaii-cosa-vedere-2.jpg', 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Big_Island_regions_map.png/1200px-Big_Island_regions_map.png', 'https://www.hawaiibeaches.com/wp-content/uploads/sites/3/2022/07/Waipio-Beach-Big-Island-22-2-BDS-5-Large.jpg', 'https://mantarayadvocates.com/wp-content/uploads/2022/03/manta-ray-advocates-visit-e0perience-hawaii-x.jpg', 'https://thewoksoflife.com/wp-content/uploads/2022/08/hawaii-big-island.jpg', 'https://www.steppestravel.com/app/uploads/2019/06/polulu-beach-big-island-hawaii-1024x768.jpg', 'https://media.tacdn.com/media/attractions-splice-spp-674x446/0b/ff/9b/23.jpg', 'https://www.viaggi-usa.it/wp-content/uploads/2017/05/Big-Island-Hawaii.jpg', 'https://guidealong.com/wp-content/uploads/2020/03/Big-Island-11.jpg', 'https://i0.wp.com/atravelingfairy.com/wp-content/uploads/2021/05/IMG_4622.jpg?w=1100&ssl=1', 'https://m.media-amazon.com/images/I/71ui3sUQo5L._AC_UF1000,1000_QL80_.jpg', 'https://lp-cms-production.imgix.net/2023-07/shutterstock1583199166-rfc.jpeg?fit=crop&ar=1%3A1&w=1200&auto=format&q=75', 'https://frankosmaps.com/cdn/shop/products/Big_Island_Adventure_Guide_2015_side_1_53816b17-6cd8-4ff1-be9d-87dd03652a92_2048x.jpg?v=1609703580', 'https://voyagefox.net/wp-content/uploads/2023/04/best-things-to-do-in-big-island-kukio-beach.jpg', 'https://www.hawaii-guide.com/images/jcogs_img/cache/big-island-hawaii-travel-guide-2020-v4_-_abcdef_-_d9b95684d4e0e42ad23a59e9b22c40d7fb13fc1c_-_abcdef_-_1cba40c60493d5a22057e830bcb73760cdc25818.jpg', 'https://c8.alamy.com/compit/2hp6t1a/mappa-stradale-della-piu-grande-isola-hawaiiana-big-island-hawaii-2hp6t1a.jpg', 'https://www.bemytravelmuse.com/wp-content/uploads/2019/12/big-island-hawaii-things-to-do-2.jpg', 'https://images.squarespace-cdn.com/content/v1/5bf1ae37a2772cbd87aefeaf/1542664034425-HYZ6WBGNEJVW0I680711/pololu+valley.jpg?format=2500w', 'https://static.ramblemaps.com/big-island-hawaii-map-1x1-2400.jpg', 'https://media.tacdn.com/media/attractions-splice-spp-674x446/11/63/42/89.jpg', 'https://media.cntraveler.com/photos/53dab67edcd5888e145c750d/master/pass/helicopter-tour-big-island-falls.jpg', 'https://www.gohawaii.jp/sites/default/files/styles/image_gallery_bg_xl/public/hero-unit-images/Hapuna%20Beach%20State%20Park.jpg?itok=vZFkW6ml', 'https://m.media-amazon.com/images/I/61bwNfLW4KL._AC_UF350,350_QL80_.jpg', 'https://www.hawaiitours.com/wp-content/uploads/2020/10/kona-downtown-main-street-and-church-big-island-product-image.jpg', 'https://static1.squarespace.com/static/6226f62738f4f73d2b353e79/6226f784f0c44161f8d9e904/622c4cea7608a939ead49743/1735016621631/DSC04048.jpg?format=1500w', 'https://thehawaiivacationguide.com/wp-content/uploads/2022/10/Best-time-to-visit-the-Big-Island-of-Hawaii-scaled.jpg', 'https://eknb7fhjwcs.exactdn.com/wp-content/uploads/2024/04/seascape.jpg', 'https://i0.wp.com/www.prettyliltraveler.com/wp-content/uploads/2023/11/Discover-Big-Island-Hawaii.jpg?fit=1024%2C577&ssl=1', 'https://hat-storage.imgix.net/2024/06/Beaches-on-the-Big-Island.jpg?auto=compress%2Cformat&ixlib=php-3.3.1&s=6eae36f44a059ea3228c3f102ebf5fa4', 'https://danielshawaii.com/wp-content/uploads/sites/7116/2021/02/kilauea-scaled-1.jpg?w=1000&h=1000', 'https://www.viaggi-usa.it/wp-content/uploads/2017/05/spiagge-big-island-hawaii.jpg', 'https://www.planetware.com/wpimages/2019/11/hawaii-big-island-best-beaches-hapuna-state-beach-aerial.jpg', 'https://saltandwind.com/wp-content/uploads/2023/01/Magic-Sands-Beach-Hawaii-scaled.jpeg', 'https://bigislandguide.com/wp-content/uploads/2017/11/kona-landing@1x.jpg', 'https://images.squarespace-cdn.com/content/v1/61eee5dbbfeabd6491d05edc/1645510192512-K91RWX5XU98RV3INYA21/PXL_20220209_031033222+Copy.jpeg', 'https://bigisland.org/wp-content/uploads/2021/03/naturehawaii.jpg', 'https://www.secondastellaadovest.com/wp-content/uploads/2022/06/BIg-Island-scaled.jpg', 'https://www.hawaiitours.com/wp-content/uploads/2019/01/Lava-and-Ocean-Big-Island-shutterstock_665445211-1200x600-845x600.jpg', 'https://amanda-wanders.com/wp-content/uploads/2022/02/Big-Island-Travel-Tips-Guides-1568x1045.jpg', 'https://www.atacama.it/wp-content/uploads/2020/04/HAWAII-Big-Island-Sheraton-Keauhou-Bay-Resort-aerial.jpg', 'https://www.insiderfamilies.com/wp-content/uploads/2021/05/best-beaches-big-island-hawaii-Depositphotos_37404371_xl-2015.jpg', 'https://www.nuoveali.it/data/foto/768x768/BIG%20ISLAND%2010.jpg', 'https://www.travelworld.it/wp-content/uploads/2019/09/Hawaii-Big-Island-Hawaii-Magazine.jpg', 'https://xdaysiny.com/wp-content/uploads/2020/07/Mahaiula-Beach-Big-Island-Hawaii.jpg', 'https://i0.wp.com/voyageswithval.com/wp-content/uploads/2024/01/Big-Island-of-Hawaii-4-Day-Itinerary.jpg?resize=1024%2C682&ssl=1', 'https://hawaii-forest.com/wp-content/uploads/20190120_ARH-0500-blue-1-1.jpg', 'https://images.squarespace-cdn.com/content/v1/61eee5dbbfeabd6491d05edc/1645576560127-WZRX9332XNQA1QCU0IMR/GPTempDownload.jpeg?format=1000w', 'https://inviaggiodasola.com/wp-content/uploads/2022/06/20220128_143417.jpg', 'https://www.lovebigisland.com/wp-content/uploads/aerial-view-kailua-kona-scaled.jpg', 'https://res.cloudinary.com/hawaiigaga/image/fetch/w_1000,h_644,c_fill,q_auto,f_auto/https://www.hawaiigaga.com/images/attractions/anaehoomalu-bay-s1.jpg', 'https://img.sunset02.com/sites/default/files/image/2016/10/main/big-island-mauna-kea-beach-hotel-sun-1216.jpg', 'https://www.nuoveali.it/data/foto/768x768/COPERTINA%20-%20BIG%20ISLAND%20R1_2.jpg', 'https://images.musement.com/cover/0002/08/island-of-hawaii-view-jpg_header-107997.jpeg', 'https://bigislanddivers.com/wp-content/uploads/2021/02/image-1-288-1024x682.jpg', 'https://i0.wp.com/atravelingfairy.com/wp-content/uploads/2021/05/IMG_4698.jpg?w=1100&ssl=1', 'https://lp-cms-production.imgix.net/2024-07/GettyImages-896972864.jpg?auto=compress&fit=crop&format=auto&q=50&w=1200&h=800', 'https://www.nasa.gov/wp-content/uploads/2023/03/iss063e105782.jpg?w=1041', 'https://www.nps.gov/common/uploads/cropped_image/secondary/7EA6DC31-E9CB-B4DB-AC71341B68C5DD13.jpg?width=640&quality=90&mode=crop', 'https://assets3.thrillist.com/v1/image/2838971/792x529/scale;webp=auto;jpeg_quality=60.jpg', 'https://eknb7fhjwcs.exactdn.com/wp-content/uploads/2020/05/Big-island-itinerary-2.jpg', 'https://goop-img.com/wp-content/uploads/1990/06/hawaii-DSC00946-1.jpg', 'https://pennhenderson.com/wp-content/uploads/2021/03/big-island-hiking-pololu-valley.jpg', 'https://eternalarrival.com/wp-content/uploads/2021/05/rainbow-falls-big-island-hike-shutterstock_1583199226-1.jpg']
#result_list=['https://a.travel-assets.com/findyours-php/viewfinder/images/res70/37000/37477-Kapiolani-Park.jpg']

for url in result_list:
        
    try:

        img=imageForModel(url)

        print(url)

        TimeModelPrediction = TimeGetClassPrediction(TimeModel,img)
        print("TimePrediction: ",TimeModelPrediction)

        PhotoModelPrediction = PhotoGetClassPrediction(PhotoModel,img)
        print("PhotoPrediction: ", PhotoModelPrediction)

        PeopleModelPrediction = PeopleGetClassPrediction(PeopleModel, img)
        print("PeoplePrediction: ",PeopleModelPrediction)

        #MarePrediction,MontagnaPrediction,CittaPrediction=MareMontagnaCittaGetClassPrediction(MareMontagnaCittaModel,img)
        MarePrediction=MareGetClassPrediction(MareModel,img)
        print("MarePrediction: ", MarePrediction)

        MontagnePrediction=MountainGetClassPrediction(MontagnaModel,img)
        print("MontagnaPrediction: ", MontagnePrediction)

        CittaPrediction=CittaGetClassPrediction(CittaModel,img)
        print("CittaPrediction: ", CittaPrediction)
        
        print()

    except Exception as e: 
        print(e)
        pass

