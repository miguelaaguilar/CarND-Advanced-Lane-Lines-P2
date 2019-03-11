## Advanced Lane Finding Project

### Writeup of Miguel Aguilar
---

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./output_images/chessboard_corners.jpg "Chessboard Corners Example"
[image2]: ./output_images/undistorted_chessboard.jpg "Undistorted Chessboard Example"
[image3]: ./output_images/undistorted_test_image.jpg "Undistorted Test Images"
[image4]: ./output_images/binary_image.jpg "Binary Image"
[image5]: ./output_images/perspective_transform0.jpg "Perspective Transform 0"
[image6]: ./output_images/perspective_transform1.jpg "Perspective Transform 1"
[image7]: ./output_images/perspective_transform2.jpg "Perspective Transform 2"
[image8]: ./output_images/perspective_transform3.jpg "Perspective Transform 3"
[image9]: ./output_images/perspective_transform4.jpg "Perspective Transform 4"
[image10]: ./output_images/perspective_transform5.jpg "Perspective Transform 5"
[image11]: ./output_images/perspective_transform6.jpg "Perspective Transform 6"
[image12]: ./output_images/perspective_transform7.jpg "Perspective Transform 7"

[image2]: ./test_images/test1.jpg "Road Transformed"
[image3]: ./examples/binary_combo_example.jpg "Binary Example"
[image4]: ./examples/warped_straight_lines.jpg "Warp Example"
[image5]: ./examples/color_fit_lines.jpg "Fit Visual"
[image6]: ./examples/example_output.jpg "Output"
[video1]: ./project_video.mp4 "Video"

The rubric with the specifications for this project can be found [here](https://review.udacity.com/#!/rubrics/571/view)

The code of the project can be found [here](P2.ipynb)

---

### Camera Calibration  

The first step of this project before lane detection pipeline is to calibrate the camera to be able to correct image distortion. The process is done once at the beginning. The camera calibration is based on a chessboard image from which is possible to detect its corners. From the previous image we can observe that the number of corner in the x axis is 9, while in the y axis is 6. From this image the corners can be detected using the `cv2.findChessboardCorners()` function as shown in the following image:

![alt text][image1]

Then, using the function  `cv2.findChessboardCorners()` it is possible to extract the `objpoints` and the  `imgpoints`. Using the `objpoints` and the  `imgpoints` is possible to derive the camera calibration and distortion coefficents by using the `cv2.calibrateCamera()`. Finally, using the `cv2.undistort()` function the images can be undistorted, as shown in the following example:

![alt text][image2]


### Advanced Lane Detection Pipeline

In this section each of the stages of the proposed advanced lane detection pipeline is explained.

#### 1. Undistorting a Test Image

The following test images show the camera distortion correction in action:

![alt text][image3]

#### 2. Color and Gradient Thresholding

For an efective lane detection, in this project it was used a combination of color and gradient thresholds (see the `color_gradient_thres()` function). Before extracting this thresholds the brightness of the images is improved by the `increase_brightness()` function.

First of all, a color thresholding is applied to the images to extract only the yellow and white objects. By this is possible to filter out other possible lines and noise on the road. This extraction of colors is key for the challenge video. To extract the yellow and white colors the images are converted to the HSV color space. Once in the HSV color space it was possible to apply thresholds to extract only yellow and white objects. 

Afterward, gradient thresholding was applied, which is a combination of sobel x, direction and magnitude thresholds. The following image shows an example of a resulting binary image after applying the combined color and gradient thresholds:

![alt text][image4]

It is worth mentioning that during the development of this project, the major part of the time was spent tunning the color and gradient thresholds to achieve a satisfactory lane detection.

#### 4. Perspective Transform

The next step in the pipeline is to perform a perspective transformation to get a bird's eye view of the road. This is achieved by using the `cv2.getPerspectiveTransform()` and `cv2.warpPerspective()` functions. The following are examples of the perpective transformation for the given test images:

![alt text][image5]
![alt text][image6]
![alt text][image7]
![alt text][image8]
![alt text][image9]
![alt text][image10]
![alt text][image11]
![alt text][image12]

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The code for my perspective transform includes a function called `warper()`, which appears in lines 1 through 8 in the file `example.py` (output_images/examples/example.py) (or, for example, in the 3rd code cell of the IPython notebook).  The `warper()` function takes as inputs an image (`img`), as well as source (`src`) and destination (`dst`) points.  I chose the hardcode the source and destination points in the following manner:

```python
src = np.float32(
    [[(img_size[0] / 2) - 55, img_size[1] / 2 + 100],
    [((img_size[0] / 6) - 10), img_size[1]],
    [(img_size[0] * 5 / 6) + 60, img_size[1]],
    [(img_size[0] / 2 + 55), img_size[1] / 2 + 100]])
dst = np.float32(
    [[(img_size[0] / 4), 0],
    [(img_size[0] / 4), img_size[1]],
    [(img_size[0] * 3 / 4), img_size[1]],
    [(img_size[0] * 3 / 4), 0]])
```

This resulted in the following source and destination points:

| Source        | Destination   | 
|:-------------:|:-------------:| 
| 585, 460      | 320, 0        | 
| 203, 720      | 320, 720      |
| 1127, 720     | 960, 720      |
| 695, 460      | 960, 0        |

I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto a test image and its warped counterpart to verify that the lines appear parallel in the warped image.

![alt text][image4]

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

Then I did some other stuff and fit my lane lines with a 2nd order polynomial kinda like this:

![alt text][image5]

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

I did this in lines # through # in my code in `my_other_file.py`

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

I implemented this step in lines # through # in my code in `yet_another_file.py` in the function `map_lane()`.  Here is an example of my result on a test image:

![alt text][image6]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](./project_video.mp4)

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

Here I'll talk about the approach I took, what techniques I used, what worked and why, where the pipeline might fail and how I might improve it if I were going to pursue this project further.  
