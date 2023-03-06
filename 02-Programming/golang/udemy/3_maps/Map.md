Map(Go) == Hash(Ruby) == Object(JS) == Dict(Python)

# Map
```
key -> value
key -> value
key -> value
```
- keys are the same type
- values are the same type
- key and value no need to same type

# Map vs Struct
## Map
- All keys must be the same type
- All values must be the same type
- Keys are indexed : we can iterate over them
- Use to represent a collection of related properties
- Don't need to know all the keys at compile time
- Reference Type

## Struct
- Values can be of different type
- Keys don't support indexing
- You need to know all the different fields at compile time
- Use to represent a "thing" with a lot of different properties
- Value Type