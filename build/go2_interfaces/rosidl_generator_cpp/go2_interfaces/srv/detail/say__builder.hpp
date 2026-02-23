// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from go2_interfaces:srv/Say.idl
// generated code does not contain a copyright notice

#ifndef GO2_INTERFACES__SRV__DETAIL__SAY__BUILDER_HPP_
#define GO2_INTERFACES__SRV__DETAIL__SAY__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "go2_interfaces/srv/detail/say__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace go2_interfaces
{

namespace srv
{

namespace builder
{

class Init_Say_Request_text
{
public:
  Init_Say_Request_text()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::go2_interfaces::srv::Say_Request text(::go2_interfaces::srv::Say_Request::_text_type arg)
  {
    msg_.text = std::move(arg);
    return std::move(msg_);
  }

private:
  ::go2_interfaces::srv::Say_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::go2_interfaces::srv::Say_Request>()
{
  return go2_interfaces::srv::builder::Init_Say_Request_text();
}

}  // namespace go2_interfaces


namespace go2_interfaces
{

namespace srv
{

namespace builder
{

class Init_Say_Response_message
{
public:
  explicit Init_Say_Response_message(::go2_interfaces::srv::Say_Response & msg)
  : msg_(msg)
  {}
  ::go2_interfaces::srv::Say_Response message(::go2_interfaces::srv::Say_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::go2_interfaces::srv::Say_Response msg_;
};

class Init_Say_Response_success
{
public:
  Init_Say_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Say_Response_message success(::go2_interfaces::srv::Say_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_Say_Response_message(msg_);
  }

private:
  ::go2_interfaces::srv::Say_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::go2_interfaces::srv::Say_Response>()
{
  return go2_interfaces::srv::builder::Init_Say_Response_success();
}

}  // namespace go2_interfaces

#endif  // GO2_INTERFACES__SRV__DETAIL__SAY__BUILDER_HPP_
