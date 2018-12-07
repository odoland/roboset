# roboset

This is just a little robot to play set! It was just a project for me to learn about basic image processing, and computer vision.
I made my own algorithms for the color and fill detection (reinventing the wheel a bit)
The first version was before I learned of machine learning algorithms - so all the parameters for each of features
and cut off points were determined manually ( trial and error)

Currently refactoring some of the stuff with ML.
naive bayes for color detection
(WIP) card object detection - because there's an issue with Window's Selenium taking the card images


## Video Demo:
[video demo](https://www.youtube.com/watch?v=6uBgwcrD5Z4)

## Libraries used:

1. image processing/computer vision with **openCV**, 
2. automation and crawling with **Selenium**, 
3. arrays, computation with **numpy**
4. plotting and data with **matplotlib** and **scipy**

---

## Game

[Explanation of the card game: Set](https://puzzles.setgame.com/set/rules_set.html)
Every card has four categories, each category has exactly three states:

A) Color : Red, Green or Purple
B) Count : One, Two, Three
C) Shape : Diamond, Oval, Squiggle
D) Fill  : Hollow, Striped, Fill

A 'Set' consists of three cards, that for each category is eitehr all the same or all different for each card.
For example, for color - they would have to be either ALL the same (all red) or each different (red, green, purple)

## Theory

The idea was to extract all four features from the images to determine what the card was and then pipe it to my own set detecting algorithm.

--
### Detecting Color
Color detection was the easiest! 
Because there are only three different colors - I needed only to find the specific range of the BGR values for red purple and green!

In this case, I just needed to analyze the pictures: openCV has the format in B-G-R
```
purpb = np.array ([80, 0, 80]), np.array([160,60,160])
greenb = np.array([0,100,0]), np.array([45,180,45])
redb = np.array([0,0,160]), np.array([30,30,255])
```
Then I just had to filter the image for all pixels that fell in this range, and the maximum counts that arises is the most likely color.

**Update: 2018/11/02**
Currently working on detecting the color in an imperfect image (real life photograph). 
**Update: 2018/11/15**
see color.py -> Naive Bayes classifier, using ratio of red, green, and purple pixels (from filtering through HSV) as the feature vector.

### Detecting Shape and Count
To approximate the shape, I found all the contours (just a shape that joins all the points together as a continuos line)
It's based on those pixels with the similar color/intensity which we can use for shape and object detection
[contours](https://docs.opencv.org/3.4.3/d4/d73/tutorial_py_contours_begin.html)

For better accuracy, I converted the image to binary image by setting a threshold for what will become white or black. 
With the contours, I could use cv2's approx polyDP algorithm with the approx Perimeter of the contours to 'approximate' the sides of the polygon. It works well for the diamond shape (4 sides) but picks up multiple sides for the oval and squiggle.

### Detecting Fill
My thought was for a comptuer to "see" the stripes, was the go down the image in the y direction.
In a way, we would be taking a 'derivative' or more accurately, the rate of change (discrete)
I would measure the rate of change (indicating a white to black as a positive slope, and black to white as negative).
Because I didn't want to deal with negative slopes, I just removed the sign by squaring and then squarerooting it.
To avoid picking up noise, I just used the max height of the peak (which is very likely a real change) and made sure that we only looked for peaks that were at least 1/3rd the length of the max peak (1/3)

Here are the example pictures with matplotlib:
**Hollow**

Hollows start white, instantly change to a color, and then back down to emptiness again and stays constant. 
Then once it hits the other side, you can see it spikes back up to solid briefly and then back to white.
In total this should be 4 peaks:

<p align="center">
  <img src="https://github.com/odoland/roboset/blob/master/examples/hollow.png">
</p>

**Solid**
Similarily, for solids, you can see only two peaks: Once from transition to white to solid color - then stays constant (0 slope or rate of change)
<p align="center">
  <img src="https://github.com/odoland/roboset/blob/master/examples/solid.png">
</p>

**Striped**
Striped would have a constant swap back and forth, as seen here:
<p align="center">
  <img src="https://github.com/odoland/roboset/blob/master/examples/striped_peaks.png">
</p>

## Implementation

[Selenium](https://www.seleniumhq.org/)
Navigating to the website and taking screenshots of each card was done with Selenium. 
It allows the robot to interact with the website - allowing it to locate the region of the buttons through the page source  and clicking them.
For selenium, we enter the website, then take a screenshot of the cards, crop pictures by position of the buttons.
Planning to replace this with object detection.

[openCV](https://opencv.org/)
- Sobel derivatives & filtered for peaks of 1/3rd (manually decided parameter) + pixel density for  fill / color.
- [The Sobel operator](https://en.wikipedia.org/wiki/Sobel_operator) is a kernel that is convolved on each pixel. Normally, it is done both in the X and Y , and you could check the gradient direction, and used in edge detection.
I just needed the Sobel operator kernel to approximate the 'derivative'. Then I just reduced the entire thing by projecting it  into a 1D array - leaving 'white pixels' as 0, so that they don't have any contribution.

-For striped images, contour finding was tricky - each stripe was picked up as a new shape.
To fix this, I just blurred the image (also with an erosion and dilation) to smother the stripes.
-For hollow images, there were also other complications because the outline was so thin. 
To fix this, I used a floodfill on the corner and then inverted the image - effectively turning any hollow images into solid forms.
This way all images are pushed into 'solid' images for more accurate shape detection.


** Set Finding Algorithm **

We could store each attribute element as an integer (0, 1, 2). A set occurs when all elements are either unique, or in triplets.
Because of that, we can exploit the average of the three, of a 'set' will be an integer value. Or in other words, would be evenly divisible by three.

Another thing to note is that for any two cards, the third is pre-determined. Because there is only one number possible that can make a number evenly divisible by 3 - which is the 'complement'.
Because the third card is predetermined by the first two, this becomes a problem of just searching for the existence of that specific card generated from two cards - which reduces the time complexity from O(n^3) (finding combinations of three) into just finding combinations of two O(n^2) with the use of a HashMap for O(1) access.

Computation of the third member is done as a simple computation O(1).

**Future Features**

2018/11/05
Working on adapting the vision into working on real images - with various tints, glares obstructions!
SVM/naive bayes classifier for fitting/predicting for each attribute (thinking SVM or naive bayes)
Simple CNN for object (card) detection to avoid screenshot error
