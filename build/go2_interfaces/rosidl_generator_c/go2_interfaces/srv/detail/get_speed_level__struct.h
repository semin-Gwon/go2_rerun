// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from go2_interfaces:srv/GetSpeedLevel.idl
// generated code does not contain a copyright notice

#ifndef GO2_INTERFACES__SRV__DETAIL__GET_SPEED_LEVEL__STRUCT_H_
#define GO2_INTERFACES__SRV__DETAIL__GET_SPEED_LEVEL__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/GetSpeedLevel in the package go2_interfaces.
typedef struct go2_interfaces__srv__GetSpeedLevel_Request
{
  uint8_t structure_needs_at_least_one_member;
} go2_interfaces__srv__GetSpeedLevel_Request;

// Struct for a sequence of go2_interfaces__srv__GetSpeedLevel_Request.
typedef struct go2_interfaces__srv__GetSpeedLevel_Request__Sequence
{
  go2_interfaces__srv__GetSpeedLevel_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} go2_interfaces__srv__GetSpeedLevel_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/GetSpeedLevel in the package go2_interfaces.
typedef struct go2_interfaces__srv__GetSpeedLevel_Response
{
  bool success;
  rosidl_runtime_c__String message;
  int32_t level;
} go2_interfaces__srv__GetSpeedLevel_Response;

// Struct for a sequence of go2_interfaces__srv__GetSpeedLevel_Response.
typedef struct go2_interfaces__srv__GetSpeedLevel_Response__Sequence
{
  go2_interfaces__srv__GetSpeedLevel_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} go2_interfaces__srv__GetSpeedLevel_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // GO2_INTERFACES__SRV__DETAIL__GET_SPEED_LEVEL__STRUCT_H_
