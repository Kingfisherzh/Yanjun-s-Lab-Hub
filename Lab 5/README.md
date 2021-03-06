# Observant Systems


For lab this week, we focus on creating interactive systems that can detect and respond to events or stimuli in the environment of the Pi, like the Boat Detector we mentioned in lecture. 
Your **observant device** could, for example, count items, find objects, recognize an event or continuously monitor a room.

This lab will help you think through the design of observant systems, particularly corner cases that the algorithms need to be aware of.

In Lab 5 part 1, we focus on detecting and sense-making.

In Lab 5 part 2, we'll incorporate interactive responses.


## Prep

1.  Pull the new Github Repo.
2.  Read about [OpenCV](https://opencv.org/about/).
3.  Read Belloti, et al's [Making Sense of Sensing Systems: Five Questions for Designers and Researchers](https://www.cc.gatech.edu/~keith/pubs/chi2002-sensing.pdf)

### For the lab, you will need:

1. Raspberry Pi
1. Raspberry Pi Camera (2.1)
1. Microphone (if you want speech or sound input)
1. Webcam (if you want to be able to locate the camera more flexibly than the Pi Camera)

### Deliverables for this lab are:
1. Show pictures, videos of the "sense-making" algorithms you tried.
1. Show a video of how you embed one of these algorithms into your observant system.
1. Test, characterize your interactive device. Show faults in the detection and how the system handled it.


## Overview
Building upon the paper-airplane metaphor (we're understanding the material of machine learning for design), here are the four sections of the lab activity:

A) [Play](#part-a)

B) [Fold](#part-b)

C) [Flight test](#part-c)

D) [Reflect](#part-d)

---

### Part A
### Play with different sense-making algorithms.

Befor you get started connect the RaspberryPi Camera V2. [The Pi hut has a great explanation on how to do that](https://thepihut.com/blogs/raspberry-pi-tutorials/16021420-how-to-install-use-the-raspberry-pi-camera).  

#### OpenCV
A more traditional to extract information out of images is provided with OpenCV. The RPI image provided to you comes with an optimized installation that can be accessed through python.

Additionally, we also included 4 standard OpenCV examples. These examples include contour(blob) detection, face detection with the ``Haarcascade``, flow detection(a type of keypoint tracking), and standard object detection with the [Yolo](https://pjreddie.com/darknet/yolo/) darknet.

Most examples can be run with a screen (I.e. VNC or ssh -X or with an HDMI monitor), or with just the terminal. The examples are separated out into different folders. Each folder contains a ```HowToUse.md``` file, which explains how to run the python example.

```shell
pi@ixe00:~/openCV-examples $ tree -l
.
├── contours-detection
│   ├── contours.py
│   └── HowToUse.md
├── data
│   ├── slow_traffic_small.mp4
│   └── test.jpg
├── face-detection
│   ├── face-detection.py
│   ├── faces_detected.jpg
│   ├── haarcascade_eye_tree_eyeglasses.xml
│   ├── haarcascade_eye.xml
│   ├── haarcascade_frontalface_alt.xml
│   ├── haarcascade_frontalface_default.xml
│   └── HowToUse.md
├── flow-detection
│   ├── flow.png
│   ├── HowToUse.md
│   └── optical_flow.py
└── object-detection
    ├── detected_out.jpg
    ├── detect.py
    ├── frozen_inference_graph.pb
    ├── HowToUse.md
    └── ssd_mobilenet_v2_coco_2018_03_29.pbtxt
```
#### Filtering, FFTs, and Time Series data. (beta, optional)
Additional filtering and analysis can be done on the sensors that were provided in the kit. For example, running a Fast Fourier Transform over the IMU data stream could create a simple activity classifier between walking, running, and standing.

Using the set up from the [Lab 3 demo](https://github.com/FAR-Lab/Interactive-Lab-Hub/tree/Spring2021/Lab%203/demo) and the accelerometer, try the following:

**1. Set up threshold detection** Can you identify when a signal goes above certain fixed values?

**2. Set up averaging** Can you average your signal in N-sample blocks? N-sample running average?

**3. Set up peak detection** Can you identify when your signal reaches a peak and then goes down?

Include links to your code here, and put the code for these in your repo--they will come in handy later.

#### Teachable Machines (beta, optional)
Google's [TeachableMachines](https://teachablemachine.withgoogle.com/train) might look very simple.  However, its simplicity is very useful for experimenting with the capabilities of this technology.

You can train a Model on your browser, experiment with its performance, and then port it to the Raspberry Pi to do even its task on the device.

Here is Adafruit's directions on using Raspberry Pi and the Pi camera with Teachable Machines:

1. [Setup](https://learn.adafruit.com/teachable-machine-raspberry-pi-tensorflow-camera/raspberry-pi-setup)
2. Install Tensorflow: Like [this](https://learn.adafruit.com/running-tensorflow-lite-on-the-raspberry-pi-4/tensorflow-lite-2-setup), but use this [pre-built binary](https://github.com/bitsy-ai/tensorflow-arm-bin/) [the file](https://github.com/bitsy-ai/tensorflow-arm-bin/releases/download/v2.4.0/tensorflow-2.4.0-cp37-none-linux_armv7l.whl) for Tensorflow, it will speed things up a lot.
3. [Collect data and train models using the PiCam](https://learn.adafruit.com/teachable-machine-raspberry-pi-tensorflow-camera/training)
4. [Export and run trained models on the Pi](https://learn.adafruit.com/teachable-machine-raspberry-pi-tensorflow-camera/transferring-to-the-pi)

Alternative less steps option is [here](https://github.com/FAR-Lab/TensorflowonThePi).

#### PyTorch  
As a note, the global Python install contains also a PyTorch installation. That can be experimented with as well if you are so inclined.

### Part B
### Construct a simple interaction.

Pick one of the models you have tried, pick a class of objects, and experiment with prototyping an interaction.
This can be as simple as the boat detector earlier.
Try out different interactions outputs and inputs.
**Describe and detail the interaction, as well as your experimentation.**

![image](model.png)
I tried to build a finger-digit-detection model using TeachableMachine. Dataset of digits from 1 to 5 is collected and built, each with 34 pieces of images. All the data use Yanjun's left hand as the reference and are shot with my laptop webcam with white wall as the background. Occulusion or complex background is avoided as much as possible.

Following an open-sesame design in Lab 3, which is audio-based detection of the number information in human voices, this time I plan to design a gesture-based magic box. People need to make the right hand gesture pose as the keyword to open the magic box. 

### Part C
### Test the interaction prototype

The model generally has a good performance when being used to detect the hands similar to the raw data, which are hands being located in the center with blank background.
![image](1.png) ![image](2.png)![image](3.png)![image](4.png)![image](5.png)

Now flight test your interactive prototype and **note your observations**:

1. When does it fail?

The detection result goes bad with complex background and any abnormal hand gestures. It means that if the background includes any other objects or the hand is rotated from its horizontal axis, the estimated result could be wrong.

2. When it fails, why does it fail?

As our dataset is all built with white wall as background, it is not robust against those common complex backgrounds in our daily life. Besides, a relatively dark environment makes it worse.


**Think about someone using the system. Describe how you think this will work.**
1. Are they aware of the uncertainties in the system?
 
Without any provided graphical feedback,  the participants would probably not recognize the uncerntainty that immediately. But as soon as they ensure that their hand gestures are correct but the green LED is not lit up, they would recognize that it was the system's fault.

2. How bad would they be impacted by a miss classification?

As the expected input will be a series of numbers, any miss in the number queue will be very bad as the user has to input from the beginning again.

3. How could change your interactive system to address this?

To avoid such a kind of annoying result, I decided to simplify the system to only detect one-digit input. It means that as far as the user makes a correct gesture, like 1, the green LED will light up.

### Part D
### Characterize your own Observant system

Now that you have experimented with one or more of these sense-making systems **characterize their behavior**.
During the lecture, we mentioned questions to help characterize a material:
* What can you use finger-digit-detection model for?

Finger digit detection could be very useful when dealing with contactless scenarios, especially under this epidemic. Given that not only that oeople wearing masks are hard to be recognized by their phones, but also touching the phone is highly risky, showing the gesture in front of a webcam could be a hygienic metric to replace them. 

* What is a good environment for finger-digit-detection model?

Pure-color background, fewer occlusion, and a bright environment.

* What is a bad environment for finger-digit-detection model?

Complex background, wide-range occlusion and a dark environment.

* When will finger-digit-detection model break?

As the dataset comes from Yanjun's hand, detection results on other people's hands may become poor.

* When it breaks how will finger-digit-detection model break?

It will pop out false negatives, like predicting digit 2 but the label is digit 1.

* What are other properties/behaviors of finger-digit-detection model?

Even though the image will not be shown to the user diretly, its fps is not that high, which may makes the detection worse under dynamic scenarios. 

* How does finger-digit-detection model feel?

It is a simple and tiny design afterall. Every part of PI is set in a small box. With one open side to show the camera and the green LED. 


### Part 2.

Following exploration and reflection from Part 1, finish building your interactive system, and demonstrate it in use with a video.

**Include a short video demonstrating the finished result.**

https://drive.google.com/file/d/1HrbwIlv4cZirZQbvyI2kecmcSXOBVxVk/view?usp=sharing

The detection went poor comparing to the test on laptop webcam. Two reasons could contribute to this. One is the low resolution and low fps. The other is the dark environment.
