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
[image13]: ./output_images/histogram1.jpg "Histogram 1"
[image14]: ./output_images/histogram2.jpg "Histogram 2"
[image15]: ./output_images/sliding_windows.jpg "Sliding Windows Example"
[image16]: ./output_images/previous_fit.jpg "Previous Fit Example"
[image17]: ./output_images/final_images1.jpg "Final Images 1"
[image18]: ./output_images/final_images2.jpg "Final Images 2"
[image19]: ./output_images/final_images3.jpg "Final Images 3"
[image20]: ./output_images/final_images4.jpg "Final Images 4"

[video1]: ./project_video.mp4 "Video"

The rubric with the specifications for this project can be found [here](https://review.udacity.com/#!/rubrics/571/view)

The code of the project can be found in a Jupyter Notebook [here](P2.ipynb)

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

The next step in the pipeline is to perform a perspective transformation to get a bird's eye view of the road. The code was implemented in the `perspective_transform()` function. The perspective transformation is achieved by using the `cv2.getPerspectiveTransform()` and `cv2.warpPerspective()` functions. The following are examples of the perpective transformation for the given test images:

![alt text][image5]
![alt text][image6]
![alt text][image7]
![alt text][image8]
![alt text][image9]
![alt text][image10]
![alt text][image11]
![alt text][image12]

#### 5. Detection of Lane Lines

To detect the pixels that correspond to the lane lines the histogram is used as as a basis. The peaks in an histogram of the binary image in birds view represent the position of the lanes, as is shown in the following example.

![alt text][image13]

![alt text][image14]

The `find_lanes_sliding_windows()` function implements a slinding windows approach in which the histogram is used in each window to detect the lane lines. The detection of the lane lines is based on a second order polynomial by using the `np.polyfit()` function. The following are the parameters used for the sliding windows approach:

```
# Number of sliding windows
nwindows = 9
    
# Width of the windows +/- margin
margin = 100
    
# Minimum number of pixels found to recenter window
minpix = 50
```

The following image shows an example of lane detection using sliding windows:

![alt text][image15]

As previously mentioned, the `find_lanes_sliding_windows()` function implements the lane lines detection using an sliding window approach. However, once we have the estimation of both lane lines for a given frame, it is possible to exploit the fact that the estimation is similar between consecutive frames in a video. This enables the implementation of a more effecient lane estimation approach, which focuses of a narrow area around the lane lines detected in previous frames to avoid performing the sliding window approach for every frame from scratch. The `find_lanes_previous_fit()` function implements the lane line detection using previous polynomial estimations. As example of this is shown in the following image:

![alt text][image16]

#### 6. Lane Curvature and Offset

The curvature of the lane is compute in the `calc_lane_curvature()` function. Here the lane radius is computed using the bird's view of the lane.

The vehicle position with respect to center is computed in the `calc_lane_offset()`. A negative value means that the car has an offset towards the left of the lane, otherwise, in the value is positive that means the offset is towards the right of the lane.

The following is an example of the lane curvature and offset computation:

```
test_images/test6.jpg  | Left curvature =  917.98 m, Right curvature =  859.61 m, Lane offset =  -0.39 m
```
![alt text][image15]

#### 7. Displaying Lane and Information on the Original Image

The function `display_lane_and_info()` shows on top of the original road image the curvature and offset information. In addition, the bird's eye view of the road is shown, along with the binary image and the estimated lane lines. An example of the resultant images is shown in the following sections.

#### 8. Complete Lane Detection Pipeline

The complete lane detection pipeline is implemented in the `lane_detection_pipeline()` function. The steps performed are the following:

1. Correct image distortion
2. Apply color and gradient thresholds
3. Apply perspective transformation to get the bird's eye view
4. Find lane lines either using the sliding window approach, or the faster previous fit approach
5. Verify if the lane estimation is valid by checking the resulting average lane width against the most recent valid value. To detect bad frames by checking the minimum and maximum distance between lines with the average distance of the previous valid frame. The tolerance metric here is +- 20% of the average lane width
6. Draw the lane identification information on top of the original image. If the frame is valid the new estimation is used, orthewise, the previous valid estimation

Note that to the keep track of characteristics of the lane across multiple frames, a class called `class Lane()` is used. 

#### Applying the Lane Detection Pipeline to the Test Images

In the following example, it can be observed the detected lane projected on the original images. In addition, the curvature and offset computations are presented. Finally, the bird's eye view of the lane is shown on the top left of the images.

![alt text][image17]
![alt text][image18]
![alt text][image19]
![alt text][image20]

#### Applying the Lane Detection Pipeline to the Videos

#### 1. Project Video

#### 2. Chanllenge Video


### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](./project_video.mp4)

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

Here I'll talk about the approach I took, what techniques I used, what worked and why, where the pipeline might fail and how I might improve it if I were going to pursue this project further.  
