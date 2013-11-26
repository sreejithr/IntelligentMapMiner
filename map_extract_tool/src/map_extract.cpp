#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"

#include <boost/python.hpp>
#include <exception>
#include <iostream>
#include <vector>

using namespace cv;
using namespace std;
namespace py = boost::python;


class OpenCVMapAnalyzer {

    public:

        template<class T>
        py::list std_vector_to_py_list(std::vector<T>& v)
        {
            py::list l;
            for (size_t i=0; i<v.size(); i++)
                l.append(v.at(i));

            return l;
        }

        py::list extract_points(string input_filename, string output_filename)
        {
            Mat img = imread(input_filename, 0);
            if(img.empty())
            {
                throw invalid_argument("File provided is empty");
            }

            Mat cimg;
            //medianBlur(img, img, 5);
            cvtColor(img, cimg, CV_GRAY2BGR);

            vector<Vec3f> circles;
            vector<int> coordinates;

            py::list py_list_coordinates;

            HoughCircles(img, circles, CV_HOUGH_GRADIENT, 2, 5,
                         100, 20, 0, 5 // change the last two parameters
                                       // (min_radius & max_radius) to detect larger circles
                         );

            for( size_t i = 0; i < circles.size(); i++ )
            {
                Vec3i c = circles[i];
                circle( cimg, Point(c[0], c[1]), c[2], Scalar(0,255,0), 3, CV_AA);
                circle( cimg, Point(c[0], c[1]), 2, Scalar(0,0,255), 3, CV_AA);
                coordinates.push_back(c[0]);
                coordinates.push_back(c[1]);
            }

            py_list_coordinates = this->std_vector_to_py_list(coordinates);
            cv::imwrite(output_filename, cimg);

            return py_list_coordinates;
        }
};


BOOST_PYTHON_MODULE(map_extract) {
    py::class_<OpenCVMapAnalyzer>("OpenCVMapAnalyzer")
        .def("extract_points", &OpenCVMapAnalyzer::extract_points)
    ;
}
