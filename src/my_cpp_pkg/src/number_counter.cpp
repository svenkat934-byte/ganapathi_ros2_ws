#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/int64.hpp"

using namespace std::placeholders;


class NumberSubscriberNode : public rclcpp::Node
{
    public:
        NumberSubscriberNode() : Node("number_publisher_node")
        {
            number_subscribe_ = this->create_subscription<example_interfaces::msg::Int64>("number", 10, std::bind(&NumberCounterNode::callbackNumber, this, _1));
        }

}