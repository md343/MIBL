# MIBL
Matt's Image-Based Localisation (MIBL) is a Python implementation of a global feature extracting and classifying technique designed for localisation. It uses a NetVLAD CNN to compute image features, and a nearest neighbour search to identify the closest match from an existing dataset of image features.

The local application outputs the localisation information to a window on your machine.

The remote application creates a server, which can take a request input and output the localisation information across a network.

The example application requires the image and result datasets in order to run.

An example output:
![image](https://github.com/md343/MIBL/assets/64204441/564688a2-262b-41d5-acf9-725eed444fbf)

The implementation architecture:
![image](https://github.com/md343/MIBL/assets/64204441/49e46d36-e7c7-46e0-8b77-f1187116ebc6)

