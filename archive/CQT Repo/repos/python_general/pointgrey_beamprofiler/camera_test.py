import numpy as np
import cv2
import gauss2D_ptgrey as gauss

# cap = cv2.VideoCapture(0)
# ret, frame = cap.read()
# # while(True):
# #     # Capture frame-by-frame
# #     ret, frame = cap.read()
# #
# #     # Display the resulting frame
# cv2.imshow('frame', frame)
# #     if cv2.waitKey(1) & 0xFF == ord('q'):
# #         break
#
# # When everything done, release the capture
# cap.release()
# cv2.destroyAllWindows()


def main():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    b_waist = gauss.Profile()
    b_waist.frame2array(frame)
    b_waist.twoD_Gaussian_fit()
    print('Major width: {0:.2f} um\nMinor width: {1:.2f} um\nAngle: {2:.2f}'.format(
        b_waist.sigma_0, b_waist.sigma_1, b_waist.popt[6]))
    # print(b_waist.sigma_0, b_waist.sigma_1)

if __name__ == '__main__':
    main()