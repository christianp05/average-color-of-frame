#include <iostream>
#include <string>
#include <cmath>
#include <opencv2/opencv.hpp>
#include <opencv2/imgproc.hpp>


using namespace std;
using namespace cv;

int main() {

    string name;
    cout << "Whats the movie name ma dude?: ";
    getline(cin, name);
    // Create a VideoCapture object and open the input file
    VideoCapture cap(name);


    if (!cap.isOpened()) {
        cout << "Error opening video stream or file" << endl;
        return -1;
    }

    int totalFrames = cap.get(CAP_PROP_FRAME_COUNT);
    Mat image(10000, totalFrames, CV_8UC3, Scalar(0, 0, 0));
    while (1) {
        int currentFrame = cap.get(CAP_PROP_POS_FRAMES);
        Mat frame;

        // Capture frame-by-frame
        cap >> frame;

        Scalar color = mean(frame);
        if (frame.empty())
            break;
        cout << "frame: " << currentFrame << "/" << totalFrames << "\n";
        Point p1(currentFrame, 0), p2(currentFrame, 10000);
        Scalar colorLine(round(color[0]), round(color[1]), round(color[2]));

        line(image, p1, p2, colorLine, 2);


    }
    imwrite("final.png", image);
    // When everything done, release the video capture object
    cap.release();
    // Closes all the frames
    destroyAllWindows();
    return 0;
}