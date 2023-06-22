'''This Script file aims at finding the image similary/difference scores by given functions and remove 
images with same/similar characteristics from given directory'''

import os
import argparse
import cv2

from multiprocessing import Pool

from imaging_interview import ImageSimilarityDetector

output_file = "report.txt"

with open(output_file, "w") as file:
        file.write("Image\t\t\t\t\t\t\tCompared with\t\t\t\tChange Score\t\tContours\t\t\tStatus\n\n")
        file.close()


##########################################
''' process function 
    1. calculates similarity scores by calling
    the given compare_frames_change_detection
    function
    2. returns the remove/retain info for perticular
    camera id
    '''
##########################################

def process(args, filenames):

    data = []

    directory_path = args.img_dir


    filenames = list(filenames)
    filenames.sort()

    # Initialize the previous image as None
    prev_img = None

    original_image_count = len(filenames)
    removed_image_count  = 0

    file_old = None

    img_sim_det = ImageSimilarityDetector(gaussian_blur_radius_list=args.gauss_blur, min_contour_area = args.min_cont)


    # Iterate through the images in the directory
    for filename in filenames:
        #print("File_name: ", filename)

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

                        line = "%-30s%-30s%-20.1f%-15i%s\n" % (
                            filename, file_old, score, len(contours), "Current Image Retained")
                        data.append(line)

                        prev_img = processed_img
                        file_old = filename

                    elif score==0:

                        os.remove(os.path.join(directory_path,filename))

                        line = "%-30s%-30s%-20.1f%-15i%s\n" % (
                            filename, file_old, score, len(contours), "Current Image removed")
                        data.append(line)
                        
                        removed_image_count = removed_image_count+1

                    else:
                        print("invalid Score!!!")

                        return
                
                else:
                    '''Store the current image as the previous image for the next iteration'''
                    prev_img = processed_img
                    file_old = filename
        
    #rem_img_count = original_image_count-removed_image_count
    removed_percentage = (removed_image_count/original_image_count)*100

    return data, removed_percentage




##########################################
''' main function 
    arrange image lists on the basis of camera id
    and write the data to report.txt'''
##########################################

def main(args):

    directory_path = args.img_dir

    filenames = os.listdir(directory_path)
    #print(filenames)


    camera_id_list = []
    filenames_by_camera = {}

    # Iterate through the filenames and group them by camera ID
    for filename in filenames:
        #camera_id = filename[:3]
        if '_' in filename:
            camera_id = filename.split('_')[0]  # Extract the substring before the first underscore
        elif '-' in filename:
            camera_id = filename.split('-')[0]  # Extract the substring before the first underscore
        if camera_id not in filenames_by_camera:
            filenames_by_camera[camera_id] = []
            camera_id_list.append(camera_id)
        filenames_by_camera[camera_id].append(filename)

    file_name_lists = []

    for i in range (len(camera_id_list)):
        file_name_lists.append(filenames_by_camera[camera_id_list[i]])
    
    '''We can utilize parallel processing for our case where we have  independent lists of images
     but for the sake of simplicity and understanding, loops are preferred ahead '''

    # with Pool() as pool:
    #     args_ = [(args, filenames) for filenames in zip(file_name_lists)]
    #     return_data = pool.starmap(process, args_)

    
    # call the process function for each camera id and store return info to lists
    report_data = []
    removed_image_percentage = []
    for i in range(len(file_name_lists)):
        data, rm_perc  = process(args, file_name_lists[i])
        report_data.append(data)
        removed_image_percentage.append(rm_perc)

    total_rm_perc = 0

    # write data to files 
    with open(output_file, "a") as file:
        for i in range(len(report_data)):
            file.write(''.join(report_data[i]))
            total_rm_perc += removed_image_percentage[i]

        file.write("\n\n\n%.2f percent images removed"%(total_rm_perc/len(removed_image_percentage)))
    file.close()


    print("%.2f percent images removed"%(total_rm_perc/len(removed_image_percentage)))




##########################################
''' Arguments '''
##########################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--img_dir', type=str, required=True,
                        help='Path to directory containing similar images')
    
    parser.add_argument('--min_cont', type=int, default=500,
                        help='minimum contour area for similarity/change detection  --> lower value, more sensitive for detection and vice versa, ')
    
    parser.add_argument('--gauss_blur', nargs='+', type=int, default=None, 
                        help='Gaussian Blur radius list.   --> None means high sensitivity. Setting radius list would blurout image')
    

    args, _ = parser.parse_known_args()

    main(args)

