///////////////////////////////////////////////////////////////////////////
//
// Copyright (c) 2022, STEREOLABS.
//
// All rights reserved.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
// OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
// LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
// DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//
///////////////////////////////////////////////////////////////////////////

/*****************************************************************************************
 ** This sample demonstrates how to detect human bodies and retrieves their 3D position **
 **         with the ZED SDK and display the result in an OpenGL window.                **
 *****************************************************************************************/
#include <sstream>
#include <iostream>
#include <fstream>
 // ZED includes
#include <sl/Camera.hpp>

// Sample includes
#include "GLViewer.hpp"
#include "TrackingViewer.hpp"
#include "utils.hpp"
#include <opencv2/opencv.hpp>
// Using std and sl namespaces
using namespace std;
using namespace sl;

void print(string msg_prefix, ERROR_CODE err_code = ERROR_CODE::SUCCESS, string msg_suffix = "");
void parseArgs(int argc, char** argv, InitParameters& param);

std::string printBodyParts(BODY_34_PARTS part) {
    std::string out;
    switch (part) {
    case BODY_34_PARTS::PELVIS:
        out = "Pelvis";
        break;
    case BODY_34_PARTS::NAVAL_SPINE:
        out = "Naval_Spine";
        break;
    case BODY_34_PARTS::CHEST_SPINE:
        out = "Chest_Spine";
        break;
    case BODY_34_PARTS::NECK:
        out = "Neck";
        break;
    case BODY_34_PARTS::LEFT_CLAVICLE:
        out = "L_Clavicle";
        break;
    case BODY_34_PARTS::LEFT_SHOULDER:
        out = "L_Shoulder";
        break;
    case BODY_34_PARTS::LEFT_ELBOW:
        out = "L_Elbow";
        break;
    case BODY_34_PARTS::LEFT_WRIST:
        out = "L_Wrist";
        break;
    case BODY_34_PARTS::LEFT_HAND:
        out = "L_Hand";
        break;
    case BODY_34_PARTS::LEFT_HANDTIP:
        out = "L_Handtip";
        break;
    case BODY_34_PARTS::LEFT_THUMB:
        out = "L_Thumb";
        break;
    case BODY_34_PARTS::RIGHT_CLAVICLE:
        out = "R_Clavicle";
        break;
    case BODY_34_PARTS::RIGHT_SHOULDER:
        out = "R_Shoulder";
        break;
    case BODY_34_PARTS::RIGHT_ELBOW:
        out = "R_Elbow";
        break;
    case BODY_34_PARTS::RIGHT_WRIST:
        out = "R_Wrist";
        break;
    case BODY_34_PARTS::RIGHT_HAND:
        out = "R_Hand";
        break;
    case BODY_34_PARTS::RIGHT_HANDTIP:
        out = "R_Handtip";
        break;
    case BODY_34_PARTS::RIGHT_THUMB:
        out = "R_Thumb";
        break;
    case BODY_34_PARTS::LEFT_HIP:
        out = "L_Hip";
        break;
    case BODY_34_PARTS::LEFT_KNEE:
        out = "L_Knee";
        break;
    case BODY_34_PARTS::LEFT_ANKLE:
        out = "L_Ankle";
        break;
    case BODY_34_PARTS::LEFT_FOOT:
        out = "L_Foot";
        break;
    case BODY_34_PARTS::RIGHT_HIP:
        out = "R_Hip";
        break;
    case BODY_34_PARTS::RIGHT_KNEE:
        out = "R_Knee";
        break;
    case BODY_34_PARTS::RIGHT_ANKLE:
        out = "R_Ankle";
        break;
    case BODY_34_PARTS::RIGHT_FOOT:
        out = "R_Foot";
        break;
    case BODY_34_PARTS::HEAD:
        out = "Head";
        break;
    case BODY_34_PARTS::NOSE:
        out = "Nose";
        break;
    case BODY_34_PARTS::LEFT_EYE:
        out = "L_Eye";
        break;
    case BODY_34_PARTS::LEFT_EAR:
        out = "L_Ear";
        break;
    case BODY_34_PARTS::RIGHT_EYE:
        out = "R_Eye";
        break;
    case BODY_34_PARTS::RIGHT_EAR:
        out = "R_Ear";
        break;
    case BODY_34_PARTS::LEFT_HEEL:
        out = "L_Heel";
        break;
    case BODY_34_PARTS::RIGHT_HEEL:
        out = "R_Heel";
        break;
    }
    return out;
}

