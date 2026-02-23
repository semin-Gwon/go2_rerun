// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from go2_interfaces:srv/SetBrightness.idl
// generated code does not contain a copyright notice

#ifndef GO2_INTERFACES__SRV__DETAIL__SET_BRIGHTNESS__TRAITS_HPP_
#define GO2_INTERFACES__SRV__DETAIL__SET_BRIGHTNESS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "go2_interfaces/srv/detail/set_brightness__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace go2_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const SetBrightness_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: brightness
  {
    out << "brightness: ";
    rosidl_generator_traits::value_to_yaml(msg.brightness, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SetBrightness_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: brightness
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "brightness: ";
    rosidl_generator_traits::value_to_yaml(msg.brightness, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SetBrightness_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace go2_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use go2_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const go2_interfaces::srv::SetBrightness_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  go2_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use go2_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const go2_interfaces::srv::SetBrightness_Request & msg)
{
  return go2_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<go2_interfaces::srv::SetBrightness_Request>()
{
  return "go2_interfaces::srv::SetBrightness_Request";
}

template<>
inline const char * name<go2_interfaces::srv::SetBrightness_Request>()
{
  return "go2_interfaces/srv/SetBrightness_Request";
}

template<>
struct has_fixed_size<go2_interfaces::srv::SetBrightness_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<go2_interfaces::srv::SetBrightness_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<go2_interfaces::srv::SetBrightness_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace go2_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const SetBrightness_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: message
  {
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SetBrightness_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }

  // member: message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SetBrightness_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace go2_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use go2_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const go2_interfaces::srv::SetBrightness_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  go2_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use go2_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const go2_interfaces::srv::SetBrightness_Response & msg)
{
  return go2_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<go2_interfaces::srv::SetBrightness_Response>()
{
  return "go2_interfaces::srv::SetBrightness_Response";
}

template<>
inline const char * name<go2_interfaces::srv::SetBrightness_Response>()
{
  return "go2_interfaces/srv/SetBrightness_Response";
}

template<>
struct has_fixed_size<go2_interfaces::srv::SetBrightness_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<go2_interfaces::srv::SetBrightness_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<go2_interfaces::srv::SetBrightness_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<go2_interfaces::srv::SetBrightness>()
{
  return "go2_interfaces::srv::SetBrightness";
}

template<>
inline const char * name<go2_interfaces::srv::SetBrightness>()
{
  return "go2_interfaces/srv/SetBrightness";
}

template<>
struct has_fixed_size<go2_interfaces::srv::SetBrightness>
  : std::integral_constant<
    bool,
    has_fixed_size<go2_interfaces::srv::SetBrightness_Request>::value &&
    has_fixed_size<go2_interfaces::srv::SetBrightness_Response>::value
  >
{
};

template<>
struct has_bounded_size<go2_interfaces::srv::SetBrightness>
  : std::integral_constant<
    bool,
    has_bounded_size<go2_interfaces::srv::SetBrightness_Request>::value &&
    has_bounded_size<go2_interfaces::srv::SetBrightness_Response>::value
  >
{
};

template<>
struct is_service<go2_interfaces::srv::SetBrightness>
  : std::true_type
{
};

template<>
struct is_service_request<go2_interfaces::srv::SetBrightness_Request>
  : std::true_type
{
};

template<>
struct is_service_response<go2_interfaces::srv::SetBrightness_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // GO2_INTERFACES__SRV__DETAIL__SET_BRIGHTNESS__TRAITS_HPP_
