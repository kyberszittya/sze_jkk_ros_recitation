#include <ros/ros.h>
#include <std_msgs/Float32.h>
#include <chrono>
#include <thread>
#include <memory>

void sineFunctionThread(std::shared_ptr<ros::NodeHandle> nh){
    ros::Publisher pub = nh->advertise<std_msgs::Float32>("/sin",100);
    std_msgs::Float32 msg;
    while(ros::ok()){
        auto now = std::chrono::system_clock::now().time_since_epoch();
        float val = sin(std::chrono::duration_cast<std::chrono::milliseconds>(now).count()/1000.0);
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
        msg.data = val;
        pub.publish(msg);
    }
}

void squareFunctionThread(std::shared_ptr<ros::NodeHandle> nh){
    ros::Publisher pub = nh->advertise<std_msgs::Float32>("/square",100);
    std_msgs::Float32 msg;
    while(ros::ok()){
        auto now = std::chrono::system_clock::now().time_since_epoch();
        auto t = std::chrono::duration_cast<std::chrono::milliseconds>(now).count()/1000.0;
        float val = sin(t / 2.0 * 2.0 * M_PI)>=0.0 ? 1.0:-1.0;
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
        msg.data = val;
        pub.publish(msg);
    }
}

void sawtoothFunctionThread(std::shared_ptr<ros::NodeHandle> nh){
    ros::Publisher pub = nh->advertise<std_msgs::Float32>("/saw",100);
    std_msgs::Float32 msg;
    while(ros::ok()){
        auto now = std::chrono::system_clock::now().time_since_epoch();
        auto t = std::chrono::duration_cast<std::chrono::milliseconds>(now).count()/1000.0;
        float val = t - floor(t);
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
        msg.data = val;
        pub.publish(msg);
    }
}

int main(int argc, char **argv){
    ros::init(argc, argv, "function_generator");
    ros::AsyncSpinner spinner(4);
    spinner.start();
    std::shared_ptr<ros::NodeHandle> nh(new ros::NodeHandle);
    std::thread t0 = std::thread(sineFunctionThread, nh);
    t0.detach();
    std::thread t1 = std::thread(squareFunctionThread, nh);
    t1.detach();
    std::thread t2 = std::thread(sawtoothFunctionThread, nh);
    t2.detach();
    //ros::spin();
    ros::waitForShutdown();
    return 0;
}