std::string printBodyParts(BODY_38_PARTS part) {
    std::string out;
    switch (part) {
    case BODY_38_PARTS::PELVIS:
        out = "Pelvis";
        break;
    case BODY_38_PARTS::SPINE_1:
        out = "Spine_1";
        break;
    case BODY_38_PARTS::SPINE_2:
        out = "Spine_2";
        break;
    case BODY_38_PARTS::SPINE_3:
        out = "Spine_3";
        break;
    case BODY_38_PARTS::NECK:
        out = "Neck";
        break;
    case BODY_38_PARTS::NOSE:
        out = "Nose";
        break;
    case BODY_38_PARTS::LEFT_EYE:
        out = "L_Eye";
        break;
    case BODY_38_PARTS::RIGHT_EYE:
        out = "R_Eye";
        break;
    case BODY_38_PARTS::LEFT_EAR:
        out = "L_Ear";
        break;
    case BODY_38_PARTS::RIGHT_EAR:
        out = "R_Ear";
        break;
    case BODY_38_PARTS::LEFT_CLAVICLE:
        out = "L_Clavicle";
        break;
    case BODY_38_PARTS::RIGHT_CLAVICLE:
        out = "R_Clavicle";
        break;
    case BODY_38_PARTS::LEFT_SHOULDER:
        out = "L_Shoulder";
        break;
    case BODY_38_PARTS::RIGHT_SHOULDER:
        out = "R_Shoulder";
        break;
    case BODY_38_PARTS::LEFT_ELBOW:
        out = "L_Elbow";
        break;
    case BODY_38_PARTS::RIGHT_ELBOW:
        out = "R_Elbow";
        break;
    case BODY_38_PARTS::LEFT_WRIST:
        out = "L_Wrist";
        break;
    case BODY_38_PARTS::RIGHT_WRIST:
        out = "R_Wrist";
        break;
    case BODY_38_PARTS::LEFT_HIP:
        out = "L_Hip";
        break;
    case BODY_38_PARTS::RIGHT_HIP:
        out = "R_Hip";
        break;
    case BODY_38_PARTS::LEFT_KNEE:
        out = "L_Knee";
        break;
    case BODY_38_PARTS::RIGHT_KNEE:
        out = "R_Knee";
        break;
    case BODY_38_PARTS::LEFT_ANKLE:
        out = "L_Ankle";
        break;
    case BODY_38_PARTS::RIGHT_ANKLE:
        out = "R_Ankle";
        break;
    case BODY_38_PARTS::LEFT_BIG_TOE:
        out = "L_Big_Toe";
        break;
    case BODY_38_PARTS::RIGHT_BIG_TOE:
        out = "R_Big_Toe";
        break;
    case BODY_38_PARTS::LEFT_SMALL_TOE:
        out = "L_Small_Toe";
        break;
    case BODY_38_PARTS::RIGHT_SMALL_TOE:
        out = "R_Small_Toe";
        break;
    case BODY_38_PARTS::LEFT_HEEL:
        out = "L_Heel";
        break;
    case BODY_38_PARTS::RIGHT_HEEL:
        out = "R_Heel";
        break;
    case BODY_38_PARTS::LEFT_HAND_THUMB_4:
        out = "L_Hand_Thumb_4";
        break;
    case BODY_38_PARTS::RIGHT_HAND_THUMB_4:
        out = "R_Hand_Thumb_4";
        break;
    case BODY_38_PARTS::LEFT_HAND_INDEX_1:
        out = "L_Hand_Index_1";
        break;
    case BODY_38_PARTS::RIGHT_HAND_INDEX_1:
        out = "R_Hand_Index_1";
        break;
    case BODY_38_PARTS::LEFT_HAND_MIDDLE_4:
        out = "L_Hand_Middle_4";
        break;
    case BODY_38_PARTS::RIGHT_HAND_MIDDLE_4:
        out = "R_Hand_Middle_4";
        break;
    case BODY_38_PARTS::LEFT_HAND_PINKY_1:
        out = "L_Hand_Pinky_1";
        break;
    case BODY_38_PARTS::RIGHT_HAND_PINKY_1:
        out = "R_Hand_Pinky_1";
        break;
    }
    return out;
}

