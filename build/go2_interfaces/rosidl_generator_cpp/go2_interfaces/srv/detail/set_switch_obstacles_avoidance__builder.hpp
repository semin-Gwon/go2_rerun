// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from go2_interfaces:srv/SetSwitchObstaclesAvoidance.idl
// generated code does not contain a copyright notice

#ifndef GO2_INTERFACES__SRV__DETAIL__SET_SWITCH_OBSTACLES_AVOIDANCE__BUILDER_HPP_
#define GO2_INTERFACES__SRV__DETAIL__SET_SWITCH_OBSTACLES_AVOIDANCE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "go2_interfaces/srv/detail/set_switch_obstacles_avoidance__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace go2_interfaces
{

namespace srv
{

namespace builder
{

class Init_SetSwitchObstaclesAvoidance_Request_enable
{
public:
  Init_SetSwitchObstaclesAvoidance_Request_enable()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::go2_interfaces::srv::SetSwitchObstaclesAvoidance_Request enable(::go2_interfaces::srv::SetSwitchObstaclesAvoidance_Request::_enable_type arg)
  {
    msg_.enable = std::move(arg);
    return std::move(msg_);
  }

private:
  ::go2_interfaces::srv::SetSwitchObstaclesAvoidance_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::go2_interfaces::srv::SetSwitchObstaclesAvoidance_Request>()
{
  return go2_interfaces::srv::builder::Init_SetSwitchObstaclesAvoidance_Request_enable();
}

}  // namespace go2_interfaces


namespace go2_interfaces
{

namespace srv
{

namespace builder
{

class Init_SetSwitchObstaclesAvoidance_Response_message
{
public:
  explicit Init_SetSwitchObstaclesAvoidance_Response_message(::go2_interfaces::srv::SetSwitchObstaclesAvoidance_Response & msg)
  : msg_(msg)
  {}
  ::go2_interfaces::srv::SetSwitchObstaclesAvoidance_Response message(::go2_interfaces::srv::SetSwitchObstaclesAvoidance_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::go2_interfaces::srv::SetSwitchObstaclesAvoidance_Response msg_;
};

class Init_SetSwitchObstaclesAvoidance_Response_success
{
public:
  Init_SetSwitchObstaclesAvoidance_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SetSwitchObstaclesAvoidance_Response_message success(::go2_interfaces::srv::SetSwitchObstaclesAvoidance_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_SetSwitchObstaclesAvoidance_Response_message(msg_);
  }

private:
  ::go2_interfaces::srv::SetSwitchObstaclesAvoidance_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::go2_interfaces::srv::SetSwitchObstaclesAvoidance_Response>()
{
  return go2_interfaces::srv::builder::Init_SetSwitchObstaclesAvoidance_Response_success();
}

}  // namespace go2_interfaces

#endif  // GO2_INTERFACES__SRV__DETAIL__SET_SWITCH_OBSTACLES_AVOIDANCE__BUILDER_HPP_
