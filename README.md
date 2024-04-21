# Examples

```python
import dataclasses


@dataclasses.dataclass
class DependencyModel:
    dep: str

dep_object = DependencyModel(dep="test")
    
dp = Dispatcher(
    dep_object=DependencyModel
)

@dp()
def main(dep_object: DependencyModel):
    print(dep_object)

main()
```