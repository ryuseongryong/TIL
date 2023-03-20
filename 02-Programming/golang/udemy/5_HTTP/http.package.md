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

### Interface Review
- for code reusable

### Reader Interface
- Every value has a type
- Every function has to specify the type of its args
- Every function we ever write has to be rewritten to accommodate different types even if the logic in it is identical?

Source of Input 		  			 		 | Returns   | To print it
--|--|--
HTTP Req Bocy       	 		 	 		 | []flargen | func printHTTP([]flargen)
Text file on hard drive  			 		 | []string  | func printFile([]string)
Image file on hard drive 			 		 | jpegne	 | func printImage(jpegne)
User entering text into command line 		 | []byte	 | func printText([]byte)
Data from analog sensor plugged into machine | []float	 | func printData([]float)

Source of Input(*) -> Reader -> []byte : Output data that anyone can work with