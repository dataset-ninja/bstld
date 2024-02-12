The authors present the **BSTLD: Bosch Small Traffic Lights Dataset**, an accurate dataset for vision-based traffic light detection. Vision-only based traffic light detection and tracking is a vital step on the way to fully automated driving in urban environments. The authors hope that this dataset allows for easy testing of objection detection approaches, especially for small objects in larger images.

Note, similar **BSTLD: Bosch Small Traffic Lights Dataset** datasets are also available on the [DatasetNinja.com](https://datasetninja.com/):

- [S2TLD: Small Traffic Light Dataset](https://datasetninja.com/s2tld)

## Motivation

Accurate detection and classification of traffic lights are vital for the success of automated driving in urban settings. Presently, there is a lack of systems capable of reliably perceiving traffic lights in real-time, without relying on map-based information, and from adequate distances necessary for seamless urban driving. While automated driving on highways has garnered considerable research attention, urban environments present a fresh set of challenges demanding more sophisticated algorithms across various domains, including perception, behavioral planning, and collision avoidance systems.

Within the realm of perception, identifying and categorizing traffic signs and lights stands out as a critical task. Traffic lights, in particular, pose a formidable challenge due to their small size and potential confusion with other urban elements such as lamps, decorations, and reflections. Recent advancements in deep neural networks have significantly enhanced various fields of machine learning, particularly computer vision. Deep learning techniques have been successfully employed for tasks such as image classification, end-to-end object detection, pixel-precise object segmentation, and numerous other applications.

<img src="https://github.com/dataset-ninja/bstld/assets/120389559/f8272848-022a-443b-b561-5bb512f77094" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Sample detections of small trafﬁc lights in an image. The top image is taken at the full resolution of 1280 × 720. At the bottom, the enlarged crop shows detected trafﬁc lights of size about 6 × 12 pixels. All lights are correctly classiﬁed as yellow.</span>

## Dataset description

The authors publish the Bosch Small Trafﬁc Lights Dataset, an accurately labeled dataset for detecting, classifying, and tracking trafﬁc lights. Dataset contains RGB color images at the resolution of 1280 × 720 pixels. For training, the authors collected more than 5000 images, mainly along El Camino Real in the San Francisco Bay Area in California. Overall, 10,756 trafﬁc lights are labeled within those images. The different trafﬁc light sizes within the training set vary between approximately 1 and 85 pixels in width with the mean of 11.3 pixels.

|         | Width | Height | Area   |
|---------|-------|--------|--------|
| Minimum | 1.12  | 0.25   | 0.28   |
| Average | 11.18 | 24.32  | 404.52 |
| Median  | 8.55  | 18.93  | 158.8  |
| Maximum | 98.0  | 207.0  | 20286.0|

<span style="font-size: smaller; font-style: italic;">Training set bounding box sizes in pixels.</span>

The label distribution of the different trafﬁc light states is heavily skewed towards the three most common types which are *green*, *red*, and *yellow*. Also, because of the difference between the sampling frequency of our camera and the trafﬁc light refresh rate, a lot of trafﬁc lights frequently appear to be *off*. Whenever this is the case, the authors opted for labeling them as off instead of their current state.

|                  | Training | In %  | Test | In %  |
|------------------|----------|-------|------|-------|
| Red              | 3057     | 28.42 | 5321 | 39.44 |
| Red Straight     | 9        | 0.08  | 0    | 0     |
| Red Straight Left| 1        | 0.01  | 0    | 0     |
| Red Left         | 1092     | 10.15 | 0    | 0     |
| Red Right        | 5        | 0.05  | 0    | 0     |
| Yellow           | 444      | 4.13  | 154  | 0.01  |
| Green            | 5207     | 48.41 | 7569 | 56.10 |
| Green Straight   | 20       | 0.19  | 0    | 0     |
| Green Straight Left| 1      | 0.01  | 0    | 0     |
| Green Straight Right| 3     | 0.03  | 0    | 0     |
| Green Left       | 178      | 1.65  | 0    | 0     |
| Green Right      | 13       | 0.12  | 0    | 0     |
| Off              | 726      | 6.75  | 449  | 0.03  |

<span style="font-size: smaller; font-style: italic;">Label distribution over the training and test set.</span>

For testing, the authors collected a stereo video sequence with odometry along University Avenue in Palo Alto, California. In contrast to the training images, those images are taken and labeled consecutively at a frequency of 15.6 frames per second. Since the bounding boxes are labeled consecutively, it is possible to evaluate a tracker on them. In total, the test set comprises 8,334 labeled image files, encompassing 13,493 traffic lights. Notably, 2,094 of these lights are labeled despite being obscured by various objects. Remarkably, our test set exclusively includes labels for traffic lights in "off," "green," "red," and "yellow" states. Table III offers a comprehensive breakdown of the diverse sizes of traffic lights within our test set. This dataset is intended to serve as a rigorous benchmark for the detection of traffic lights, or more broadly, small objects within images. Additionally, the authors present our findings as a baseline using this dataset.

|         | Width  | Height | Area    |
|---------|--------|--------|---------|
| Minimum | 1.875  | 3.250  | 11.718  |
| Average | 9.430  | 26.745 | 313.349 |
| Median  | 8.500  | 24.500 | 212.109 |
| Maximum | 48.375 | 104.500| 4734.000|

<span style="font-size: smaller; font-style: italic;">Test set trafﬁc light bounding box sizes in pixels.</span>

Identifying objects within images presents significant challenges, particularly when aiming for consistent performance in real-time across a spectrum of object sizes. In the case of traffic lights, achieving real-time detection with minimal false negatives and false positives is imperative. A high false negative rate can result in missed traffic lights, an outcome deemed unacceptable for autonomous vehicles. Conversely, false positive detections can induce erratic behavior in automated vehicles, such as halting for non-existent red traffic lights.

The YOLO architecture has demonstrated impressive performance on datasets like PASCAL VOC 2007 and 2012, achieving processing speeds of up to 45 frames per second. However, a grid-based approach to detection presents limitations, particularly in suggesting bounding boxes per cell. Authors have noted difficulties in detecting small objects and clusters of objects. Additionally, there's a challenge in balancing image input sizes, processing speed, and memory usage. Given that the average width of traffic lights in our datasets is only 10 pixels, adjustments are necessary to enable the network to detect small objects effectively. To address this, the authors have implemented a multi-step approach. Instead of feeding the entire image into the network, they partition the image into different patches and evaluate each patch separately. During training, random crops of the image are utilized as inputs to the network, leading to improved convergence speed and accuracy. For the final detection phase, they focus on three specific crops in the upper part of the image, as this is where most traffic lights are typically located. The authors have also developed a heatmap to visualize the occurrences of traffic lights. Each network has a receptive field of 448 × 448 pixels, allowing for comprehensive analysis of the image data.

<img src="https://github.com/dataset-ninja/bstld/assets/120389559/fbad9b91-2d29-4d44-94b1-f9fc8f6bca3c" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Sample image from test-set. The authors network is evaluated at the positions within the image, shown in red, teal, and yellow. Two green trafﬁc lights are detected, one by a cell of the yellow network, the other by red.</span>