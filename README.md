# colorBlindTransform
colorBlindTransform

Color Blind Transform Project

Description:
This project aims to create a tool that will ingest an image and transform it so that it appears clear to a color-blind person. Specifically, this tool will start by giving users an assessment that will evaluate what kinds of color blindness they have, so that the application only transforms colors that users have trouble seeing. After the evaluation, the application will generate a scale on which it will transform the colors of images, and then apply that scale to an image to change the color.


As someone who is colorblind, I have experienced some of the troubles, although small, and a tool like this would be interesting to implement. I think an actual implementation could be a collaboration with a company like Meta on their Orion glasses, which have a built-in screen and camera pointing outwards. The built-in screen could transform colors specific to users and their relative view of colors so that they could see colors the same way as people who are not color blind.  

Run Instructions:
This project is written in Python and uses the CMU Graphics library, the Pillow library, and the numpy library. 
Assuming you have Python installed properly you should be able to run pip install pillow in the terminal to download the Pillow library and pip install numpy to download the numpy library. The best way to get CMU Graphics is by going to the website on the next line, and following the instructions to download the package and add it to the same folder as the source code.
https://academy.cs.cmu.edu/desktop

Please also note you must have the "test2.png" image in the same folder as the source code as well since it is a graphics used in the code.

When you feed in a file path for the program to transform, if you have a file in the same folder as the source code, you can just use its name, but if not, you may need to copy the entire path. 

Shortcut Commands
There are no shortcut commands, the code can simply be run once the libraries mentioned above are downloaded and configured properly
