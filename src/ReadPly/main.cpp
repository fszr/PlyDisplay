#include <iostream>
#include <string>
#include <vector>
#include <pcl/point_cloud.h>
#include <pcl/visualization/pcl_visualizer.h>

#include <rapidcsv.h>
/*�������ԽǶ�*/
/*��ɫ��X�ᣬ��ɫ��Y�ᣬ��ɫ��Z��Ҳ����˵PCL���ƿ���ʹ�õ���������ά����ϵ��*/

using namespace std;

int main() {
	std::string filePath = "E:/DataSets/lecturehall/lecturehall1.pose1.object1.label.csv";
	rapidcsv::Document doc(filePath, rapidcsv::LabelParams(-1, -1));

	const int rowCount = doc.GetRowCount();
	const int colCount = doc.GetColumnCount();

	//�������ƶ���ָ�������
	pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_ptr(new pcl::PointCloud<pcl::PointXYZ>);
	pcl::PointCloud<pcl::PointXYZ>& cloud = *cloud_ptr;

	for (int i = 0; i < 100; ++i)
	{
		vector<float> row = doc.GetRow<float>(i);
		pcl::PointXYZ p;
		p.x = row[0];
		p.y = row[1];
		p.z = row[2];
		cloud_ptr->points.push_back(p);
	}

	//std::cout << "cloud.sensor_orientation_.matrix() ��\n" << cloud.sensor_orientation_.matrix() << std::endl; // x y z ���� ƫ�� u
	//std::cout << "cloud.sensor_origin_\n" << cloud.sensor_origin_ << std::endl;

	pcl::visualization::PCLVisualizer viewer("viewer");
	std::cout << "��ʼ����̬����\n" << viewer.getViewerPose().matrix() << std::endl;

	viewer.addCoordinateSystem(0.5);
	viewer.addPointCloud(cloud_ptr);
	//viewer.setCameraPosition(3, 0, 0, -1, 0, 0, 0, 1, 0); //�ӵ� ���� �Ϸ��� 

	viewer.spin();

	return 0;
}
