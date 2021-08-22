from rest_framework import status
from rest_framework.response import Response


def try_action(func, args, msg_error):
    try:
        func(**args)
    except Exception:
        return Response(
            data=msg_error,
            status=status.HTTP_400_BAD_REQUEST
        )


def create_or_delete_obj_use_func(
    is_delete, serializer, func, args, msg_error
):
    serializer.is_valid(raise_exception=True)

    res = try_action(func=func, args=args, msg_error=msg_error)
    if res is not None:
        return res

    if is_delete:
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(serializer.data, status=status.HTTP_201_CREATED)