/*std::string printBodyParts(BODY_70_PARTS part) {
    std::string out;
    switch (part) {
    case BODY_70_PARTS::PELVIS:
        out = "Pelvis";
        break;
    case BODY_70_PARTS::SPINE_1:
        out = "Spine_1";
        break;
    case BODY_70_PARTS::SPINE_2:
        out = "Spine_2";
        break;
    case BODY_70_PARTS::SPINE_3:
        out = "Spine_3";
        break;
    case BODY_70_PARTS::NECK:
        out = "Neck";
        break;
    case BODY_70_PARTS::NOSE:
        out = "Nose";
        break;
    case BODY_70_PARTS::LEFT_EYE:
        out = "L_Eye";
        break;
    case BODY_70_PARTS::RIGHT_EYE:
        out = "R_Eye";
        break;
    case BODY_70_PARTS::LEFT_EAR:
        out = "L_Ear";
        break;
    case BODY_70_PARTS::RIGHT_EAR:
        out = "R_Ear";
        break;
    case BODY_70_PARTS::LEFT_CLAVICLE:
        out = "L_Clavicle";
        break;
    case BODY_70_PARTS::RIGHT_CLAVICLE:
        out = "R_Clavicle";
        break;
    case BODY_70_PARTS::LEFT_SHOULDER:
        out = "L_Shoulder";
        break;
    case BODY_70_PARTS::RIGHT_SHOULDER:
        out = "R_Shoulder";
        break;
    case BODY_70_PARTS::LEFT_ELBOW:
        out = "L_Elbow";
        break;
    case BODY_70_PARTS::RIGHT_ELBOW:
        out = "R_Elbow";
        break;
    case BODY_70_PARTS::LEFT_WRIST:
        out = "L_Wrist";
        break;
    case BODY_70_PARTS::RIGHT_WRIST:
        out = "R_Wrist";
        break;
    case BODY_70_PARTS::LEFT_HIP:
        out = "L_Hip";
        break;
    case BODY_70_PARTS::RIGHT_HIP:
        out = "R_Hip";
        break;
    case BODY_70_PARTS::LEFT_KNEE:
        out = "L_Knee";
        break;
    case BODY_70_PARTS::RIGHT_KNEE:
        out = "R_Knee";
        break;
    case BODY_70_PARTS::LEFT_ANKLE:
        out = "L_Ankle";
        break;
    case BODY_70_PARTS::RIGHT_ANKLE:
        out = "R_Ankle";
        break;
    case BODY_70_PARTS::LEFT_BIG_TOE:
        out = "L_Big_Toe";
        break;
    case BODY_70_PARTS::RIGHT_BIG_TOE:
        out = "R_Big_Toe";
        break;
    case BODY_70_PARTS::LEFT_SMALL_TOE:
        out = "L_Small_Toe";
        break;
    case BODY_70_PARTS::RIGHT_SMALL_TOE:
        out = "R_Small_Toe";
        break;
    case BODY_70_PARTS::LEFT_HEEL:
        out = "L_Heel";
        break;
    case BODY_70_PARTS::RIGHT_HEEL:
        out = "R_Heel";
        break;
    case BODY_70_PARTS::LEFT_HAND_THUMB_1:
        out = "L_Hand_Thumb_1";
        break;
    case BODY_70_PARTS::LEFT_HAND_THUMB_2:
        out = "L_Hand_Thumb_2";
        break;
    case BODY_70_PARTS::LEFT_HAND_THUMB_3:
        out = "L_Hand_Thumb_3";
        break;
    case BODY_70_PARTS::LEFT_HAND_THUMB_4:
        out = "L_Hand_Thumb_4";
        break;
    case BODY_70_PARTS::LEFT_HAND_INDEX_1:
        out = "L_Hand_Index_1";
        break;
    case BODY_70_PARTS::LEFT_HAND_INDEX_2:
        out = "L_Hand_Index_2";
        break;
    case BODY_70_PARTS::LEFT_HAND_INDEX_3:
        out = "L_Hand_Index_3";
        break;
    case BODY_70_PARTS::LEFT_HAND_INDEX_4:
        out = "L_Hand_Index_4";
        break;
    case BODY_70_PARTS::LEFT_HAND_MIDDLE_1:
        out = "L_Hand_Middle_1";
        break;
    case BODY_70_PARTS::LEFT_HAND_MIDDLE_2:
        out = "L_Hand_Middle_2";
        break;
    case BODY_70_PARTS::LEFT_HAND_MIDDLE_3:
        out = "L_Hand_Middle_3";
        break;
    case BODY_70_PARTS::LEFT_HAND_MIDDLE_4:
        out = "L_Hand_Middle_4";
        break;
    case BODY_70_PARTS::LEFT_HAND_RING_1:
        out = "L_Hand_Ring_1";
        break;
    case BODY_70_PARTS::LEFT_HAND_RING_2:
        out = "L_Hand_Ring_2";
        break;
    case BODY_70_PARTS::LEFT_HAND_RING_3:
        out = "L_Hand_Ring_3";
        break;
    case BODY_70_PARTS::LEFT_HAND_RING_4:
        out = "L_Hand_Ring_4";
        break;
    case BODY_70_PARTS::LEFT_HAND_PINKY_1:
        out = "L_Hand_Pinky_1";
        break;
    case BODY_70_PARTS::LEFT_HAND_PINKY_2:
        out = "L_Hand_Pinky_2";
        break;
    case BODY_70_PARTS::LEFT_HAND_PINKY_3:
        out = "L_Hand_Pinky_3";
        break;
    case BODY_70_PARTS::LEFT_HAND_PINKY_4:
        out = "L_Hand_Pinky_4";
        break;
    case BODY_70_PARTS::RIGHT_HAND_THUMB_1:
        out = "R_Hand_Thumb_1";
        break;
    case BODY_70_PARTS::RIGHT_HAND_THUMB_2:
        out = "R_Hand_Thumb_2";
        break;
    case BODY_70_PARTS::RIGHT_HAND_THUMB_3:
        out = "R_Hand_Thumb_3";
        break;
    case BODY_70_PARTS::RIGHT_HAND_THUMB_4:
        out = "R_Hand_Thumb_4";
        break;
    case BODY_70_PARTS::RIGHT_HAND_INDEX_1:
        out = "R_Hand_Index_1";
        break;
    case BODY_70_PARTS::RIGHT_HAND_INDEX_2:
        out = "R_Hand_Index_2";
        break;
    case BODY_70_PARTS::RIGHT_HAND_INDEX_3:
        out = "R_Hand_Index_3";
        break;
    case BODY_70_PARTS::RIGHT_HAND_INDEX_4:
        out = "R_Hand_Index_4";
        break;
    case BODY_70_PARTS::RIGHT_HAND_MIDDLE_1:
        out = "R_Hand_Middle_1";
        break;
    case BODY_70_PARTS::RIGHT_HAND_MIDDLE_2:
        out = "R_Hand_Middle_2";
        break;
    case BODY_70_PARTS::RIGHT_HAND_MIDDLE_3:
        out = "R_Hand_Middle_3";
        break;
    case BODY_70_PARTS::RIGHT_HAND_MIDDLE_4:
        out = "R_Hand_Middle_4";
        break;
    case BODY_70_PARTS::RIGHT_HAND_RING_1:
        out = "R_Hand_Ring_1";
        break;
    case BODY_70_PARTS::RIGHT_HAND_RING_2:
        out = "R_Hand_Ring_2";
        break;
    case BODY_70_PARTS::RIGHT_HAND_RING_3:
        out = "R_Hand_Ring_3";
        break;
    case BODY_70_PARTS::RIGHT_HAND_RING_4:
        out = "R_Hand_Ring_4";
        break;
    case BODY_70_PARTS::RIGHT_HAND_PINKY_1:
        out = "R_Hand_Pinky_1";
        break;
    case BODY_70_PARTS::RIGHT_HAND_PINKY_2:
        out = "R_Hand_Pinky_2";
        break;
    case BODY_70_PARTS::RIGHT_HAND_PINKY_3:
        out = "R_Hand_Pinky_3";
        break;
    case BODY_70_PARTS::RIGHT_HAND_PINKY_4:
        out = "R_Hand_Pinky_4";
        break;
    }
    return out;
}*/

