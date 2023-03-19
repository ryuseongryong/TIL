# http package
- https://pkg.go.dev/net/http#Response

## Response Struct
- Status string
- StatusCode int
- Body io.ReadCloser

### io.ReadCloser Interface
- Reader
- Closer

### io.Reader Interface
- Read([]byte) (int, error)

### io.Closer Interface
- Close() (error)

```
type ReadCloser
type ReadCloser interface {
	Reader
	Closer
}
```