#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"

#include <boost/python.hpp>
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
            // py::object get_iter = py::iterator<std::vector<T> >();
            // py::object iter = get_iter(v);
            py::list l;
            for (size_t i=0; i<v.size(); i++) {
                l.append(v.at(i));
            }
            return l;
        }

        py::list extract_points(string file)
        {
            string filename = "/Users/sreejith/Desktop/cape.tiff";

            Mat img = imread(filename, 0);
            // if(img.empty())
            // {
            //     help();
            //     cout << "Cannot open\n" << filename << endl;
            //     return -1;
            // }

            Mat cimg;
            //medianBlur(img, img, 5);
            cvtColor(img, cimg, CV_GRAY2BGR);

            vector<Vec3f> circles;
            vector<int> coordinate(2);
            vector<int> coordinates(100);

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
                coordinates.at(i) = c[0];
                coordinates.at(i+1) = c[1];
                //auto py_list_coordinate = this->std_vector_to_py_list(coordinate);
                //coordinates.at(i) = coordinate;
            }

            py_list_coordinates = this->std_vector_to_py_list(coordinates);
            // imshow("detected circles", cimg);
            filename = "/Users/sreejith/Desktop/circles.jpg";
            cv::imwrite(filename, cimg);
            // waitKey();

            return py_list_coordinates;
        }
};


BOOST_PYTHON_MODULE(map_extract) {
    py::class_<OpenCVMapAnalyzer>("OpenCVMapAnalyzer")
        .def("extract_points", &OpenCVMapAnalyzer::extract_points)
    ;
}