#define SELECT_RECT 1

#if SELECT_RECT

struct ROIdata {
    // Current ROI, 0: means discard, other value will keep the pixel
    cv::Mat ROI;
    cv::Rect selection_rect;
    cv::Point origin_rect;
    bool selectInProgress = false;
    bool selection = false;

    void reset(bool full = true) {
        selectInProgress = false;
        selection_rect = cv::Rect(0, 0, 0, 0);
        if (full) {
            ROI.setTo(0);
            selection = false;
        }
    }
};

static void onMouse(int event, int x, int y, int, void* data) {
    auto pdata = reinterpret_cast<ROIdata*> (data);
    switch (event) {
    case cv::EVENT_LBUTTONDOWN:
    {
        pdata->origin_rect = cv::Point(x, y);
        pdata->selectInProgress = true;
        break;
    }
    case cv::EVENT_LBUTTONUP:
    {
        pdata->selectInProgress = false;
        // set ROI to valid for the given rectangle
        cv::rectangle(pdata->ROI, pdata->selection_rect, cv::Scalar(250), -1);
        pdata->selection = true;
        break;
    }
    case cv::EVENT_RBUTTONDOWN:
    {
        pdata->reset(false);
        break;
    }
    }

    if (pdata->selectInProgress) {
        pdata->selection_rect.x = MIN(x, pdata->origin_rect.x);
        pdata->selection_rect.y = MIN(y, pdata->origin_rect.y);
        pdata->selection_rect.width = abs(x - pdata->origin_rect.x) + 1;
        pdata->selection_rect.height = abs(y - pdata->origin_rect.y) + 1;
    }
}
#else

struct ROIdata {
    // Current ROI, 0: means discard, other value will keep the pixel
    cv::Mat ROI;
    std::vector<std::vector<cv::Point>> polygons;
    std::vector<cv::Point> current_select;
    bool selection = false;
    bool selectInProgress = false;

    void reset() {
        polygons.clear();
        ROI.setTo(0);
        selection = true;
        selectInProgress = false;
    }
};

static void onMouse(int event, int x, int y, int, void* data) {
    auto pdata = reinterpret_cast<ROIdata*> (data);
    switch (event) {
    case cv::EVENT_LBUTTONDOWN:
        pdata->selectInProgress = true;
        break;
    case cv::EVENT_MOUSEMOVE:
        if (pdata->selectInProgress)
            pdata->current_select.push_back(cv::Point(x, y));
        break;
    case cv::EVENT_LBUTTONUP:
        if (pdata->current_select.size() > 2) {
            pdata->polygons.push_back(pdata->current_select);
            pdata->current_select.clear();
        }
        pdata->selectInProgress = false;
        break;
    case cv::EVENT_RBUTTONDOWN:
        pdata->reset();
        break;
    }
}
#endif

