
### Questions and Answers

1. **What did you learn after looking at our dataset?**

   Answer: The dataset contains the images of parking lot from the cameras installed at various locations covering the imortant parts of the parking lot.
    The images are taken at different times during the day and the night as well. There are few things that could be improved to lessen the effort of data preprocessing prior to training:
    - Naming convension
        - better to have same time stamp format
        - separation character between camera id and time stamp could be same for uniformity
    - Image resolution not same
    - corrupt images could be avaoided. For example:  "c21_2021_03_27__10_36_36.png" and "c21_2021_03_27__12_53_37.png"
    - Image Quality could be improved usng high resolution cameras (not necessary. case dependent)

2. **How does your program work?**

   Answer: The program consists of two scripts. **imaging_interview.py** and **DetectAndRemoveMain_CameraID.py**
    - imaging_interview.py contains the **ImageSimilarityDetector** class that implements given **change detection algorithm**
    - DetectAndRemoveMain_CameraID.py is the main file that has the following function:
        - main() --> Tasks of this functions
            - Gets the command line args like **input directory path**, **Gaussian Blur Radius List**, **Minimum contour area**
            - Devide all image list into various independent image lists depending upon the camera ID stamp
            - pass each independent image list to process function in a loop for change detection
            - Write information to a text file for each image like change score, comparison with, Contours info, retension or deletion status
        - process() --> Tasks of process function are:
            - Receives the image list for specific camera ID
            - Creates instance for ImageSimilarityDetector class from imaging_interview.py
            - In a loop, read images one by one. Sanity checks if image is not corrupted and check for the image size uniformity. Else resize.
            - process image using given function **preprocess_image_change_detection** from ImageSimilarityDetector class. this function returns gray or blurred greyscale image depending upon your input parameters
            - the processed image, along with previous image, is then passed to another (given) function **compare_frames_change_detection**  from same class that compares both and returns change score, and contours
            - Based on Change Score, removal or retaintion is decided for that current image
            - Keep record of removed images

3. **What values did you decide to use for input parameters and how did you find these values?**

   Answer: We can pass two input parameters to the algorithm.
    - **Gaussian Blur radius List**. Default is none that in my understanding will result in high sensitivity. We can pass single odd value like 3, 5, 7 or list of odd values like [3, 5]. Higher values tend to blurr images more, removing fine dtails, consequently less details perceiveable, hence lower would be the sensitivity.
        - For me, I set it to [3] --> for better sensitivity --> good change perceiveablity and small smooting incase of any noise
        - In some cases, Gaussian blurring may result in **increase of change score** as it may remove **noise** or unnecessary detail.
    - **Minimum_Contour_Area**. if we need higher change score and want our algo to be more sensitive, we can set this value to low i.e 300 or 500. More contours, including small and potentially insignificant ones, will be considered for the change score calculation. The change score may increase because even small changes in the image will contribute to the score. Similarly. higher value leads to less contours, that means lower sensitivity and lower change score.

4. **What would you suggest implementing to improve data collection of unique cases in the future?**

   Answer: Though the given dataset looks good in terms of variation i.e it carries images from different angles of the parking lot. It benifits from different lightning conditions as well. But, we could do the following to improve it further if want to scale the project:
    - Add images of parking lots with different layouts, sizes, and obstacles
    - Add images of cars parked in different positions and orientations, wrongly parked --> at angles, partially occupying multiple parking spaces
    - Include images with crowded parking spaces, narrow parking areas, complex parking structures, or scenarios with obstructed views


5. **Any other comments about your solution?**

   Answer: As we have independent image list depending upon camera IDs, we can do parallel processing for faster computaions. For example using Multiprocessing Package. For the sake of simplicity, these scripts benifits from iterative approach