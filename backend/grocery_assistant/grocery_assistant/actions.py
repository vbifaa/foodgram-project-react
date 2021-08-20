from rest_framework import status
from rest_framework.response import Response


def try_action(func, args, mssg_error):
    try:
        func(**args)
    except Exception:
        return Response(
            data=mssg_error,
            status=status.HTTP_400_BAD_REQUEST
        )


def create_or_delete_obj_use_func(
    is_delete, serializer, func, args, msg_errors
):
    serializer.is_valid(raise_exception=True)

    if is_delete:
        res = try_action(
            func=func['delete'], args=args['delete'], mssg_error=['delete']
        )
        if res is not None:
            return res
        return Response(status=status.HTTP_204_NO_CONTENT)

    res = try_action(
        func=func['create'],
        args=args['create'],
        mssg_error=msg_errors['create']
    )
    if res is not None:
        return res

    return Response(serializer.data, status=status.HTTP_201_CREATED)