void applyMask(cv::Mat& cvImage, ROIdata& data);

int main(int argc, char** argv) {
    // Create ZED objects
    Camera zed;
    RuntimeParameters runtime_parameters;
    runtime_parameters.enable_fill_mode = false;
    runtime_parameters.remove_saturated_areas = false;

    InitParameters init_parameters;
    init_parameters.input.setFromSVOFile("G:/Mi unidad/Doctorado IA/BaseHandball/jugador4_sec1.svo");
    init_parameters.coordinate_units = UNIT::METER;
    // On Jetson the object detection combined with an heavy depth mode could reduce the frame rate too much
    init_parameters.depth_mode = DEPTH_MODE::NEURAL;
    init_parameters.depth_minimum_distance = 0.3;
    init_parameters.coordinate_system = COORDINATE_SYSTEM::RIGHT_HANDED_Y_UP;
    init_parameters.sdk_verbose = true;

    parseArgs(argc, argv, init_parameters);
    // Open the camera
    auto returned_state = zed.open(init_parameters);
    if (returned_state != ERROR_CODE::SUCCESS) {
        print("Open Camera", returned_state, "\nExit program.");
        zed.close();
        return EXIT_FAILURE;
    }

    // Enable Positional tracking (mandatory for object detection)
    PositionalTrackingParameters positional_tracking_parameters;
    //If the camera is static, uncomment the following line to have better performances and boxes sticked to the ground.
    positional_tracking_parameters.set_as_static = true;
    positional_tracking_parameters.set_floor_as_origin = true;
    positional_tracking_parameters.enable_pose_smoothing = true;

    returned_state = zed.enablePositionalTracking(positional_tracking_parameters);
    if (returned_state != ERROR_CODE::SUCCESS) {
        print("enable Positional Tracking", returned_state, "\nExit program.");
        zed.close();
        return EXIT_FAILURE;
    }

    // Enable the Objects detection module
    BodyTrackingParameters body_tracker_params;
    body_tracker_params.detection_model = BODY_TRACKING_MODEL::HUMAN_BODY_ACCURATE;
    body_tracker_params.body_selection = BODY_KEYPOINTS_SELECTION::FULL;
    body_tracker_params.enable_tracking = false; // track people across images flow, cuando esta en falso la presición de los joints es casi perfecta
    body_tracker_params.enable_body_fitting = true; // smooth skeletons moves
    body_tracker_params.image_sync = true;
    body_tracker_params.enable_segmentation = false;
    body_tracker_params.prediction_timeout_s = 0.0001f; //mejora la precision de los joints cuando esta activado el tracking
    body_tracker_params.body_format = BODY_FORMAT::BODY_38;

    returned_state = zed.enableBodyTracking(body_tracker_params);

    if (returned_state != ERROR_CODE::SUCCESS) {
        print("enable Object Detection", returned_state, "\nExit program.");
        zed.close();
        return EXIT_FAILURE;
    }

    cv::String imWndName = "Image";
    cv::String depthWndName = "Depth";
    cv::String ROIWndName = "ROI";
    cv::namedWindow(imWndName, cv::WINDOW_NORMAL);
    cv::namedWindow(ROIWndName, cv::WINDOW_NORMAL);
    cv::namedWindow(depthWndName, cv::WINDOW_NORMAL);

#if SELECT_RECT
    std::cout << "Draw some rectangles on the left image with a left click\n";
#else
    std::cout << "Draw some shapes on the left image with a left click\n";
#endif
    std::cout << "Press 'a' to apply the ROI\n"
        "Press 'r' to reset the ROI\n"
        "Press 's' to save the ROI as image file to reload it later\n"
        "Press 'l' to load the ROI from an image file" << std::endl;

    auto resolution = zed.getCameraInformation().camera_configuration.resolution;

    auto camera_config = zed.getCameraInformation().camera_configuration;
    // Define OpenCV window size (resize to max 720/404)
    sl::Resolution low_resolution(min(720, (int)resolution.width) * 2, min(404, (int)resolution.height));
    Mat svo_image(low_resolution, MAT_TYPE::U8_C4, MEM::CPU);
    cv::Mat svo_image_ocv = slMat2cvMat(svo_image);
    //Depth image
    Resolution display_resolution(min((int)resolution.width, 2560), min((int)resolution.height, 1440));
    Mat depth(display_resolution, MAT_TYPE::U8_C4);
    cv::Mat depth_image_ocv = slMat2cvMat(depth);
    //Left Image
    cv::Mat image_left_ocv(display_resolution.height, display_resolution.width, CV_8UC4, 1);
    Mat image_left(display_resolution, MAT_TYPE::U8_C4, image_left_ocv.data, image_left_ocv.step);
    sl::float2 img_scale(display_resolution.width / (float)camera_config.resolution.width, display_resolution.height / (float)camera_config.resolution.height);

    Mat zed_image(resolution, MAT_TYPE::U8_C4);
    cv::Mat cvImage(resolution.height, resolution.width, CV_8UC4, zed_image.getPtr<sl::uchar1>(MEM::CPU));
    // Create OpenGL Viewer
    GLViewer viewer;
    viewer.init(argc, argv);

    Pose cam_pose;
    cam_pose.pose_data.setIdentity();

    // Configure object detection runtime parameters
    BodyTrackingRuntimeParameters body_tracker_parameters_rt;
    body_tracker_parameters_rt.detection_confidence_threshold = 40;

    // Create ZED Objects filled in the main loop
    Bodies bodies;

    int svo_frame_rate = zed.getInitParameters().camera_fps;
    int nb_frames = zed.getSVONumberOfFrames();
    print("[Info] SVO contains " + to_string(nb_frames) + " frames");

    ROIdata roi_data;
    roi_data.ROI = cv::Mat(resolution.height, resolution.width, CV_8UC1);
    roi_data.reset();

    // set Mouse Callback to handle User inputs
    cv::setMouseCallback(imWndName, onMouse, &roi_data);

    std::string mask_name = "D:/Pruebas_Captura/Adquisicion/Jugador4Sec1/Mask.png";

    // Start SVO playback
     // Main Loop
    bool quit = false;
    ofstream MyFile("D:/Pruebas_Captura/Adquisicion/Jugador4Sec1/Data.txt");
    int count_1 = 0;
    char key = ' ';
    // Capture new images until 'q' is pressed
    while (key != 'q') {
        returned_state = zed.grab();
        if (returned_state == ERROR_CODE::SUCCESS) {
            // Draw rectangle on the image

            //sl::Mat point_cloud_to_save;
            // Get the side by side image
            // Retrieve Detected Human Bodies
            zed.retrieveBodies(bodies, body_tracker_parameters_rt);
            //zed.retrieveImage(svo_image, VIEW::SIDE_BY_SIDE, MEM::CPU, low_resolution);
            zed.retrieveImage(image_left, VIEW::LEFT, MEM::CPU, display_resolution);
            zed.retrieveImage(zed_image, VIEW::LEFT, MEM::CPU, display_resolution);
            zed.retrieveImage(depth, VIEW::DEPTH, MEM::CPU, display_resolution);
            //zed.retrieveImage(zed_depth_image, VIEW::DEPTH, MEM::CPU, display_resolution);
           // zed.retrieveMeasure(point_cloud_to_save, MEASURE::XYZRGBA);
            zed.getPosition(cam_pose, REFERENCE_FRAME::CAMERA);
            ////Update GL View
           // viewer.updateData(bodies, cam_pose.pose_data);
           // render_2D(image_left_ocv, img_scale, bodies.body_list, bodies.is_tracked);
            // Display the frame
           // cv::imshow("Left", image_left_ocv);
            //cv::imshow("View", svo_image_ocv);
           // cv::imshow("DEPTH", depth_image_ocv);
            //auto write_suceed = point_cloud_to_save.write("Pointcloud.ply");
            //auto timestamp = zed.getTimestamp(sl::TIME_REFERENCE::IMAGE); // Get image timestamp
            //printf("Image timestamp: %llu\n", timestamp);
            // Draw rectangle on the image
            if (roi_data.selection)
                applyMask(image_left_ocv, roi_data);
            applyMask(cvImage, roi_data);

            viewer.updateData(bodies, cam_pose.pose_data);
            render_2D(image_left_ocv, img_scale, bodies.body_list, bodies.is_tracked);
            cv::imshow(imWndName, image_left_ocv);
            cv::imshow("left", cvImage);
            //Display the image and the current global ROI
            cv::imshow(depthWndName, depth_image_ocv);
            cv::imshow(ROIWndName, roi_data.ROI);
            int svo_position = zed.getSVOPosition();


            stringstream file;
            stringstream filed;
            stringstream file1;

            if (bodies.is_new) {
                count_1++;
                file << "D:/Pruebas_Captura/Adquisicion/Jugador4Sec1/" << "Skeleton2d" << count_1 << ".jpg";
                cv::imwrite(file.str(), image_left_ocv);

                file1 << "D:/Pruebas_Captura/Adquisicion/Jugador4Sec1/" << "rgb" << count_1 << ".jpg";
                cv::imwrite(file1.str(), cvImage);

                filed << "D:/Pruebas_Captura/Adquisicion/Jugador4Sec1/" << "depth" << count_1 << ".png";
                cv::imwrite(filed.str(), depth_image_ocv);

                float min_distance = std::numeric_limits<float>::max(); // Inicializa con un valor grande
                auto& nearest_object = bodies.body_list[0]; // Inicializa con el primer objeto
                // Itera a través de la lista de objetos detectados
                for (auto& current_body : bodies.body_list) {
                    float current_z = std::abs(current_body.position.z);
                    // Comprueba si la coordenada Z (profundidad) del objeto actual es menor que la mínima conocida
                    if (current_z < min_distance) {
                        // Actualiza el objeto más cercano
                        min_distance = current_z;
                        nearest_object = current_body;
                    }
                }
                MyFile << "frame " << count_1 << " " << bodies.body_list.size() << " Person(s) detected\n\n";
                auto& first_object = nearest_object;
                MyFile << "First Person attributes :\n";
                MyFile << " Confidence (" << first_object.confidence << "/100)\n";

                MyFile << " Tracking ID: " << first_object.id << " tracking state: " <<
                    first_object.tracking_state << " / " << first_object.action_state << "\n";
                MyFile << " 3D position: " << first_object.position;

                MyFile << " 3D dimensions: " << first_object.dimensions << "\n";

                MyFile << " Keypoints 2D \n";
                // The body part meaning can be obtained by casting the index into a BODY_PARTS
                // to get the BODY_PARTS index the getIdx function is available
                for (int i = 0; i < first_object.keypoint.size(); i++) {
                    auto& kp = first_object.keypoint[i];
                    MyFile << "    " << printBodyParts((BODY_38_PARTS)i) << " " << kp.x << ", " << kp.y << "\n";
                }

                // The BODY_PARTS can be link as bones, using sl::BODY_BONES which gives the BODY_PARTS pair for each
                MyFile << " Keypoints 3D \n";
                for (int i = 0; i < first_object.keypoint.size(); i++) {
                    auto& kp = first_object.keypoint[i];
                    MyFile << "    " << printBodyParts((BODY_38_PARTS)i) << " " << kp.x << ", " << kp.y << ", " << kp.z << "\n";
                }




            }

            //key = cv::waitKey(10);

            /*switch (key) {
            case 's':
                svo_image.write(("capture_" + to_string(svo_position) + ".png").c_str());
                break;
            case 'f':
                zed.setSVOPosition(svo_position + svo_frame_rate);
                break;
            case 'b':
                zed.setSVOPosition(svo_position - svo_frame_rate);
                break;
            }*/

            ProgressBar((float)(svo_position / (float)nb_frames), 60);
            //}
            //else if (returned_state == sl::ERROR_CODE::END_OF_SVOFILE_REACHED)
            //{
            //    print("SVO end has been reached. Looping back to 0\n");
            //    zed.setSVOPosition(0);
            //}
            //else {
            //    print("Grab ZED : ", returned_state);
            //    break;
        }
        key = cv::waitKey(10);
        // Apply Current ROI
        if (key == 'a') {
            Mat slROI(resolution, MAT_TYPE::U8_C1, roi_data.ROI.data, roi_data.ROI.step);
            zed.setRegionOfInterest(slROI);
        }
        else if (key == 'r') { //Reset ROI
            Mat emptyROI;
            zed.setRegionOfInterest(emptyROI);
            // clear user data
            roi_data.reset();
        }
        else if (key == 's') {
            // Save the current Mask to be loaded in another app
            cv::imwrite(mask_name, roi_data.ROI);
        }
        else if (key == 'l') {
            // Load the mask from a previously saved file
            cv::Mat tmp = cv::imread(mask_name);
            if (!tmp.empty()) {
                roi_data.ROI = tmp;
                Mat slROI(resolution, MAT_TYPE::U8_C1, roi_data.ROI.data, roi_data.ROI.step);
                zed.setRegionOfInterest(slROI);
            }
            else std::cout << mask_name << " could not be found" << std::endl;
        }
    }
    viewer.exit();
    image_left.free();
    bodies.body_list.clear();
    zed.disableBodyTracking();
    zed.disablePositionalTracking();
    zed.close();
    return EXIT_SUCCESS;
}

