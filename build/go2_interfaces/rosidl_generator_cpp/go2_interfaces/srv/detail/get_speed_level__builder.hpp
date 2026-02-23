// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from go2_interfaces:srv/GetSpeedLevel.idl
// generated code does not contain a copyright notice

#ifndef GO2_INTERFACES__SRV__DETAIL__GET_SPEED_LEVEL__BUILDER_HPP_
#define GO2_INTERFACES__SRV__DETAIL__GET_SPEED_LEVEL__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "go2_interfaces/srv/detail/get_speed_level__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace go2_interfaces
{

namespace srv
{


}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::go2_interfaces::srv::GetSpeedLevel_Request>()
{
  return ::go2_interfaces::srv::GetSpeedLevel_Request(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace go2_interfaces


namespace go2_interfaces
{

namespace srv
{

namespace builder
{

class Init_GetSpeedLevel_Response_level
{
public:
  explicit Init_GetSpeedLevel_Response_level(::go2_interfaces::srv::GetSpeedLevel_Response & msg)
  : msg_(msg)
  {}
  ::go2_interfaces::srv::GetSpeedLevel_Response level(::go2_interfaces::srv::GetSpeedLevel_Response::_level_type arg)
  {
    msg_.level = std::move(arg);
    return std::move(msg_);
  }

private:
  ::go2_interfaces::srv::GetSpeedLevel_Response msg_;
};

class Init_GetSpeedLevel_Response_message
{
public:
  explicit Init_GetSpeedLevel_Response_message(::go2_interfaces::srv::GetSpeedLevel_Response & msg)
  : msg_(msg)
  {}
  Init_GetSpeedLevel_Response_level message(::go2_interfaces::srv::GetSpeedLevel_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return Init_GetSpeedLevel_Response_level(msg_);
  }

private:
  ::go2_interfaces::srv::GetSpeedLevel_Response msg_;
};

class Init_GetSpeedLevel_Response_success
{
public:
  Init_GetSpeedLevel_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GetSpeedLevel_Response_message success(::go2_interfaces::srv::GetSpeedLevel_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_GetSpeedLevel_Response_message(msg_);
  }

private:
  ::go2_interfaces::srv::GetSpeedLevel_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::go2_interfaces::srv::GetSpeedLevel_Response>()
{
  return go2_interfaces::srv::builder::Init_GetSpeedLevel_Response_success();
}

}  // namespace go2_interfaces

#endif  // GO2_INTERFACES__SRV__DETAIL__GET_SPEED_LEVEL__BUILDER_HPP_
