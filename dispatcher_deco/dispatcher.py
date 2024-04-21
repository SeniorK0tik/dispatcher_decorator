import inspect
from functools import wraps
from typing import Any, AsyncGenerator, Callable, Dict



class Dispatcher:
    """Транспортный объект"""
    def __init__(self, **kwargs) -> None:
        self.workflow_data: Dict[str, Any] = kwargs

    def __getitem__(self, item: str) -> Any:
        return self.workflow_data[item]

    def __setitem__(self, key: str, value: Any) -> None:
        self.workflow_data[key] = value

    def __delitem__(self, key: str) -> None:
        del self.workflow_data[key]

    def get(self, key: str, /, default: Any | None = None) -> Any | None:
        """Отдает значение из словаря"""
        return self.workflow_data.get(key, default)

    def add_to_workflow(self, **kwargs) -> None:
        """Добавляет ключ-значение в словарь"""
        self.workflow_data.update(kwargs)

    def inject(self, func: Callable, kwargs: dict) -> None:
        args_name = inspect.getfullargspec(func).args

        for arg in args_name:
            value = self.workflow_data.get(arg)
            if value:
                kwargs.update({arg: value})

    def __call__(self) -> Callable:  # noqa: C901
        def decorator(func: Callable) -> Callable:  # noqa: C901

            if inspect.iscoroutinefunction(func):
                @wraps(func)
                async def wrapper(*args, **kwargs) -> Any:
                    self.inject(func=func, kwargs=kwargs)
                    return await func(*args, **kwargs)

            elif inspect.isasyncgenfunction(func):
                async def wrapper(*args, **kwargs) -> AsyncGenerator[None, Any]:
                    self.inject(func=func, kwargs=kwargs)
                    async for res in func(*args, **kwargs):
                        yield res
            else:
                @wraps(func)
                def wrapper(*args, **kwargs) -> Any:
                    self.inject(func=func, kwargs=kwargs)
                    return func(*args, **kwargs)
            return wrapper
        return decorator