void parseArgs(int argc, char** argv, InitParameters& param) {
    if (argc > 1 && string(argv[1]).find(".svo") != string::npos) {
        // SVO input mode
        param.input.setFromSVOFile(argv[1]);
        cout << "[Sample] Using SVO File input: " << argv[1] << endl;
    }
    else if (argc > 1 && string(argv[1]).find(".svo") == string::npos) {
        string arg = string(argv[1]);
        unsigned int a, b, c, d, port;
        if (sscanf(arg.c_str(), "%u.%u.%u.%u:%d", &a, &b, &c, &d, &port) == 5) {
            // Stream input mode - IP + port
            string ip_adress = to_string(a) + "." + to_string(b) + "." + to_string(c) + "." + to_string(d);
            param.input.setFromStream(String(ip_adress.c_str()), port);
            cout << "[Sample] Using Stream input, IP : " << ip_adress << ", port : " << port << endl;
        }
        else if (sscanf(arg.c_str(), "%u.%u.%u.%u", &a, &b, &c, &d) == 4) {
            // Stream input mode - IP only
            param.input.setFromStream(String(argv[1]));
            cout << "[Sample] Using Stream input, IP : " << argv[1] << endl;
        }
        else if (arg.find("HD2K") != string::npos) {
            param.camera_resolution = RESOLUTION::HD2K;
            cout << "[Sample] Using Camera in resolution HD2K" << endl;
        }
        else if (arg.find("HD1200") != string::npos) {
            param.camera_resolution = RESOLUTION::HD1200;
            cout << "[Sample] Using Camera in resolution HD1200" << endl;
        }
        else if (arg.find("HD1080") != string::npos) {
            param.camera_resolution = RESOLUTION::HD1080;
            cout << "[Sample] Using Camera in resolution HD1080" << endl;
        }
        else if (arg.find("HD720") != string::npos) {
            param.camera_resolution = RESOLUTION::HD720;
            cout << "[Sample] Using Camera in resolution HD720" << endl;
        }
        else if (arg.find("SVGA") != string::npos) {
            param.camera_resolution = RESOLUTION::SVGA;
            cout << "[Sample] Using Camera in resolution SVGA" << endl;
        }
        else if (arg.find("VGA") != string::npos) {
            param.camera_resolution = RESOLUTION::VGA;
            cout << "[Sample] Using Camera in resolution VGA" << endl;
        }
    }
}

