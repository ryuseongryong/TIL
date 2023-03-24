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

```
type Reader interface {
	Read(p []byte) (n int, err error)
}
```

Source of Input 		  			 		 | Returns   | To print it
--|--|--
HTTP Req Bocy       	 		 	 		 | Reader  	 | []byte
Text file on hard drive  			 		 | Reader  	 | []byte
Image file on hard drive 			 		 | Reader	 | []byte
User entering text into command line 		 | Reader	 | []byte
Data from analog sensor plugged into machine | Reader	 | []byte

`Byte Slice` : Thing that wants to read the body(something that wants to see the Reader Interface)
-> Thing that implements Reader: `Read([]byte) (int, err)` : Byte Slice <- Raw body of response

```
Thing to read data into
[]byte
0 1 2 ... n-1 n
```
```
<!doctype html>
<head>
...
Real source of data
```
=> Read

### Writer Interface
[]byte -> Write -> Some form of Output

Input |  		Returns 		 | Source of Output
--|--|--
[]byte | Writer | HTTP Req Bocy       	 		 	 		 
[]byte | Writer | Text file on hard drive  			 		 
[]byte | Writer | Image file on hard drive 			 		 
[]byte | Writer | User entering text into command line 		 
[]byte | Writer | Data from analog sensor plugged into machine 

- Writer Interface describes something that can take into and send it outside of our program
- We need to find something in the standard library that implements the Writer interface, and use that to log out all the data that we're receiving from the Reader

### io.Copy
- Something that implements the Writer interface -> os.Stdout -> value of type File -> File has a function called Write -> Therefore, it implements the Write interface
- Something that implements the Reader interface -> resp.Body

## implemetation io.Copy
```
func Copy(dst Writer, src Reader) (written int64, err error) {
	return copyBuffer(dst, src, nil)
}
```
```
func CopyBuffer(dst Writer, src Reader, buf []byte) (written int64, err error) {
	if buf != nil && len(buf) == 0 {
		panic("empty buffer in CopyBuffer")
	}
	return copyBuffer(dst, src, buf)
}
```
```
func copyBuffer(dst Writer, src Reader, buf []byte) (written int64, err error) {
	// If the reader has a WriteTo method, use it to do the copy.
	// Avoids an allocation and a copy.
	if wt, ok := src.(WriterTo); ok {
		return wt.WriteTo(dst)
	}
	// Similarly, if the writer has a ReadFrom method, use it to do the copy.
	if rt, ok := dst.(ReaderFrom); ok {
		return rt.ReadFrom(src)
	}
	if buf == nil {
		size := 32 * 1024
		if l, ok := src.(*LimitedReader); ok && int64(size) > l.N {
			if l.N < 1 {
				size = 1
			} else {
				size = int(l.N)
			}
		}
		buf = make([]byte, size)
	}
	for {
		nr, er := src.Read(buf)
		if nr > 0 {
			nw, ew := dst.Write(buf[0:nr])
			if nw < 0 || nr < nw {
				nw = 0
				if ew == nil {
					ew = errInvalidWrite
				}
			}
			written += int64(nw)
			if ew != nil {
				err = ew
				break
			}
			if nr != nw {
				err = ErrShortWrite
				break
			}
		}
		if er != nil {
			if er != EOF {
				err = er
			}
			break
		}
	}
	return written, err
}
```