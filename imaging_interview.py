import cv2
import imutils

class ImageSimilarityDetector:
    def __init__(self, gaussian_blur_radius_list=None, black_mask=(5, 10, 5, 0), min_contour_area = 500):
        self.gaussian_blur_radius_list = gaussian_blur_radius_list
        self.black_mask = black_mask
        self.min_contour_area = min_contour_area

    def draw_color_mask(self, img, borders, color=(0, 0, 0)):
        h = img.shape[0]
        w = img.shape[1]

        x_min = int(borders[0] * w / 100)
        x_max = w - int(borders[2] * w / 100)
        y_min = int(borders[1] * h / 100)
        y_max = h - int(borders[3] * h / 100)

        img = cv2.rectangle(img, (0, 0), (x_min, h), color, -1)
        img = cv2.rectangle(img, (0, 0), (w, y_min), color, -1)
        img = cv2.rectangle(img, (x_max, 0), (w, h), color, -1)
        img = cv2.rectangle(img, (0, y_max), (w, h), color, -1)

        return img

    def preprocess_image_change_detection(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if self.gaussian_blur_radius_list is not None:
            for radius in self.gaussian_blur_radius_list:
                gray = cv2.GaussianBlur(gray, (radius, radius), 0)

        gray = self.draw_color_mask(gray, self.black_mask)
        cv2.imshow("gray: ", gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return gray

    def compare_frames_change_detection(self, prev_frame, next_frame):

        frame_delta = cv2.absdiff(prev_frame, next_frame)
        thresh = cv2.threshold(frame_delta, 45, 255, cv2.THRESH_BINARY)[1]

        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        score = 0
        res_cnts = []
        for c in cnts:
            if cv2.contourArea(c) < self.min_contour_area:
                continue

            res_cnts.append(c)
            score += cv2.contourArea(c)

        return score, res_cnts, thresh


