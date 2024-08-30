# Adyen Terminal printning experiment
This project presents an experiment of how to increase the speed of receipt printouts with Adyen terminals.

In this experiment there are two modes of printing presented:
1. Where n number of QR codes are printed separetly by calling the Adyen Terminal API endpoint n times one by one
2. Where n number of QR codes are first drawn by generating an image, then concatinating all images into one and lastly calling the image printing endpoint using the Terminal API

The second option presents a faster result.
Please keep in mind that the max width for the image should be no more than 384 px. In this experiment the width of 380 px is used.
