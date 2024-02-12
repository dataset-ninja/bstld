The authors present the **BSTLD: Bosch Small Traffic Lights Dataset**, an accurate dataset for vision-based traffic light detection. Vision-only based traffic light detection and tracking is a vital step on the way to fully automated driving in urban environments. The authors hope that this dataset allows for easy testing of objection detection approaches, especially for small objects in larger images.

Note, similar **BSTLD: Bosch Small Traffic Lights Dataset** datasets are also available on the [DatasetNinja.com](https://datasetninja.com/):

- [S2TLD: Small Traffic Light Dataset](https://datasetninja.com/s2tld)

## Motivation

Reliable traffic light detection and classification is crucial for automated driving in urban environments. Currently, there are no systems that can reliably perceive traffic lights in real-time, without map-based information, and in sufficient distances needed for smooth urban driving.

## Dataset description

This dataset contains 13427 camera images at a resolution of 1280x720 pixels and contains about 24000 annotated traffic lights. The annotations include bounding boxes of traffic lights as well as the current state (active light) of each traffic light. The camera images are provided as raw 12 bit HDR images taken with a red-clear-clear-blue filter and as reconstructed 8-bit RGB color images. The RGB images are provided for debugging and can also be used for training. However, the RGB conversion process has some drawbacks. Some of the converted images may contain artifacts and the color distribution may seem unusual. For the test set, every frame was annotated and temporal information was used to improve the label accuracy. The test set was recorded independently from the training set, but within the same region. The dataset was created to prototype traffic light detection approaches, it is not intended to cover all cases and not to be used for production.

The datasets scenes cover a decent variety of road scenes and typical difficulties:
* Busy street scenes inner-city,
* Suburban multilane roads with varying traffic density,
* Dense stop-and-go traffic,
* Road-works,
* Strong changes in illumination/exposure,
* Overcast sky with light rain,
* Flickering/Fluctuating traffic lights,
* Multiple visible traffic lights,
* Image parts that can be confused with traffic lights (e.g. large round tail lights).

<img src="https://github.com/dataset-ninja/bstld/assets/120389559/59fb4436-a0c8-45a6-9e40-50a1736ba9d0" alt="image" width="1000">

<span style="font-size: smaller; font-style: italic;">Example images.</span>