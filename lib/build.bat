@echo on
go mod tidy
go build -buildmode=c-shared -o d2lib.dll d2lib.go
if not exist ..\d2\resources mkdir ..\d2\resources
copy d2lib.dll ..\d2\resources\
del d2lib.dll
dir ..\d2\
dir ..\d2\resources\
