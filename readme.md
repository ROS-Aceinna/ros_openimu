ros_openimu

ROS driver for Aceinna OpenIMU products

- Please refer to the included application note for further information.


### Changes made to integrate OpenIMU300RI

The default axis orientation of the device is not compliant with The ros standard. 

Changes are from  X Y Z to X -Y - Z


    Acceleration: Be careful with acceleration data. The state estimation nodes in robot_localization assume that an IMU that is placed in its neutral right-side-up position on a flat surface will:

        > Measure +9.81 meters per second squared for the Z axis.
If the sensor is rolled +90
degrees (left side up), the acceleration should be +9.81 meters per second squared for the Y
axis. <br/>
If the sensor is pitched +90
degrees (front side down), it should read -9.81 meters per second squared for the X axis.


