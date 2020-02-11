# QuidEst

## Présentation
Dépôt de projet de **QuidEst**


## Poids de YOLO COCO
Le modèle utilise un modèle YOLO, réalisé par Joseph Chet Redmon, plus d'informations sur son [site](https://pjreddie.com/darknet/yolo/).

Les poids pré-entrainés sont à télécharger et à placer dans le dossier **ODetectionCV/yolo-coco** : [poids](https://pjreddie.com/media/files/yolov3.weights).


## Téléchargement
Un fichier compressé de l'exécutable est disponible au [téléchargement](https://drive.google.com/drive/folders/1LFToXumcK73RxTownUWq57vvJ3irxHTu?usp=sharing). Il suffit de choisir la version voulu.

Actuellement la version la plus récente est : *Version beta*.


## Installation
* Pour créer l'exécutable, il suffit de d'installer le pacquet `pyinstaller`.

  Puis exécuter la commande : `$ pyinstaller QuidEst-beta.spec`

* Pour créer l'installeur, qui est une aide à l'installation, il faut exécuter la commande : `$ pyinstaller pre_QuidEst.spec`

  Il permet seulement de décompresser le dossier après téléchargement, et de créer un raccourci de l'exécutable sur le bureau. Les dossier de l'application seront placé dans le dossier *Documents* de l'ordinateur.


## Crédits
Réalisé par Alexandre Banon.