void print(string msg_prefix, ERROR_CODE err_code, string msg_suffix) {
    cout << "[Sample]";
    if (err_code != ERROR_CODE::SUCCESS)
        cout << "[Error] ";
    else
        cout << " ";
    cout << msg_prefix << " ";
    if (err_code != ERROR_CODE::SUCCESS) {
        cout << " | " << toString(err_code) << " : ";
        cout << toVerbose(err_code);
    }
    if (!msg_suffix.empty())
        cout << " " << msg_suffix;
    cout << endl;
}

#if SELECT_RECT
void applyMask(cv::Mat& cvImage, ROIdata& data) {
    auto res = cvImage.size();
    const float darker = 0.8f; // make the image darker

    for (int y = 0; y < res.height; y++) {
        // line pointer
        uchar* ptr_mask = (uchar*)((data.ROI.data) + y * data.ROI.step);
        sl::uchar4* ptr_image = (sl::uchar4*)(cvImage.data + y * cvImage.step);

        for (int x = 0; x < res.width; x++) {
            if (ptr_mask[x] == 0) {
                auto& px = ptr_image[x];
                // make the pixel darker without overflow
                px.x = px.x * darker;
                px.y = px.y * darker;
                px.z = px.z * darker;
            }
        }
    }

    // DIsplay current selection
    cv::rectangle(cvImage, data.selection_rect, cv::Scalar(255, 90, 0, 255), 3);
}
#else

