# TrashRecogntion

This was a cloud computing server I developed for a capstone project on trash sorting IOT trashcan. The trashcan takes a photo of the object and sends the image via REST protocol to this cloud computing server. It would then respond with the predicted trash category (Trash, Recycling, Compost) to the trashcan, and use that result to dump the trash onto one of the three bins assigned to a category.

SmartSort_App contains my implementation of the trash sorting cloud compute server run inside an Amazon EC2 instance and a docker container.

SmartSort_ModelTraining contains my implementation of image classification training. I experimented with various deep learning architectures and chose the one that gave the best results (ResNet).
The dataset used: https://www.kaggle.com/datasets/asdasdasasdas/garbage-classification

Repository for the smart sort trash firmware is on this repo: https://github.com/emilylondon/SmartSortCapstone
![image](https://github.com/Russellkusuma/TrashRecogntion/assets/29903759/9197c747-1a9b-4bf0-821f-21804661cc01)
