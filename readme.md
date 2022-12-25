# Shadow Writing

This project deals with gesture writing, leveraging the power of OpenCV to create a gesture writing code.

I encourge all the developers to use this code and create their version of gesture writing.


### Functions Decscriptions

-  **getContours**: This fucntion deals with creating area mask around the captured img
-  **findColor**: This function deals with seperating the specific colors from entire video frame
-  **stackImages**: This function deals with stacking of images together irrespective of image dimensions which is a plus over ***numpy*** *horizontal stack and vertical stack*
-  **drawCanvas**: This fuction deals with catpuring the points of my unique object and creating the geometrical shape over the object movement i.e doing shadow writing

#### Prerequisites 
- pip install opencv-python
- pip install numpy


<img src="https://user-images.githubusercontent.com/38580106/209468021-1a288181-b02b-4554-b909-c662ade2c813.jpg" data-canonical-src="https://gyazo.com/eb5c5741b6a9a16c692170a41a49c858.png" width="400" height="400" />