inline bool contains(std::vector<cv::Point>& poly, cv::Point2f test) {
    int i, j;
    bool c = false;
    const int nvert = poly.size();
    for (i = 0, j = nvert - 1; i < nvert; j = i++) {
        if (((poly[i].y > test.y) != (poly[j].y > test.y)) &&
            (test.x < (poly[j].x - poly[i].x) * (test.y - poly[i].y) / (poly[j].y - poly[i].y) + poly[i].x))
            c = !c;
    }
    return c;
}

inline bool contains(std::vector<std::vector<cv::Point>>& polygons, cv::Point2f test) {
    bool c = false;
    for (auto& it : polygons) {
        c = contains(it, test);
        if (c) break;
    }
    return c;
}

void applyMask(cv::Mat& cvImage, ROIdata& data) {
    // left_sl and mask must be at the same size
    auto res = cvImage.size();
    const float darker = 0.8f; // make the image darker

    // Convert P�lygons into real Mask
#if 1 // manual check
    for (int y = 0; y < res.height; y++) {
        uchar* ptr_mask = (uchar*)((data.ROI.data) + y * data.ROI.step);
        sl::uchar4* ptr_image = (sl::uchar4*)(cvImage.data + y * cvImage.step);
        for (int x = 0; x < res.width; x++) {
            if (contains(data.polygons, cv::Point2f(x, y)))
                ptr_mask[x] = 255;
            else {
                auto& px = ptr_image[x];
                // make the pixel darker without overflow
                px.x = px.x * darker;
                px.y = px.y * darker;
                px.z = px.z * darker;
            }
        }
    }
#else // same with open Function
    cv::fillPoly(data.ROI, data.polygons, 255);
#endif

    // Display current selection
    if (data.current_select.size() > 2) {
        auto last = data.current_select.back();
        for (auto& it : data.current_select) {
            cv::line(cvImage, last, it, cv::Scalar(30, 130, 240), 1);
            last = it;
        }
    }
}
#endif