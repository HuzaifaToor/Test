import os
import argparse
import cv2

from imaging_interview import ImageSimilarityDetector

output_file = "report.txt"


def main(args):

    # Path to the directory containing the images
    directory_path = args.img_dir

    # Initialize the previous image as None
    prev_img = None

    filenames = os.listdir(directory_path)

    original_image_count = len(filenames)
    removed_image_count  = 0

    # Sort the filenames in ascending order
    filenames.sort()
    file_old = None

    img_sim_det = ImageSimilarityDetector(gaussian_blur_radius_list=args.gauss_blur, min_contour_area = args.min_cont)

    with open(output_file, "w") as file:
        file.write("Image\t\t\t\t\t\t\tCompared with\t\t\t\tChange Score\t\tContours\t\t\tStatus\n\n")  # Write the header row
    
        # Iterate through the images in the directory
        for filename in filenames:

            if filename.endswith(".jpg") or filename.endswith(".png"):
                image_path = os.path.join(directory_path, filename)

                
                # Load the image
                img = cv2.imread(image_path)

                if img is not None:

                    # Check if the image size is (640, 480)
                    if img.shape[:2] != (640, 480):
                        img = cv2.resize(img, (640, 480))
                        
                        # Preprocess the image for change detection
                    processed_img = img_sim_det.preprocess_image_change_detection(img)
                    
                    # Compare the current image with the previous image (if available)
                    if prev_img is not None:
                        score, contours, thresh = img_sim_det.compare_frames_change_detection(prev_img, processed_img)

                        if score > 0:
                            # print("image %s compared with %s, change score=%.1f, contours=%i, status: Current Image Retained"
                            #     % (filename, file_old, score, len(contours)))

                            line = "%-30s%-30s%-20.1f%-15i%s\n" % (
                                filename, file_old, score, len(contours), "Current Image Retained")
                            file.write(line)

                            prev_img = processed_img
                            file_old = filename

                        elif score==0:

                            os.remove(os.path.join(directory_path,filename))

                            # print("image %s compared with %s, change score=%.4f, contours=%i, status: Current Image Removed"
                            #     % (filename, file_old, score, len(contours))) 

                            line = "%-30s%-30s%-20.1f%-15i%s\n" % (
                                filename, file_old, score, len(contours), "Current Image removed")
                            file.write(line)
                            
                            removed_image_count = removed_image_count+1

                        else:
                            print("invalid Score!!!")

                            return
                    
                    else:
                        '''Store the current image as the previous image for the next iteration'''
                        prev_img = processed_img
                        file_old = filename
            
        rem_img_count = original_image_count-removed_image_count
        rem_percentage = (removed_image_count/original_image_count)*100

        file.write("\n\nOriginal image count %i remaining image count %i, %.2f percent images removed" % (
                                    original_image_count, rem_img_count, rem_percentage))
        file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--img_dir', type=str, 
    default="/home/cinemo-de.internal/hahmad/Downloads/testDataset/dataset-candidates-ml/tempdataset",
                        help='Path to directory containing similar images')

    # parser.add_argument('--img_dir', type=str, required=True,
    #                     help='Path to directory containing similar images')
    
    parser.add_argument('--min_cont', type=int, default=500,
                        help='minimum contour area for similarity/change detection  --> lower value, more sensitive for detection and vice versa, ')
    
    parser.add_argument('--gauss_blur', nargs='+', type=int, default=None, 
                        help='Gaussian Blur radius list.   --> None means high sensitivity. Setting radius list would blurout image')
    

    args, _ = parser.parse_known_args()

    main(args)