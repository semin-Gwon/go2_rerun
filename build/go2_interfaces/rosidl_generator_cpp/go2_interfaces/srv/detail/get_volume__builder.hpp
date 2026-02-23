// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from go2_interfaces:srv/GetVolume.idl
// generated code does not contain a copyright notice

#ifndef GO2_INTERFACES__SRV__DETAIL__GET_VOLUME__BUILDER_HPP_
#define GO2_INTERFACES__SRV__DETAIL__GET_VOLUME__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "go2_interfaces/srv/detail/get_volume__struct.hpp"
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
auto build<::go2_interfaces::srv::GetVolume_Request>()
{
  return ::go2_interfaces::srv::GetVolume_Request(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace go2_interfaces


namespace go2_interfaces
{

namespace srv
{

namespace builder
{

class Init_GetVolume_Response_volume
{
public:
  explicit Init_GetVolume_Response_volume(::go2_interfaces::srv::GetVolume_Response & msg)
  : msg_(msg)
  {}
  ::go2_interfaces::srv::GetVolume_Response volume(::go2_interfaces::srv::GetVolume_Response::_volume_type arg)
  {
    msg_.volume = std::move(arg);
    return std::move(msg_);
  }

private:
  ::go2_interfaces::srv::GetVolume_Response msg_;
};

class Init_GetVolume_Response_message
{
public:
  explicit Init_GetVolume_Response_message(::go2_interfaces::srv::GetVolume_Response & msg)
  : msg_(msg)
  {}
  Init_GetVolume_Response_volume message(::go2_interfaces::srv::GetVolume_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return Init_GetVolume_Response_volume(msg_);
  }

private:
  ::go2_interfaces::srv::GetVolume_Response msg_;
};

class Init_GetVolume_Response_success
{
public:
  Init_GetVolume_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GetVolume_Response_message success(::go2_interfaces::srv::GetVolume_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_GetVolume_Response_message(msg_);
  }

private:
  ::go2_interfaces::srv::GetVolume_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::go2_interfaces::srv::GetVolume_Response>()
{
  return go2_interfaces::srv::builder::Init_GetVolume_Response_success();
}

}  // namespace go2_interfaces

#endif  // GO2_INTERFACES__SRV__DETAIL__GET_VOLUME__BUILDER_HPP_
