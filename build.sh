python3.6 ./aws/test/lambda_test.py
python3.6 ./device/test/roku_test.py
mkdir -p ./build/
rm ./build/lambda.zip
cp ./aws/main/lambda_handler.py ./build
cd build
zip lambda.zip lambda_handler.py
rm lambda_handler.py